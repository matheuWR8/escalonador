from dataclasses import dataclass, field

from model.prioridade import Prioridade


@dataclass
class Periodo:
    inicio: float
    fim: float
    tipo: str = "Execução"  # "Execução" ou "CTX"

    def get_duracao(self):
        return self.fim - self.inicio

    def contem_instante(self, instante, epsilon=0.0001):
        return self.inicio - epsilon <= instante < self.fim + epsilon


@dataclass(eq=False)
class Processo:
    id: int
    chegada: float
    duracao: float
    prioridade: Prioridade
    tempo_restante: float = field(init=False)
    processamentos: list = field(default_factory=list, init=False, repr=False)
    ultimo_contexto: object = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if not isinstance(self.prioridade, Prioridade):
            raise TypeError("prioridade deve ser uma instância de Prioridade.")
        if self.chegada < 0:
            raise ValueError("chegada deve ser não-negativa.")
        if self.duracao <= 0:
            raise ValueError("duracao deve ser maior que zero.")
        self.tempo_restante = self.duracao

    def adicionar_processamento(self, inicio, fim):
        if self.tempo_restante - (fim - inicio) < 0:
            fim = inicio + self.tempo_restante

        self.processamentos.append(Periodo(inicio, fim))
        self.tempo_restante -= fim - inicio

        return self.processamentos[-1].get_duracao()

    def adicionar_troca_contexto(self, inicio, fim):
        self.processamentos.append(Periodo(inicio, fim, "CTX"))
        return fim - inicio

    def get_turnaround(self):
        if not self.processamentos:
            return 0

        # Filtra apenas os períodos de execução
        periodos_execucao = [p for p in self.processamentos if p.tipo == "Execução"]
        if not periodos_execucao:
            return 0

        # Turnaround = término da última execução - chegada
        ultimo_periodo = periodos_execucao[-1]
        return ultimo_periodo.fim - self.chegada

    def get_espera(self):
        # T_w = T - t_p: tempo perdido na fila de prontas, em suspensão por
        # recurso e em trocas de contexto (C8). Não é o tempo até a 1ª
        # execução — ver get_tempo_ate_primeira_execucao.
        if not self.processamentos:
            return 0
        return self.get_turnaround() - self.duracao

    def get_tempo_ate_primeira_execucao(self):
        if not self.processamentos:
            return 0

        # Filtra apenas os períodos de execução
        periodos_execucao = [p for p in self.processamentos if p.tipo == "Execução"]
        if not periodos_execucao:
            return 0

        primeiro_periodo = periodos_execucao[0]
        return primeiro_periodo.inicio - self.chegada

    def verificar_estado(self, instante, epsilon=0.0001):
        if not self.processamentos:
            return "Desconhecido"

        if instante < self.chegada - epsilon:
            return "Antes da chegada"

        if instante >= self.processamentos[-1].fim - epsilon:
            return "Após a chegada"

        for periodo in self.processamentos:
            if periodo.contem_instante(instante, epsilon):
                return periodo.tipo

        return "Espera"

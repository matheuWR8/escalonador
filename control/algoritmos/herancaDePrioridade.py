from control.algoritmos._base import trocar_contexto, finalizar_metricas
from control.algoritmos.nomes import Algoritmo


def heranca_prioridade(processos, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    # Rastreamento de recursos e prioridades
    recursos = {}  # Mapa de processo -> tempo de liberação do recurso
    prioridade_original = {}  # Mapa de processo -> prioridade original

    # Ordenação inicial por chegada e prioridade
    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade.numero))

    while processos_ordenados:
        # Define próximo processo a executar
        processo_atual = processos_ordenados[0]

        # Avança o tempo se necessário
        if processo_atual.chegada > tempo_atual:
            tempo_atual = processo_atual.chegada

        # Se há processos de maior prioridade concorrendo pelo recurso que o
        # processo atual detém, ele herda a maior prioridade entre todos eles
        bloqueadores = [
            p for p in processos_ordenados
            if p.chegada <= tempo_atual and p.prioridade.numero > processo_atual.prioridade.numero
        ]
        if bloqueadores and processo_atual in recursos:
            if processo_atual not in prioridade_original:
                prioridade_original[processo_atual] = processo_atual.prioridade.numero
            processo_atual.prioridade.numero = max(p.prioridade.numero for p in bloqueadores)

        # Verifica se é hora de liberar algum recurso
        if processo_atual in recursos and tempo_atual >= recursos[processo_atual]:
            # Restaura prioridade original
            if processo_atual in prioridade_original:
                processo_atual.prioridade.numero = prioridade_original[processo_atual]
                del prioridade_original[processo_atual]
            # Libera o recurso
            del recursos[processo_atual]

        tempo_atual = trocar_contexto(ultimo_processo, processo_atual, tempo_atual, ctx_time, exigir_troca=True)

        # Executa por 1 unidade de tempo
        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)

        # Se o processo está começando, aloca o recurso
        if processo_atual.tempo_restante == processo_atual.duracao - 1:
            # Aloca o recurso por metade da duração do processo
            recursos[processo_atual] = tempo_atual + (processo_atual.duracao / 2)

        # Se o processo terminou
        if processo_atual.tempo_restante == 0:
            # Restaura prioridade original se necessário
            if processo_atual in prioridade_original:
                processo_atual.prioridade.numero = prioridade_original[processo_atual]
                del prioridade_original[processo_atual]
            # Remove processo da lista
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            processos_ordenados.remove(processo_atual)

        # Reordena os processos considerando as prioridades herdadas
        processos_ordenados.sort(key=lambda p: (
            p.chegada > tempo_atual,  # Primeiro os que já chegaram
            -p.prioridade.numero,     # Depois por prioridade (maior primeiro)
            p.chegada                 # Por fim, por ordem de chegada
        ))

        ultimo_processo = processo_atual

    return finalizar_metricas(total_espera, total_execucao, len(processos), Algoritmo.HERANCA_DE_PRIORIDADE.nome_exibicao)

from control.algoritmos._base import avancar_tempo_para_chegada, trocar_contexto, selecionar_proximo, finalizar_metricas
from control.algoritmos.nomes import Algoritmo


def sjf(processos, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.duracao))

    while processos_ordenados:
        tempo_atual = avancar_tempo_para_chegada(processos_ordenados[0], tempo_atual)
        processo_atual = selecionar_proximo(processos_ordenados, tempo_atual, lambda p: p.duracao)

        tempo_atual = trocar_contexto(ultimo_processo, processo_atual, tempo_atual, ctx_time, exigir_troca=False)

        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + processo_atual.duracao)

        total_execucao += processo_atual.get_turnaround()
        total_espera += processo_atual.get_espera()

        processos_ordenados.remove(processo_atual)
        ultimo_processo = processo_atual

    return finalizar_metricas(total_espera, total_execucao, len(processos), Algoritmo.SJF.nome_exibicao)

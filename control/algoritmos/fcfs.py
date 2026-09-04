from control.algoritmos._base import avancar_tempo_para_chegada, trocar_contexto, finalizar_metricas
from control.algoritmos.nomes import Algoritmo


def fcfs(processos, ctx_time=0.5):
    tempo_atual = 0
    total_execucao = 0
    total_espera = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)

    for processo in processos_ordenados:
        tempo_atual = avancar_tempo_para_chegada(processo, tempo_atual)
        tempo_atual = trocar_contexto(ultimo_processo, processo, tempo_atual, ctx_time, exigir_troca=False)

        tempo_atual += processo.adicionar_processamento(tempo_atual, tempo_atual + processo.duracao)

        total_execucao += processo.get_turnaround()
        total_espera += processo.get_espera()

        ultimo_processo = processo

    return finalizar_metricas(total_espera, total_execucao, len(processos), Algoritmo.FCFS.nome_exibicao)

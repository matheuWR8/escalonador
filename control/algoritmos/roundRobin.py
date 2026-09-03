from control.algoritmos._base import trocar_contexto, finalizar_metricas
from control.algoritmos.nomes import Algoritmo


def round_robin(processos, quantum=2, ctx_time=0.5):
    if quantum <= 0:
        raise ValueError("O quantum deve ser maior que zero.")

    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)
    fila = []

    while processos_ordenados:
        for processo in processos_ordenados:
            if processo.chegada <= tempo_atual and processo not in fila:
                fila.append(processo)

        if not fila:
            tempo_atual += 1
            continue

        processo_atual = fila.pop(0)
        processos_ordenados.remove(processo_atual)

        tempo_atual = trocar_contexto(ultimo_processo, processo_atual, tempo_atual, ctx_time, exigir_troca=True)

        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + quantum)

        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
        else:
            processos_ordenados.append(processo_atual)

        ultimo_processo = processo_atual

    return finalizar_metricas(total_espera, total_execucao, len(processos), Algoritmo.ROUND_ROBIN.nome_exibicao)

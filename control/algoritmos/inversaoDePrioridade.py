from control.algoritmos._base import avancar_tempo_para_chegada, trocar_contexto, finalizar_metricas
from control.algoritmos.nomes import Algoritmo


def _pode_preemptar_por_recurso(processo, dono_a, dono_b):
    if processo.prioridade.recurso == 'A':
        return dono_a is None or processo == dono_a
    return dono_b is None or processo == dono_b


def inversao_prioridade(processos, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    processo_with_recurso_a = None
    processo_with_recurso_b = None

    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade.numero))

    while processos_ordenados:
        processo_atual = processos_ordenados[0]
        if processo_atual.prioridade.recurso == 'A':
            processo_with_recurso_a = processo_atual
        else:
            processo_with_recurso_b = processo_atual

        tempo_atual = avancar_tempo_para_chegada(processo_atual, tempo_atual)

        for processo in processos_ordenados:
            if (processo.chegada <= tempo_atual
                    and processo.prioridade.numero > processo_atual.prioridade.numero
                    and _pode_preemptar_por_recurso(processo, processo_with_recurso_a, processo_with_recurso_b)):
                processo_atual = processo

        tempo_atual = trocar_contexto(ultimo_processo, processo_atual, tempo_atual, ctx_time, exigir_troca=True)

        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)

        if processo_atual.tempo_restante == 0:
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            if processo_atual.prioridade.recurso == 'A':
                processo_with_recurso_a = None
            else:
                processo_with_recurso_b = None
            processos_ordenados.remove(processo_atual)

        ultimo_processo = processo_atual

    return finalizar_metricas(total_espera, total_execucao, len(processos), Algoritmo.INVERSAO_DE_PRIORIDADE.nome_exibicao)

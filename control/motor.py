from control.algoritmos._base import (
    avancar_tempo_para_chegada,
    selecionar_proximo,
    trocar_contexto_padrao,
    despachar_com_quantum,
)


def simular(processos, politica, quantum, ctx_time):
    if politica.usa_quantum:
        total_espera, total_execucao = _simular_round_robin(processos, quantum, ctx_time)
    else:
        total_espera, total_execucao = _simular_por_chave(
            processos, politica.chave_selecao, politica.preemptivo, ctx_time
        )

    quantidade = len(processos)
    nome = politica.algoritmo.nome_exibicao
    return total_espera / quantidade, total_execucao / quantidade, nome


def _simular_por_chave(processos, chave_selecao, preemptivo, ctx_time):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    pendentes = list(processos)

    while pendentes:
        proxima_chegada = min(pendentes, key=lambda p: p.chegada)
        tempo_atual = avancar_tempo_para_chegada(proxima_chegada, tempo_atual)

        processo_atual = selecionar_proximo(pendentes, tempo_atual, chave_selecao)
        tempo_atual = trocar_contexto_padrao(ultimo_processo, processo_atual, tempo_atual, ctx_time)

        duracao_fatia = 1 if preemptivo else processo_atual.duracao
        fim = tempo_atual + min(duracao_fatia, processo_atual.tempo_restante)
        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, fim)

        ultimo_processo = processo_atual

        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
            pendentes.remove(processo_atual)

    return total_espera, total_execucao


def _simular_round_robin(processos, quantum, ctx_time):
    if quantum is None or quantum <= 0:
        raise ValueError("O quantum deve ser maior que zero.")

    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    pendentes = sorted(processos, key=lambda p: (p.chegada, p.id))
    fila = []

    while pendentes:
        for processo in pendentes:
            if processo.chegada <= tempo_atual and processo not in fila:
                fila.append(processo)

        if not fila:
            tempo_atual = min(p.chegada for p in pendentes)
            continue

        processo_atual = fila.pop(0)
        pendentes.remove(processo_atual)

        tempo_atual = despachar_com_quantum(ultimo_processo, processo_atual, tempo_atual, quantum, ctx_time)

        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
        else:
            pendentes.append(processo_atual)

        ultimo_processo = processo_atual

    return total_espera, total_execucao

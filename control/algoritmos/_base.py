def avancar_tempo_para_chegada(processo, tempo_atual):
    return processo.chegada if processo.chegada > tempo_atual else tempo_atual


def trocar_contexto(ultimo_processo, processo_atual, tempo_atual, ctx_time, exigir_troca=True):
    if ultimo_processo is None or ctx_time <= 0:
        return tempo_atual
    if exigir_troca and ultimo_processo == processo_atual:
        return tempo_atual

    ctx_duracao = ultimo_processo.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
    return tempo_atual + ctx_duracao


def selecionar_proximo(processos_ordenados, tempo_atual, chave):
    candidatos = [p for p in processos_ordenados if p.chegada <= tempo_atual]
    return min(candidatos, key=chave) if candidatos else processos_ordenados[0]


def finalizar_metricas(total_espera, total_execucao, quantidade, nome):
    return total_espera / quantidade, total_execucao / quantidade, nome

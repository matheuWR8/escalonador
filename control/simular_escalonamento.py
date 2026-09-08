import copy

from control.algoritmos.nomes import Algoritmo
from control.algoritmos.inversaoDePrioridade import inversao_prioridade
from control.algoritmos.herancaDePrioridade import heranca_prioridade
from control.motor import simular as simular_motor
from control.politicas import POLITICAS

_DISPATCH = {
    Algoritmo.FCFS.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.FCFS], q, c),
    Algoritmo.SJF.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.SJF], q, c),
    Algoritmo.ROUND_ROBIN.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.ROUND_ROBIN], q, c),
    Algoritmo.SRTF.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.SRTF], q, c),
    Algoritmo.PRIORIDADE_COOPERATIVO.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.PRIORIDADE_COOPERATIVO], q, c),
    Algoritmo.PRIORIDADE_PREEMPTIVO.value: lambda p, q, c: simular_motor(p, POLITICAS[Algoritmo.PRIORIDADE_PREEMPTIVO], q, c),
    Algoritmo.INVERSAO_DE_PRIORIDADE.value: lambda p, q, c: inversao_prioridade(p, c),
    Algoritmo.HERANCA_DE_PRIORIDADE.value: lambda p, q, c: heranca_prioridade(p, c),
}


def simular_escalonamento(processos, algoritmo, quantum_entry=0, ctx_time=0.5):
    if not processos:
        raise ValueError("Nenhum processo foi adicionado.")

    executar = _DISPATCH.get(algoritmo)
    if executar is None:
        raise ValueError("Selecione um algoritmo válido.")

    quantum = None
    if algoritmo == Algoritmo.ROUND_ROBIN.value:
        quantum = int(quantum_entry)
        if quantum <= 0:
            raise ValueError("O quantum do Round Robin deve ser maior que zero.")

    processos_simulados = copy.deepcopy(processos)
    media_espera, media_execucao, nome_processo = executar(processos_simulados, quantum, float(ctx_time))

    return media_execucao, media_espera, nome_processo, processos_simulados

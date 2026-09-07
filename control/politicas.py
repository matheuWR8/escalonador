from dataclasses import dataclass
from typing import Callable

from control.algoritmos._base import chave_desempate
from control.algoritmos.nomes import Algoritmo


@dataclass(frozen=True)
class Politica:
    algoritmo: Algoritmo
    chave_selecao: Callable
    preemptivo: bool
    usa_quantum: bool = False


def _chave_sjf(p):
    return (p.duracao, *chave_desempate(p))


def _chave_srtf(p):
    return (p.tempo_restante, *chave_desempate(p))


def _chave_prioridade(p):
    return (-p.prioridade.numero, *chave_desempate(p))


POLITICAS = {
    Algoritmo.FCFS: Politica(Algoritmo.FCFS, chave_desempate, preemptivo=False),
    Algoritmo.SJF: Politica(Algoritmo.SJF, _chave_sjf, preemptivo=False),
    Algoritmo.SRTF: Politica(Algoritmo.SRTF, _chave_srtf, preemptivo=True),
    Algoritmo.ROUND_ROBIN: Politica(Algoritmo.ROUND_ROBIN, chave_desempate, preemptivo=True, usa_quantum=True),
    Algoritmo.PRIORIDADE_COOPERATIVO: Politica(Algoritmo.PRIORIDADE_COOPERATIVO, _chave_prioridade, preemptivo=False),
    Algoritmo.PRIORIDADE_PREEMPTIVO: Politica(Algoritmo.PRIORIDADE_PREEMPTIVO, _chave_prioridade, preemptivo=True),
}

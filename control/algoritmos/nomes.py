from enum import Enum


class Algoritmo(Enum):
    FCFS = 1
    SJF = 2
    ROUND_ROBIN = 3
    SRTF = 4
    PRIORIDADE_COOPERATIVO = 5
    PRIORIDADE_PREEMPTIVO = 6
    INVERSAO_DE_PRIORIDADE = 7
    HERANCA_DE_PRIORIDADE = 8

    @property
    def nome_exibicao(self):
        return {
            Algoritmo.FCFS: "FCFS",
            Algoritmo.SJF: "SJF",
            Algoritmo.ROUND_ROBIN: "Round Robin",
            Algoritmo.SRTF: "SRTF",
            Algoritmo.PRIORIDADE_COOPERATIVO: "Prioridade Cooperativo",
            Algoritmo.PRIORIDADE_PREEMPTIVO: "Prioridade Preemptivo",
            Algoritmo.INVERSAO_DE_PRIORIDADE: "Inversão de Prioridade",
            Algoritmo.HERANCA_DE_PRIORIDADE: "Herança de Prioridade",
        }[self]

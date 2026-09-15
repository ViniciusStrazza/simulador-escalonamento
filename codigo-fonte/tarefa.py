class Tarefa:
    def __init__(self, id, ingresso, tp, prioridade=1):
        self.id = id
        self.ingresso = ingresso
        self.tp = tp
        self.prioridade = prioridade
        self.executado = 0
        self.conclusao = None
        self.primeira_exec = None

    def restante(self):
        return self.tp - self.executado

    def terminou(self):
        return self.executado >= self.tp

    def tt(self):
        return self.conclusao - self.ingresso

    def tw(self):
        return self.tt() - self.tp

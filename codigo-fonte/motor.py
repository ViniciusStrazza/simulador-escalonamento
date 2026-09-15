def simular(tarefas, politica=None, preemptivo=False, ttc=0, tq=None):
    relogio = 0
    atual = None
    ultima = None
    trocas = 0
    fatia = 0
    linha_do_tempo = []
    fila = []
    ingressadas = []

    def enfileirar():
        novas = [t for t in tarefas
                 if t.ingresso <= relogio and t not in ingressadas]
        novas.sort(key=lambda t: (t.ingresso, t.id))
        for t in novas:
            ingressadas.append(t)
            fila.append(t)

    while not all(t.terminou() for t in tarefas):
        enfileirar()

        if tq is None:
            prontas = [t for t in tarefas
                       if t.ingresso <= relogio and not t.terminou()]
            if not prontas:
                relogio = min(t.ingresso for t in tarefas if not t.terminou())
                continue
            if atual is None or atual.terminou() or preemptivo:
                atual = politica(prontas)
        else:
            if atual is None:
                if not fila:
                    relogio = min(t.ingresso for t in tarefas
                                  if not t.terminou())
                    continue
                atual = fila.pop(0)
                fatia = tq if atual is ultima else tq - ttc

        if atual is not ultima:
            trocas += 1
            relogio += ttc
            ultima = atual

        if atual.primeira_exec is None:
            atual.primeira_exec = relogio - atual.ingresso

        linha_do_tempo.append((relogio, atual.id))
        atual.executado += 1
        relogio += 1
        fatia -= 1

        if atual.terminou():
            atual.conclusao = relogio
            atual = None
        elif tq is not None and fatia == 0:
            enfileirar()
            fila.append(atual)
            atual = None

    return {"trocas": trocas, "linha_do_tempo": linha_do_tempo, "fim": relogio}


def eficiencia(tq, ttc):
    if tq is None:
        return None
    return tq / (tq + ttc)
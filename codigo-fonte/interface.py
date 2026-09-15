import tkinter as tk
from tkinter import messagebox

from tarefa import Tarefa
from motor import simular, eficiencia
from comparacao import ALGORITMOS
from gerador import sortear_dados
from validacao import EntradaInvalida, inteiro, validar_quantum, ler_tarefa

MONO = ("Consolas", 10)


class Janela:
    def __init__(self, raiz):
        self.raiz = raiz
        self.dados = []
        raiz.title("Simulador de Escalonamento de Tarefas")
        raiz.geometry("760x680")

        self._montar_entrada()
        self._montar_lista()
        self._montar_parametros()
        self._montar_algoritmos()
        self._montar_resultado()

    # ------------------------------------------------ montagem da janela

    def _montar_entrada(self):
        caixa = tk.LabelFrame(self.raiz, text="Definir uma tarefa", padx=8, pady=6)
        caixa.pack(fill="x", padx=10, pady=6)

        rotulos = ["Ingresso", "Duracao (tp)", "Prioridade",
                   "R: inicio", "R: duracao"]
        self.campos = {}
        for coluna, rotulo in enumerate(rotulos):
            tk.Label(caixa, text=rotulo).grid(row=0, column=coluna, padx=4)
            campo = tk.Entry(caixa, width=11)
            campo.grid(row=1, column=coluna, padx=4)
            self.campos[rotulo] = campo

        tk.Label(caixa, text="(os dois ultimos campos sao opcionais: "
                             "deixe vazios se a tarefa nao usa o recurso)",
                 fg="gray30").grid(row=2, column=0, columnspan=5, pady=(6, 0))

        tk.Button(caixa, text="Adicionar tarefa",
                  command=self.adicionar).grid(row=1, column=5, padx=8)

    def _montar_lista(self):
        caixa = tk.LabelFrame(self.raiz, text="Conjunto de tarefas",
                              padx=8, pady=6)
        caixa.pack(fill="x", padx=10, pady=6)

        self.lista = tk.Listbox(caixa, height=6, font=MONO)
        self.lista.pack(side="left", fill="both", expand=True)

        botoes = tk.Frame(caixa)
        botoes.pack(side="right", padx=8)
        tk.Button(botoes, text="Remover selecionada", width=20,
                  command=self.remover).pack(pady=2)
        tk.Button(botoes, text="Limpar tudo", width=20,
                  command=self.limpar).pack(pady=2)

        sorteio = tk.Frame(botoes)
        sorteio.pack(pady=(10, 2))
        tk.Label(sorteio, text="Quantidade:").pack(side="left")
        self.e_quantidade = tk.Entry(sorteio, width=5)
        self.e_quantidade.insert(0, "5")
        self.e_quantidade.pack(side="left", padx=4)
        tk.Button(botoes, text="Sortear tarefas", width=20,
                  command=self.sortear).pack(pady=2)

    def _montar_parametros(self):
        caixa = tk.LabelFrame(self.raiz, text="Parametros de tempo",
                              padx=8, pady=6)
        caixa.pack(fill="x", padx=10, pady=6)

        tk.Label(caixa, text="Quantum (tq):").grid(row=0, column=0, sticky="e")
        self.e_quantum = tk.Entry(caixa, width=8)
        self.e_quantum.insert(0, "2")
        self.e_quantum.grid(row=0, column=1, padx=6)

        tk.Label(caixa, text="Custo da troca (ttc):").grid(row=0, column=2,
                                                           sticky="e")
        self.e_custo = tk.Entry(caixa, width=8)
        self.e_custo.insert(0, "0")
        self.e_custo.grid(row=0, column=3, padx=6)

        tk.Label(caixa, text="Passo do envelhecimento (alfa):").grid(
            row=0, column=4, sticky="e")
        self.e_alfa = tk.Entry(caixa, width=8)
        self.e_alfa.insert(0, "0")
        self.e_alfa.grid(row=0, column=5, padx=6)

    def _montar_algoritmos(self):
        caixa = tk.LabelFrame(self.raiz, text="Algoritmo e protocolo",
                              padx=8, pady=6)
        caixa.pack(fill="x", padx=10, pady=6)

        self.algoritmo = tk.StringVar(value="FCFS")
        for i, nome in enumerate(ALGORITMOS):
            tk.Radiobutton(caixa, text=nome, variable=self.algoritmo,
                           value=nome).grid(row=i // 3, column=i % 3,
                                            sticky="w", padx=6)

        tk.Label(caixa, text="Correcao de inversao:").grid(
            row=0, column=3, columnspan=3, sticky="w", padx=(20, 0))
        self.protocolo = tk.StringVar(value="nenhum")
        for i, (texto, valor) in enumerate([("Nenhuma", "nenhum"),
                                            ("Heranca", "heranca"),
                                            ("Teto", "teto")]):
            tk.Radiobutton(caixa, text=texto, variable=self.protocolo,
                           value=valor).grid(row=1, column=3 + i, sticky="w",
                                             padx=(20 if i == 0 else 6, 6))

        tk.Button(caixa, text="Simular", width=16, command=self.rodar).grid(
            row=2, column=0, columnspan=6, pady=(10, 0))

    def _montar_resultado(self):
        caixa = tk.LabelFrame(self.raiz, text="Resultados", padx=8, pady=6)
        caixa.pack(fill="both", expand=True, padx=10, pady=6)
        self.saida = tk.Text(caixa, height=14, font=MONO, wrap="none")
        self.saida.pack(fill="both", expand=True)

    # ------------------------------------------------------------ acoes

    def adicionar(self):
        try:
            dado = ler_tarefa(
                len(self.dados) + 1,
                self.campos["Ingresso"].get(),
                self.campos["Duracao (tp)"].get(),
                self.campos["Prioridade"].get(),
                self.campos["R: inicio"].get(),
                self.campos["R: duracao"].get())
        except EntradaInvalida as erro:
            messagebox.showerror("Valor invalido", str(erro))
            return

        self.dados.append(dado)
        for campo in self.campos.values():
            campo.delete(0, tk.END)
        self.redesenhar_lista()

    def remover(self):
        escolha = self.lista.curselection()
        if not escolha:
            messagebox.showinfo("Remover",
                                "Selecione uma tarefa na lista primeiro.")
            return
        del self.dados[escolha[0]]
        self.dados = [(i + 1,) + d[1:] for i, d in enumerate(self.dados)]
        self.redesenhar_lista()

    def limpar(self):
        self.dados = []
        self.redesenhar_lista()

    def sortear(self):
        try:
            n = inteiro(self.e_quantidade.get(), "Quantidade", 1)
        except EntradaInvalida as erro:
            messagebox.showerror("Valor invalido", str(erro))
            return
        self.dados = sortear_dados(n)
        self.redesenhar_lista()

    def redesenhar_lista(self):
        self.lista.delete(0, tk.END)
        for id, ingresso, tp, prioridade, secao in self.dados:
            texto = (f"t{id}  ingresso {ingresso:>3}   tp {tp:>3}   "
                     f"prioridade {prioridade:>3}")
            if secao is not None:
                texto += f"   usa R em [{secao[0]}, {secao[0] + secao[1]})"
            self.lista.insert(tk.END, texto)

    def rodar(self):
        try:
            if not self.dados:
                raise EntradaInvalida(
                    "Adicione ou sorteie ao menos uma tarefa.")

            nome = self.algoritmo.get()
            config = ALGORITMOS[nome]

            ttc = inteiro(self.e_custo.get(), "Custo da troca", 0)
            alfa = inteiro(self.e_alfa.get(), "Passo do envelhecimento", 0)

            tq = None
            if config["usa_quantum"]:
                tq = inteiro(self.e_quantum.get(), "Quantum", 1)
                validar_quantum(tq, ttc)

            tarefas = [Tarefa(*d) for d in self.dados]
            resultado = simular(
                tarefas,
                politica=config["politica"],
                preemptivo=config["preemptivo"],
                ttc=ttc,
                tq=tq,
                protocolo=self.protocolo_escolhido(),
                alfa=alfa)

            self.escrever(nome, tarefas, resultado, tq, ttc)

        except EntradaInvalida as erro:
            messagebox.showerror("Valor invalido", str(erro))
        except Exception as erro:
            messagebox.showerror(
                "Erro na simulacao",
                f"Ocorreu um erro inesperado:\n\n{erro}\n\n"
                f"A janela continua aberta.")

    def protocolo_escolhido(self):
        escolha = self.protocolo.get()
        return None if escolha == "nenhum" else escolha

    def escrever(self, nome, tarefas, resultado, tq, ttc):
        n = len(tarefas)
        prot = self.protocolo_escolhido()
        linhas = [f"Algoritmo: {nome}      ttc = {ttc}"
                  + (f"      tq = {tq}" if tq is not None else "")
                  + (f"      protocolo: {prot}" if prot else ""),
                  ""]

        linhas.append(f"{'tarefa':<8}{'tt':>8}{'tp':>8}{'tw':>8}"
                      f"{'1a exec':>10}")
        linhas.append("-" * 42)
        for t in tarefas:
            linhas.append(f"t{t.id:<7}{t.tt():>8}{t.tp:>8}{t.tw():>8}"
                          f"{t.primeira_exec:>10}")
        linhas.append("-" * 42)
        linhas.append(f"{'media':<8}"
                      f"{sum(t.tt() for t in tarefas) / n:>8.2f}"
                      f"{sum(t.tp for t in tarefas) / n:>8.2f}"
                      f"{sum(t.tw() for t in tarefas) / n:>8.2f}"
                      f"{sum(t.primeira_exec for t in tarefas) / n:>10.2f}")
        linhas.append("")
        linhas.append(f"Trocas de contexto: {resultado['trocas']}")

        e = eficiencia(tq, ttc)
        if e is None:
            linhas.append("Eficiencia: nao definida "
                          "(o algoritmo nao usa quantum)")
        else:
            linhas.append(f"Eficiencia: {tq}/({tq} + {ttc}) = {e:.3f}")

        self.saida.delete("1.0", tk.END)
        self.saida.insert("1.0", "\n".join(linhas))


def criar_janela():
    try:
        raiz = tk.Tk()
        Janela(raiz)
        raiz.mainloop()
    except Exception as erro:
        try:
            messagebox.showerror("Erro", f"O programa nao pudo abrir:\n\n{erro}")
        except Exception:
            print("Erro ao abrir o programa:", erro)
            input("Pressione Enter para fechar...")

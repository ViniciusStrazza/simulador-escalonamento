# Simulador de Escalonamento de Tarefas

Projeto prático da disciplina de Sistemas Operacionais, ministrada por
<!-- TODO: nome do professor -->. Semestre <!-- TODO: ano/semestre -->.

## Como executar

Clique duas vezes em `Simulador.exe`, na raiz desta pasta.
Não é necessário instalar nada nem digitar comando algum.

<!-- Esta seção vem propositalmente antes de todas as outras: é a primeira
     coisa que quem avalia vai procurar. Não a mova para baixo. -->

## Autoria

- Vinicius Strazza — [@ViniciusStrazza](https://github.com/ViniciusStrazza)
- <!-- TODO: integrante 2 — @usuario -->
- <!-- TODO: integrante 3 — @usuario -->

## Descrição

Simulador de escalonamento de tarefas em um processador único, com tempo
discreto. Implementa os seis algoritmos estudados em sala — FCFS, SJF, SRTF,
Round-Robin, prioridade cooperativa e prioridade preemptiva — e apresenta,
por tarefa e em média, o tempo de execução, o tempo de processamento, o tempo
de espera e o tempo até a primeira execução.

O simulador trata recursos de uso exclusivo e reproduz o fenômeno da inversão
de prioridades, com os dois protocolos de correção estudados: herança de
prioridade e teto de prioridade. Implementa também o envelhecimento como
tratamento da inanição sob prioridade cooperativa.

## Requisitos de ambiente

- Windows <!-- TODO: confirmar versões testadas -->
- Nenhuma biblioteca externa é necessária para executar o `Simulador.exe`.

Para executar a partir do código-fonte:

- Python <!-- TODO: versão -->
- `tkinter` (acompanha a instalação padrão do Python)
- <!-- TODO: demais bibliotecas, se houver -->

```bash
cd codigo-fonte
python main.py
```

## Estrutura do repositório

```
simulador-escalonamento/
|-- README.md              este arquivo
|-- Simulador.exe          programa pronto para executar (duplo clique)
|-- codigo-fonte/          o programa em si
|-- cenarios/              conjuntos de tarefas gravados, em JSON
|-- testes/                verificação automatizada dos cenários de referência
|-- docs/                  tutoriais e documentação técnica
'-- documentos/            enunciado e guias da disciplina
```

## Arquivos de código

<!-- TODO: preencher conforme os módulos forem criados. Uma linha por arquivo,
     dizendo o que ele faz. -->

| Arquivo | O que faz |
|---|---|
| `codigo-fonte/main.py` | Ponto de entrada. Abre a janela do programa. |
| | |

## Funcionalidades

<!-- TODO: marcar conforme implementado, e indicar o arquivo. -->

| Requisito | O que faz | Onde |
|---|---|---|
| R1 | Os seis algoritmos de escalonamento | |
| R2 | Entrada de tarefas, sorteio, gravar e recarregar | |
| R3 | Métricas por tarefa e em média | |
| R4 | Quantum, custo da troca de contexto e eficiência | |
| R5 | Recurso de uso exclusivo e inversão de prioridades | |
| R6 | Herança de prioridade | |
| R7 | Teto de prioridade | |
| R8 | Envelhecimento | |
| R9 | Gerador de cenários e comparação por lote | |
| R10 | Execução por duplo clique | `Simulador.exe` |

## Documentação

- [Tutorial de execução](./docs/tutorial_execucao.pdf)
- [Tutorial de uso](./docs/tutorial_uso.pdf)
- [Documentação técnica](./docs/documentacao_projeto.pdf)

## Por onde começar

1. Abra o programa e siga o tutorial de execução;
2. Reproduza um cenário de exemplo pelo tutorial de uso;
3. Consulte a documentação técnica para entender o funcionamento interno.

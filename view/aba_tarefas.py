import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from control import carregar_cenario, salvar_cenario, sortear_tarefas
from model import Processo
from model.prioridade import Prioridade


def construir(notebook, estado):
    frame = ttk.Frame(notebook)

    form_frame = ttk.Frame(frame)
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Chegada:").grid(row=0, column=0, padx=5)
    entrada_chegada = ttk.Entry(form_frame, width=10, justify="center")
    entrada_chegada.grid(row=1, column=0, padx=5)

    ttk.Label(form_frame, text="Duração:").grid(row=0, column=1, padx=5)
    entrada_duracao = ttk.Entry(form_frame, width=10, justify="center")
    entrada_duracao.grid(row=1, column=1, padx=5)

    ttk.Label(form_frame, text="Prioridade:").grid(row=0, column=2, padx=5)
    entrada_prioridade = ttk.Entry(form_frame, width=10, justify="center")
    entrada_prioridade.grid(row=1, column=2, padx=5)

    colunas = ("id", "chegada", "duracao", "prioridade")
    tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=10)
    for col, titulo in zip(colunas, ("ID", "Chegada", "Duração", "Prioridade")):
        tabela.heading(col, text=titulo)
        tabela.column(col, anchor="center", width=90)
    tabela.pack(padx=10, pady=10, fill="x")

    def atualizar_tabela():
        tabela.delete(*tabela.get_children())
        for p in estado.tarefas:
            tabela.insert("", "end", iid=str(p.id), values=(p.id, p.chegada, p.duracao, p.prioridade.numero))

    def limpar_formulario():
        entrada_chegada.delete(0, tk.END)
        entrada_duracao.delete(0, tk.END)
        entrada_prioridade.delete(0, tk.END)

    def adicionar():
        try:
            chegada = int(entrada_chegada.get())
            duracao = int(entrada_duracao.get())
            prioridade_num = int(entrada_prioridade.get())
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos. Use apenas números inteiros.")
            return

        try:
            novo_id = max((p.id for p in estado.tarefas), default=0) + 1
            processo = Processo(novo_id, chegada, duracao, Prioridade(prioridade_num))
            estado.tarefas.append(processo)
            atualizar_tabela()
            limpar_formulario()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def tarefa_selecionada():
        selecionados = tabela.selection()
        if not selecionados:
            return None
        id_selecionado = int(selecionados[0])
        return next((p for p in estado.tarefas if p.id == id_selecionado), None)

    def remover():
        selecionados = tabela.selection()
        if not selecionados:
            return
        ids = {int(iid) for iid in selecionados}
        estado.tarefas[:] = [p for p in estado.tarefas if p.id not in ids]
        atualizar_tabela()

    def editar():
        processo = tarefa_selecionada()
        if processo is None:
            return
        entrada_chegada.delete(0, tk.END)
        entrada_chegada.insert(0, processo.chegada)
        entrada_duracao.delete(0, tk.END)
        entrada_duracao.insert(0, processo.duracao)
        entrada_prioridade.delete(0, tk.END)
        entrada_prioridade.insert(0, processo.prioridade.numero)
        estado.tarefas.remove(processo)
        atualizar_tabela()

    def limpar_tudo():
        if estado.tarefas and messagebox.askyesno("Confirmar", "Remover todas as tarefas cadastradas?"):
            estado.tarefas.clear()
            atualizar_tabela()

    def abrir_sorteio():
        n = simpledialog.askinteger("Sortear tarefas", "Quantas tarefas sortear?", minvalue=1, parent=frame)
        if not n:
            return
        try:
            novas = sortear_tarefas(n)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        estado.tarefas.clear()
        estado.tarefas.extend(novas)
        atualizar_tabela()

    def salvar():
        if not estado.tarefas:
            messagebox.showerror("Erro", "Nenhuma tarefa para salvar.")
            return
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("Cenário JSON", "*.json")], parent=frame
        )
        if not caminho:
            return
        try:
            salvar_cenario(estado.tarefas, caminho)
        except OSError as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o cenário: {e}")

    def carregar():
        caminho = filedialog.askopenfilename(filetypes=[("Cenário JSON", "*.json")], parent=frame)
        if not caminho:
            return
        try:
            novas = carregar_cenario(caminho)
        except (ValueError, OSError) as e:
            messagebox.showerror("Erro", str(e))
            return
        estado.tarefas.clear()
        estado.tarefas.extend(novas)
        atualizar_tabela()

    botoes_edicao = ttk.Frame(frame)
    botoes_edicao.pack(pady=5)
    ttk.Button(botoes_edicao, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=4)
    ttk.Button(botoes_edicao, text="Editar selecionada", command=editar).grid(row=0, column=1, padx=4)
    ttk.Button(botoes_edicao, text="Remover selecionada(s)", command=remover).grid(row=0, column=2, padx=4)
    ttk.Button(botoes_edicao, text="Limpar tudo", command=limpar_tudo).grid(row=0, column=3, padx=4)

    botoes_cenario = ttk.Frame(frame)
    botoes_cenario.pack(pady=5)
    ttk.Button(botoes_cenario, text="Sortear tarefas...", command=abrir_sorteio).grid(row=0, column=0, padx=4)
    ttk.Button(botoes_cenario, text="Salvar cenário...", command=salvar).grid(row=0, column=1, padx=4)
    ttk.Button(botoes_cenario, text="Carregar cenário...", command=carregar).grid(row=0, column=2, padx=4)

    atualizar_tabela()
    return frame

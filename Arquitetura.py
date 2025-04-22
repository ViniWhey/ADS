import sqlite3
import tkinter as tk
from tkinter import messagebox

# Sistema de banco de dados
class Sistema:
    def __init__(self, nome='estoque.db'):
        self.conn = sqlite3.connect(nome)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                localizacao TEXT
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                status TEXT DEFAULT 'Pendente'
            )""")
        self.conn.commit()

    def adicionar_produto(self, nome, categoria, quantidade, preco, localizacao):
        self.cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
        if self.cursor.fetchone():
            self.cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE nome = ?", (quantidade, nome))
        else:
            self.cursor.execute("INSERT INTO produtos (nome, categoria, quantidade, preco, localizacao) VALUES (?, ?, ?, ?, ?)",
                                (nome, categoria, quantidade, preco, localizacao))
        self.conn.commit()

    def registrar_saida_produto(self, nome, quantidade):
        self.cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome,))
        result = self.cursor.fetchone()
        if result:
            estoque_atual = result[0]
            if estoque_atual >= quantidade:
                self.cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE nome = ?", (quantidade, nome))
                self.conn.commit()
                return True
            else:
                return False
        return None

    def obter_relatorio(self):
        self.cursor.execute("SELECT nome, categoria, quantidade, preco, localizacao FROM produtos")
        return self.cursor.fetchall()

    def fechar(self):
        self.conn.close()

# Telas
class TelaInicial:
    def __init__(self, banco):
        self.banco = banco
        self.root = tk.Tk()
        self.root.title("Sistema de Estoque - Selecione o Tipo de Usuário")

        tk.Label(self.root, text="Escolha o tipo de usuário:").pack(pady=10)

        tk.Button(self.root, text="Gerente de Setor", width=25, command=lambda: self.abrir_login("Gerente de Setor")).pack(pady=5)
        tk.Button(self.root, text="Estoquista", width=25, command=lambda: self.abrir_login("Estoquista")).pack(pady=5)
        tk.Button(self.root, text="Usuário", width=25, command=lambda: self.abrir_login("Usuário")).pack(pady=5)
        tk.Button(self.root, text="Cadastrar Novo Usuário", width=25, command=self.abrir_cadastro).pack(pady=10)

        self.root.mainloop()

    def abrir_login(self, tipo_usuario):
        self.root.destroy()
        TelaLogin(self.banco, tipo_usuario)

    def abrir_cadastro(self):
        CadastroUsuario(self.banco)

class TelaLogin:
    def __init__(self, banco, tipo_usuario):
        self.banco = banco
        self.tipo_usuario = tipo_usuario
        self.root = tk.Tk()
        self.root.title(f"Login - {tipo_usuario}")

        tk.Label(self.root, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.root, text="Senha:").grid(row=1, column=0)
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.verificar_login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Voltar", command=self.voltar).grid(row=3, column=0, columnspan=2)

        self.root.mainloop()

    def verificar_login(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        self.banco.cursor.execute("SELECT tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        usuario = self.banco.cursor.fetchone()
        if usuario and usuario[0] == self.tipo_usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {nome} ({usuario[0]})!")
            self.root.destroy()
            SistemaEstoque(self.banco, self.tipo_usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos ou tipo incorreto.")

    def voltar(self):
        self.root.destroy()
        TelaInicial(self.banco)

class CadastroUsuario:
    def __init__(self, banco):
        self.banco = banco
        self.window = tk.Toplevel()
        self.window.title("Cadastro de Novo Usuário")

        tk.Label(self.window, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.window)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.window, text="Senha:").grid(row=1, column=0)
        self.entry_senha = tk.Entry(self.window, show="*")
        self.entry_senha.grid(row=1, column=1)

        tk.Label(self.window, text="Confirmar Senha:").grid(row=2, column=0)
        self.entry_confirmar = tk.Entry(self.window, show="*")
        self.entry_confirmar.grid(row=2, column=1)

        tk.Label(self.window, text="Tipo de Usuário:").grid(row=3, column=0)
        self.tipo_var = tk.StringVar(value="Gerente de Setor")
        tipos = ["Gerente de Setor", "Estoquista", "Usuário"]
        tk.OptionMenu(self.window, self.tipo_var, *tipos).grid(row=3, column=1)

        tk.Button(self.window, text="Cadastrar", command=self.cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

    def cadastrar(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()
        tipo = self.tipo_var.get()

        if not nome or not senha or not confirmar:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        self.banco.cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
        if self.banco.cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        self.banco.cursor.execute("INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)", (nome, senha, tipo))
        self.banco.conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.window.destroy()

# Interface principal
class SistemaEstoque:
    def __init__(self, banco, tipo_usuario):
        self.banco = banco
        self.tipo_usuario = tipo_usuario
        self.root = tk.Tk()
        self.root.title(f"Sistema - {tipo_usuario}")

        if tipo_usuario == "Estoquista":
            self.interface_estoquista()
        elif tipo_usuario == "Usuário":
            self.interface_usuario()
        elif tipo_usuario == "Gerente de Setor":
            self.interface_gerente()

        tk.Button(self.root, text="Voltar", command=self.voltar).pack(pady=10)
        self.root.mainloop()

    def interface_estoquista(self):
        tk.Label(self.root, text="Produto:").pack()
        self.entry_produto = tk.Entry(self.root)
        self.entry_produto.pack()

        tk.Label(self.root, text="Quantidade:").pack()
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.pack()

        tk.Label(self.root, text="Nota Fiscal (Sim/Não):").pack()
        self.entry_nota = tk.Entry(self.root)
        self.entry_nota.pack()

        tk.Label(self.root, text="Categoria:").pack()
        self.entry_categoria = tk.Entry(self.root)
        self.entry_categoria.pack()

        tk.Label(self.root, text="Preço:").pack()
        self.entry_preco = tk.Entry(self.root)
        self.entry_preco.pack()

        tk.Label(self.root, text="Localização:").pack()
        self.entry_localizacao = tk.Entry(self.root)
        self.entry_localizacao.pack()

        tk.Button(self.root, text="Registrar Entrada", command=self.registrar_entrada).pack()
        tk.Button(self.root, text="Registrar Saída", command=self.registrar_saida).pack()
        tk.Button(self.root, text="Emitir Relatório", command=self.emitir_relatorio).pack()

    def registrar_entrada(self):
        try:
            nome = self.entry_produto.get()
            quantidade = int(self.entry_quantidade.get())
            preco = float(self.entry_preco.get())
            categoria = self.entry_categoria.get()
            localizacao = self.entry_localizacao.get()
            nota = self.entry_nota.get().lower()

            if nome and nota in ["sim", "não"]:
                self.banco.adicionar_produto(nome, categoria, quantidade, preco, localizacao)
                messagebox.showinfo("Sucesso", f"{quantidade} unidades de {nome} registradas.")
            else:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Dados inválidos!")

    def registrar_saida(self):
        nome = self.entry_produto.get()
        quantidade = self.entry_quantidade.get()
        if nome and quantidade.isdigit():
            resultado = self.banco.registrar_saida_produto(nome, int(quantidade))
            if resultado is True:
                messagebox.showinfo("Sucesso", f"Saída de {quantidade} unidades registrada.")
            elif resultado is False:
                messagebox.showerror("Erro", "Estoque insuficiente!")
            else:
                messagebox.showerror("Erro", "Produto não encontrado!")
        else:
            messagebox.showerror("Erro", "Dados inválidos!")

    def emitir_relatorio(self):
        produtos = self.banco.obter_relatorio()
        relatorio_texto = "Relatório de Estoque:\n"
        for produto in produtos:
            relatorio_texto += f"{produto[0]} | Categoria: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f} | Localização: {produto[4]}\n"
        messagebox.showinfo("Relatório", relatorio_texto)

    def interface_usuario(self):
        self.entry_produto = tk.Entry(self.root)
        self.entry_produto.pack()
        self.entry_produto.insert(0, "Produto para compra")

        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.pack()
        self.entry_quantidade.insert(0, "Quantidade")

        tk.Button(self.root, text="Solicitar Compra", command=self.solicitar_compra).pack()
        tk.Button(self.root, text="Emitir Relatório", command=self.emitir_relatorio).pack()

    def solicitar_compra(self):
        produto = self.entry_produto.get()
        quantidade = self.entry_quantidade.get()
        if produto and quantidade.isdigit():
            self.banco.cursor.execute("INSERT INTO pedidos (produto, quantidade) VALUES (?, ?)", (produto, int(quantidade)))
            self.banco.conn.commit()
            messagebox.showinfo("Sucesso", "Pedido enviado!")
        else:
            messagebox.showerror("Erro", "Dados inválidos!")

    def interface_gerente(self):
        tk.Label(self.root, text="Pedidos Pendentes").pack()
        self.lista_pedidos = tk.Listbox(self.root, width=60)
        self.lista_pedidos.pack()

        tk.Button(self.root, text="Autorizar", command=lambda: self.atualizar_status("Autorizado")).pack()
        tk.Button(self.root, text="Rejeitar", command=lambda: self.atualizar_status("Rejeitado")).pack()
        self.carregar_pedidos()

    def carregar_pedidos(self):
        self.lista_pedidos.delete(0, tk.END)
        self.banco.cursor.execute("SELECT id, produto, quantidade, status FROM pedidos WHERE status = 'Pendente'")
        for pedido in self.banco.cursor.fetchall():
            self.lista_pedidos.insert(tk.END, f"ID:{pedido[0]} | {pedido[1]} - {pedido[2]} un. | {pedido[3]}")

    def atualizar_status(self, status):
        selecao = self.lista_pedidos.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um pedido.")
            return
        item = self.lista_pedidos.get(selecao[0])
        pedido_id = int(item.split("|")[0].split(":")[1].strip())
        self.banco.cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
        self.banco.conn.commit()
        self.carregar_pedidos()
        messagebox.showinfo("Sucesso", f"Pedido {status.lower()}.")

    def voltar(self):
        self.root.destroy()
        TelaInicial(self.banco)

# Execução
if __name__ == "__main__":
    banco = Sistema()
    TelaInicial(banco)

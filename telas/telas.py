import tkinter as tk  # Importa o módulo Tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa o módulo para exibir mensagens na interface
from estoque.interface import SistemaEstoque  # Importa o sistema de estoque

# Tela inicial do sistema, onde o usuário escolhe seu tipo
class TelaInicial:
    def __init__(self, banco):
        self.banco = banco  # Guarda a instância do banco de dados
        self.root = tk.Tk()  # Cria a janela principal
        self.root.title("Sistema de Estoque - Selecione o Tipo de Usuário")  # Define o título da janela

        # Cria um frame centralizado para o conteúdo
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        # Título da tela
        tk.Label(frame, text="Escolha o tipo de usuário:", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        # Botões para seleção do tipo de usuário
        botoes = ["Gerente de Setor", "Estoquista", "Usuário"]
        for tipo in botoes:
            tk.Button(
                frame, 
                text=tipo, 
                width=25, 
                height=2, 
                font=("Arial", 10), 
                command=lambda t=tipo: self.abrir_login(t)
            ).pack(pady=5)

        # Botão para cadastrar um novo usuário
        tk.Button(
            frame, 
            text="Cadastrar Novo Usuário", 
            width=25, 
            height=2, 
            font=("Arial", 10), 
            command=self.abrir_cadastro
        ).pack(pady=10)

        # Inicia o loop da interface
        self.root.mainloop()

    def abrir_login(self, tipo):
        self.root.destroy()  # Fecha a tela inicial
        TelaLogin(self.banco, tipo)  # Abre a tela de login do usuário selecionado

    def abrir_cadastro(self):
        CadastroUsuario(self.banco)  # Abre a tela de cadastro de novo usuário


# Tela de login
class TelaLogin:
    def __init__(self, banco, tipo_usuario):
        self.banco = banco
        self.tipo_usuario = tipo_usuario
        self.root = tk.Tk()
        self.root.title(f"Login - {tipo_usuario}")  # Define o título da janela de login

        # Cria um frame centralizado para os campos e botões
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        # Título da tela de login
        tk.Label(frame, text=f"Login - {tipo_usuario}", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Campos para entrada de nome e senha
        tk.Label(frame, text="Nome:", font=("Arial", 10)).pack(pady=(5, 5))
        self.entry_nome = tk.Entry(frame, font=("Arial", 10))
        self.entry_nome.pack(pady=(5, 10))

        tk.Label(frame, text="Senha:", font=("Arial", 10)).pack(pady=(5, 5))
        self.entry_senha = tk.Entry(frame, show="*", font=("Arial", 10))
        self.entry_senha.pack(pady=(5, 20))

        # Botões de login e voltar
        tk.Button(
            frame, 
            text="Login", 
            width=20, 
            height=2, 
            font=("Arial", 10), 
            command=self.verificar_login
        ).pack(pady=10)

        tk.Button(
            frame, 
            text="Voltar", 
            width=20, 
            height=2, 
            font=("Arial", 10), 
            command=self.voltar
        ).pack(pady=5)

        self.root.mainloop()

    def verificar_login(self):
        # Aqui você pode adicionar a lógica de verificação do login
        pass

    def voltar(self):
        self.root.destroy()  # Fecha a tela de login
        TelaInicial(self.banco)  # Abre a tela inicial

    def verificar_login(self):
        # Obtém os valores dos campos
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()

        # Consulta no banco de dados
        self.banco.cursor.execute("SELECT tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        usuario = self.banco.cursor.fetchone()

        # Se usuário existir e for do tipo correto, abre o sistema de estoque
        if usuario and usuario[0] == self.tipo_usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {nome} ({usuario[0]})!")
            self.root.destroy()
            SistemaEstoque(self.banco, self.tipo_usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos ou tipo incorreto.")

    def voltar(self):
        self.root.destroy()  # Fecha a tela de login
        TelaInicial(self.banco)  # Volta para a tela inicial


# Tela de cadastro de novos usuários
class CadastroUsuario:
    def __init__(self, banco):
        self.banco = banco
        self.window = tk.Toplevel()
        self.window.title("Cadastro de Novo Usuário")

        # Cria um frame centralizado para os campos de entrada e botões
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True)

        # Título da tela de cadastro
        tk.Label(frame, text="Cadastro de Novo Usuário", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Campos de entrada para nome, senha e confirmação de senha
        tk.Label(frame, text="Nome:", font=("Arial", 10)).pack(pady=(5, 5))
        self.entry_nome = tk.Entry(frame, font=("Arial", 10))
        self.entry_nome.pack(pady=(5, 10))

        tk.Label(frame, text="Senha:", font=("Arial", 10)).pack(pady=(5, 5))
        self.entry_senha = tk.Entry(frame, show="*", font=("Arial", 10))
        self.entry_senha.pack(pady=(5, 10))

        tk.Label(frame, text="Confirmar Senha:", font=("Arial", 10)).pack(pady=(5, 5))
        self.entry_confirmar = tk.Entry(frame, show="*", font=("Arial", 10))
        self.entry_confirmar.pack(pady=(5, 20))

        # Seleção do tipo de usuário
        tk.Label(frame, text="Tipo de Usuário:", font=("Arial", 10)).pack(pady=(5, 5))
        self.tipo_var = tk.StringVar(value="Gerente de Setor")
        tk.OptionMenu(frame, self.tipo_var, "Gerente de Setor", "Estoquista", "Usuário").pack(pady=(5, 10))

        # Botão de cadastro
        tk.Button(
            frame, 
            text="Cadastrar", 
            width=20, 
            height=2, 
            font=("Arial", 10), 
            command=self.cadastrar
        ).pack(pady=10)

    def cadastrar(self):
        # Obtém os valores dos campos
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()
        tipo = self.tipo_var.get()

        # Verifica se os dados são válidos
        if not nome or not senha or senha != confirmar:
            messagebox.showerror("Erro", "Verifique os dados e tente novamente.")
            return

        # Verifica se o usuário já existe no banco
        self.banco.cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
        if self.banco.cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        # Adiciona o novo usuário ao banco de dados
        self.banco.cursor.execute("INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)", (nome, senha, tipo))
        self.banco.conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.window.destroy()
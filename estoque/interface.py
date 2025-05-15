import tkinter as tk  # Importa o módulo Tkinter para criação de interfaces gráficas
from tkinter import messagebox  # Importa messagebox para exibir mensagens ao usuário

# Classe principal do sistema de estoque, que adapta a interface conforme o tipo de usuário
class SistemaEstoque:
    def __init__(self, banco, tipo_usuario):
        self.banco = banco  # Guarda a instância do banco de dados
        self.tipo_usuario = tipo_usuario  # Guarda o tipo de usuário
        self.root = tk.Tk()  # Cria a janela principal
        self.frame_atual = None  # Inicializa um atributo para armazenar um frame específico para usuários
        self.root.title(f"Sistema - {tipo_usuario}")  # Define o título da janela

        self.widgets_dinamicos = []  # Lista para armazenar widgets que serão removidos dinamicamente

        # Define qual interface será carregada dependendo do tipo de usuário
        if tipo_usuario == "Estoquista":
            self.interface_estoquista()
        elif tipo_usuario == "Usuário":
            self.interface_usuario()
        elif tipo_usuario == "Gerente de Setor":
            self.interface_gerente()

        self.root.mainloop()  # Inicia o loop da interface

    # Método para limpar a tela atual, removendo widgets dinâmicos
    def limpar_tela(self):
        if self.frame_atual:
            self.frame_atual.destroy()
        self.frame_atual = None

    # Método para exibir alerta sobre produtos com estoque baixo ou alto
    def analisar_estoque(self):
        # Buscar produtos
        produtos = self.banco.buscar_todos_produtos()

        baixo = []
        alto = []

        for nome, qtd, preco, local in produtos:
            if qtd <= 5:
                baixo.append((nome, qtd))
            elif qtd >= 50:
                alto.append((nome, qtd))

        if not baixo and not alto:
            messagebox.showinfo("Análise de Estoque", "Todos os estoques estão dentro dos limites definidos.")
            return

        # Cria uma nova janela para exibir a análise
        janela = tk.Toplevel(self.root)
        janela.title("Análise de Estoque")

        # Cabeçalhos
        headers = ["Produto", "Quantidade", "Situação"]
        for col, header in enumerate(headers):
            tk.Label(
                janela,
                text=header,
                font=("Arial", 10, "bold"),
                borderwidth=2,
                relief="groove",
                padx=5,
                pady=5).grid(row=0, column=col, sticky="nsew")

        # Conteúdo
        linha = 1
        for nome, qtd in baixo:
            tk.Label(
                janela, 
                text=nome, 
                borderwidth=1, 
                relief="solid", 
                padx=5, pady=5).grid(row=linha, column=0, sticky="nsew")
            tk.Label(
                janela, 
                text=f"{qtd} un.", 
                borderwidth=1, 
                relief="solid", 
                padx=5, pady=5).grid(row=linha, column=1, sticky="nsew")
            tk.Label(
                janela, 
                text="🔻 Baixo", 
                fg="red", 
                borderwidth=1, 
                relief="solid", 
                padx=5, 
                pady=5).grid(row=linha, column=2, sticky="nsew")
            linha += 1

        for nome, qtd in alto:
            tk.Label(
                janela, 
                text=nome, 
                borderwidth=1, 
                relief="solid", 
                padx=5, 
                pady=5).grid(row=linha, column=0, sticky="nsew")
            tk.Label(
                janela, 
                text=f"{qtd} un.", 
                borderwidth=1, 
                relief="solid", 
                padx=5, 
                pady=5).grid(row=linha, column=1, sticky="nsew")
            tk.Label(
                janela, 
                text="🔺 Alto", 
                fg="green", 
                borderwidth=1, 
                relief="solid", 
                padx=5, 
                pady=5).grid(row=linha, column=2, sticky="nsew")
            linha += 1

        # Botão para fechar
        tk.Button(
            janela, 
            text="Fechar", 
            command=janela.destroy).grid(
                row=linha, 
                column=0, 
                columnspan=3, 
                pady=10)

        # Deixa as colunas expandirem igualmente
        for col in range(3):
            janela.grid_columnconfigure(col, weight=1)


    # ==================== INTERFACE ESTOQUISTA ====================
    
    # Interface específica para o Estoquista
    def interface_estoquista(self):
        self.limpar_tela()

        # Cria um frame centralizado para os botões
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título da tela
        tk.Label(self.frame_atual, text="Menu do Estoquista", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Lista de botões e funções correspondentes
        botoes = [
            ("Solicitar Compra", self.mostrar_campos_estoquista),
            ("Registrar Entrada", self.mostrar_campos_entrada),
            ("Registrar Saída", self.mostrar_campos_saida),
            ("Emitir Relatório", self.abrir_rastreamento),
            ("Analisar Estoque", self.analisar_estoque),
            ("Voltar", self.voltar)
    ]

        # Adiciona os botões à tela com formatação padronizada
        for texto, comando in botoes:
            tk.Button(
                self.frame_atual,
                text=texto,
                command=comando,
                width=25,
                height=2,
                font=("Arial", 10)
            ).pack(pady=8)

    # Método para exibir os campos de solicitação de compra
    def mostrar_campos_estoquista(self):
        self.limpar_tela()

        # Frame central com padding
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título da tela
        tk.Label(self.frame_atual, text="Solicitar Compra", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Campo: Produto
        tk.Label(self.frame_atual, text="Produto:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_produto = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_produto.pack(pady=(0, 10))

        # Campo: Quantidade
        tk.Label(self.frame_atual, text="Quantidade:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_quantidade = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_quantidade.pack(pady=(0, 20))

        # Botão: Exibir produtos
        tk.Button(
            self.frame_atual,
            text="Exibir Produtos",
            command=self.exibir_produtos_disponiveis,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=5)

        # Botão: Enviar pedido
        tk.Button(
            self.frame_atual,
            text="Enviar Pedido",
            command=self.solicitar_compra_estoquista,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=5)

        # Botão: Voltar
        tk.Button(
            self.frame_atual,
            text="Voltar",
            command=self.voltar_estoquista,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=(15, 5))

    def mostrar_campos_entrada(self):
        self.limpar_tela()

        # Frame central com padding
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)
    
        # Título da tela
        tk.Label(self.frame_atual, text="Registrar Entrada de Produto", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Campo: Produto
        tk.Label(self.frame_atual, text="Produto:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_produto = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_produto.pack(pady=(0, 10))

        # Campo: Quantidade
        tk.Label(self.frame_atual, text="Quantidade:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_quantidade = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_quantidade.pack(pady=(0, 10))

        # Campo: Preço
        tk.Label(self.frame_atual, text="Preço:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_preco = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_preco.pack(pady=(0, 10))

        # Campo: Localização
        tk.Label(self.frame_atual, text="Localização:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_localizacao = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_localizacao.pack(pady=(0, 20))

        # Botão de confirmação
        btn_confirmar = tk.Button(
            self.frame_atual,
            text="Confirmar Entrada",
            command=self.registrar_entrada,
            width=25,
            height=2,
            font=("Arial", 10)
        )
        # Botão para exibir produtos
        tk.Button(
            self.frame_atual,
            text="Exibir Produtos",
            command=self.exibir_produtos_disponiveis,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=8)

        # Adiciona o botão de confirmação à lista de widgets dinâmicos
        btn_confirmar.pack(pady=(0, 10))
        self.widgets_dinamicos.append(btn_confirmar)

        # Botão de voltar
        tk.Button(
            self.frame_atual,
            text="Voltar",
            command=self.voltar_estoquista,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack()


    # Método para registrar a entrada de um produto no banco de dados
    def registrar_entrada(self):
        try:
            nome = self.entry_produto.get()
            quantidade = int(self.entry_quantidade.get())
            preco = float(self.entry_preco.get())
            localizacao = self.entry_localizacao.get()

            if not nome or quantidade <= 0 or preco <= 0 or not localizacao:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
                return

            self.banco.adicionar_produto(nome, quantidade, preco, localizacao)
            messagebox.showinfo("Sucesso", "Entrada registrada.")
            self.limpar_tela()
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos. Verifique a quantidade e o preço.")
        self.interface_estoquista()

    # Método para exibir campos de saída de produtos
    def mostrar_campos_saida(self):
        self.limpar_tela()

        # Frame central com padding
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título da tela
        tk.Label(self.frame_atual, text="Registrar Saída de Produto", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Campo: Produto
        tk.Label(self.frame_atual, text="Produto:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_produto = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_produto.pack(pady=(0, 10))

        # Campo: Quantidade
        tk.Label(self.frame_atual, text="Quantidade:", font=("Arial", 10)).pack(pady=(5, 2))
        self.entry_quantidade = tk.Entry(self.frame_atual, font=("Arial", 10))
        self.entry_quantidade.pack(pady=(0, 20))

        # Botão de confirmação
        btn_confirmar = tk.Button(
            self.frame_atual,
            text="Confirmar Saída",
            command=self.registrar_saida,
            width=25,
            height=2,
            font=("Arial", 10)
        )
        # Botão para exibir produtos
        tk.Button(
            self.frame_atual,
            text="Exibir Produtos",
            command=self.exibir_produtos_disponiveis,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=8)
        
        btn_confirmar.pack(pady=(0, 10))
        self.widgets_dinamicos.append(btn_confirmar)

        # Botão de voltar
        tk.Button(
            self.frame_atual,
            text="Voltar",
            command=self.voltar_estoquista,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack()

    def voltar_estoquista(self):
        self.limpar_tela()
        self.interface_estoquista()
        
    # Método para registrar a saída de um produto do estoque
    def registrar_saida(self):
        
        try:
            nome_produto = self.entry_produto.get()
            quantidade = int(self.entry_quantidade.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida. Digite um número inteiro.")
            return

        if not nome_produto or quantidade <= 0:
            messagebox.showwarning("Aviso", "Preencha todos os campos corretamente.")
            return

        resultado = self.banco.registrar_saida_produto(nome_produto, quantidade)

        if resultado is True:
            messagebox.showinfo("Sucesso", f"{quantidade} unidades de '{nome_produto}' removidas do estoque.")
            self.limpar_tela()
        elif resultado is False:
            messagebox.showerror("Erro", "Estoque insuficiente para a saída solicitada.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")
        self.interface_estoquista()

    # Método para exibir produtos por localização no estoque
    def abrir_rastreamento(self):
        janela = tk.Toplevel(self.root)
        janela.title("Áreas do Estoque") 

        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(padx=20, pady=20)

        titulo = tk.Label(frame_botoes, text="Selecione uma Área:", font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))

        # Botão para todos os produtos
        tk.Button(
            frame_botoes, 
            text="Todos os Produtos", 
            width=25, 
            height=2, 
            font=("Arial", 10), 
            command=lambda: 
            self.exibir_por_area("Todos")).pack(pady=8)

        # Botões para áreas específicas
        areas = [
            "Eletrônicos", 
            "Alimentos", 
            "Móveis", 
            "Roupas", 
            "Brinquedos"
            ]
        
        for area in areas:
            tk.Button(
                frame_botoes, 
                text=area, 
                width=25, 
                height=2, 
                font=("Arial", 10), 
                command=lambda a=area: 
                self.exibir_por_area(a)).pack(pady=5)

        # Botão de voltar
        tk.Button(
            frame_botoes, 
            text="Voltar", 
            width=25, 
            height=2, 
            font=("Arial", 10), 
            command=janela.destroy).pack(pady=(15, 0))


    def exibir_por_area(self, area):
        # Buscar produtos
        produtos = self.banco.buscar_todos_produtos() if area == "Todos" else self.banco.buscar_por_localizacao(area)

        if not produtos:
            messagebox.showinfo("Relatório por Área", f"Nenhum produto encontrado na área '{area}'.")
            return

        # Cria uma nova janela para exibir o relatório
        janela = tk.Toplevel(self.root)
        janela.title(f"Relatório: {area}")

        # Cabeçalhos
        headers = ["Produto", "Quantidade", "Preço (R$)", "Localização"]
        for col, header in enumerate(headers):
            tk.Label(
                janela, 
                text=header, 
                font=("Arial", 10, "bold"), 
                borderwidth=2, 
                relief="groove", 
                padx=5, 
                pady=5).grid(row=0, column=col, sticky="nsew")

        # Conteúdo
        for row, produto in enumerate(produtos, start=1):
            for col, valor in enumerate(produto):
                if col == 2:  # Preço
                    valor = f"R${valor:.2f}"
                tk.Label(
                    janela, 
                    text=valor, 
                    borderwidth=1, 
                    relief="solid", 
                    padx=5, 
                    pady=5).grid(row=row, column=col, sticky="nsew")

        # Botão para fechar
        tk.Button(
            janela, 
            text="Fechar", 
            command=janela.destroy).grid(row=row+1, column=0, columnspan=4, pady=10)

        # Deixa as colunas expandirem igualmente
        for col in range(4):
            janela.grid_columnconfigure(col, weight=1)

    # ==================== INTERFACE USUÁRIO ====================

    # Método para configurar a interface gráfica do usuário
    def interface_usuario(self):
        self.limpar_tela()

        # Cria um frame centralizado para os botões
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título da tela
        tk.Label(self.frame_atual, text="Menu do Usuário", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Botões principais
        botoes = [
            ("Solicitar Compra", self.mostrar_campos_usuario),
            ("Emitir Relatório", self.abrir_rastreamento),
            ("Analisar Estoque", self.analisar_estoque),
            ("Voltar", self.voltar)
        ]

        for texto, comando in botoes:
            tk.Button(
                self.frame_atual,
                text=texto,
                command=comando,
                width=25,  # Deixa todos os botões do mesmo tamanho
                height=2,
                font=("Arial", 10)
            ).pack(pady=8)

    # Método para exibir os campos de solicitação de compra
    def mostrar_campos_usuario(self):
        self.limpar_tela()

        # Cria um frame centralizado para os campos
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título da tela
        tk.Label(self.frame_atual, text="Solicitar Compra", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Label e campo para o nome do produto
        tk.Label(self.frame_atual, text="Nome do Produto:", font=("Arial", 12)).pack(anchor="w")
        self.entry_produto = tk.Entry(self.frame_atual, font=("Arial", 12), width=30)
        self.entry_produto.pack(pady=8)

        # Label e campo para a quantidade
        tk.Label(self.frame_atual, text="Quantidade:", font=("Arial", 12)).pack(anchor="w")
        self.entry_quantidade = tk.Entry(self.frame_atual, font=("Arial", 12), width=30)
        self.entry_quantidade.pack(pady=8)

        # Botão para exibir produtos
        tk.Button(
            self.frame_atual,
            text="Exibir Produtos",
            command=self.exibir_produtos_disponiveis,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=8)

        # Botão para enviar pedido
        tk.Button(
            self.frame_atual,
            text="Enviar Pedido",
            command=self.solicitar_compra,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=8)

        # Botão para voltar
        tk.Button(
            self.frame_atual,
            text="Voltar",
            command=self.voltar_usuario,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=8)

    def voltar_usuario(self):
        self.limpar_tela()
        self.interface_usuario()

    # Método para solicitar uma compra
    def solicitar_compra(self):

        try:
            produto = self.entry_produto.get()
            quantidade = int(self.entry_quantidade.get())

            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return

            produtos = self.banco.buscar_todos_produtos()
            produto_existe = any(p[0].lower() == produto.lower() for p in produtos)

            if not produto_existe:
                messagebox.showerror("Erro", "Produto não encontrado no estoque.")
                return

            self.banco.salvar_pedido(produto, quantidade)
            messagebox.showinfo("Sucesso", "Pedido enviado com sucesso!")

            self.limpar_tela()
            self.interface_usuario()  # Retorna à interface do usuário após enviar o pedido

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira uma quantidade numérica válida.")

        
    def solicitar_compra_estoquista(self):

        try:
            produto = self.entry_produto.get()
            quantidade = int(self.entry_quantidade.get())

            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return

            produtos = self.banco.buscar_todos_produtos()
            produto_existe = any(p[0].lower() == produto.lower() for p in produtos)

            if not produto_existe:
                messagebox.showerror("Erro", "Produto não encontrado no estoque.")
                return

            self.banco.salvar_pedido(produto, quantidade)
            messagebox.showinfo("Sucesso", "Pedido enviado com sucesso!")

            self.limpar_tela()
            self.interface_estoquista()  # Retorna à interface do estoquista após enviar o pedido

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira uma quantidade numérica válida.")

    # Método para exibir os produtos disponíveis no estoque
    def exibir_produtos_disponiveis(self):
        produtos = self.banco.buscar_todos_produtos()

        if not produtos:
            messagebox.showinfo("Produtos no Estoque", "Nenhum produto disponível no estoque.")
            return

        # Cria uma nova janela para exibir os produtos em formato de tabela
        janela = tk.Toplevel(self.root)
        janela.title("Produtos Disponíveis no Estoque")

        # Cabeçalhos da tabela
        headers = ["Produto", "Quantidade", "Preço (R$)", "Localização"]
        for col, header in enumerate(headers):
            tk.Label(
                janela,
                text=header,
                font=("Arial", 10, "bold"),
                borderwidth=2,
                relief="groove",
                padx=5,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        # Conteúdo da tabela
        for row, produto in enumerate(produtos, start=1):
            for col, valor in enumerate(produto):
                if col == 2:  # Formata o preço
                    valor = f"R${valor:.2f}"
                tk.Label(
                    janela,
                    text=valor,
                    font=("Arial", 10),
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=row, column=col, sticky="nsew")

        # Botão para fechar a janela
        tk.Button(
            janela,
            text="Fechar",
            font=("Arial", 10),
            width=25,
            command=janela.destroy
        ).grid(row=row + 1, column=0, columnspan=4, pady=10)

        # Configura as colunas para expandirem igualmente
        for col in range(4):
            janela.grid_columnconfigure(col, weight=1)

    # ==================== INTERFACE GERENTE ====================

    # Método para a interface do gerente, que exibe pedidos pendentes
    def interface_gerente(self):
        self.limpar_tela()

        # Frame central com padding
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True)

        # Título
        tk.Label(self.frame_atual, text="Pedidos Pendentes", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Lista de pedidos
        self.lista = tk.Listbox(self.frame_atual, width=60, font=("Arial", 10))
        self.lista.pack(pady=(0, 20))

        # Botão: Autorizar
        tk.Button(
            self.frame_atual,
            text="Autorizar",
            command=lambda: self.atualizar_status("Autorizado"),
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=5)

        # Botão: Rejeitar
        tk.Button(
            self.frame_atual,
            text="Rejeitar",
            command=lambda: self.atualizar_status("Rejeitado"),
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=5)

        # Botão: Voltar
        tk.Button(
            self.frame_atual,
            text="Voltar",
            command=self.voltar,
            width=25,
            height=2,
            font=("Arial", 10)
        ).pack(pady=(15, 5))

        # Carrega os pedidos na lista
        self.carregar_pedidos()

    # Método para carregar pedidos pendentes na lista
    def carregar_pedidos(self):
        self.lista.delete(0, tk.END)  # Limpa a lista antes de recarregar
        for id_, produto, qtd, status in self.banco.obter_pedidos_pendentes():
            self.lista.insert(tk.END, f"ID:{id_} | {produto} - {qtd} un. | {status}")

    # Método para atualizar o status de um pedido
    def atualizar_status(self, status):
        selecao = self.lista.curselection()
        if selecao:
            pedido_id = int(self.lista.get(selecao[0]).split("|")[0].split(":")[1])
            self.banco.atualizar_status_pedido(pedido_id, status)
            self.carregar_pedidos()
            messagebox.showinfo("Sucesso", f"Pedido {status.lower()}.")

    # Método para voltar à tela inicial do sistema
    def voltar(self):
        from telas.telas import TelaInicial
        self.root.destroy()
        TelaInicial(self.banco)
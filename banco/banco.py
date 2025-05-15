import sqlite3

# Classe que gerencia o banco de dados
class SistemaDB:
    def __init__(self, nome='estoque.db'):
        # Conecta ao banco de dados SQLite (ou cria um novo se não existir)
        self.conn = sqlite3.connect(nome)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()  # Chama o método para criar as tabelas no banco de dados

    # Método para criar tabelas necessárias no banco de dados
    def criar_tabelas(self):
        # Tabela de usuários (cada usuário tem um ID, nome, senha e tipo)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )""")
        
        # Tabela de produtos (cada produto tem um ID, nome, quantidade, preço e localização)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                localizacao TEXT
            )""")
        
        # Tabela de pedidos (cada pedido tem um ID, produto, quantidade e um status)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                status TEXT DEFAULT 'Pendente'
            )""")
        
        # Confirma as alterações no banco de dados
        self.conn.commit()

    # Método para buscar todos os produtos do banco de dados
    def buscar_todos_produtos(self):
        self.cursor.execute("SELECT nome, quantidade, preco, localizacao FROM produtos")
        return self.cursor.fetchall()  # Retorna todos os produtos encontrados

    # Método para adicionar um novo produto ou atualizar um existente
    def adicionar_produto(self, nome, quantidade, preco, localizacao):
        self.cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
        if self.cursor.fetchone():  # Se o produto já existir, atualiza a quantidade, preço e localização
            self.cursor.execute("UPDATE produtos SET quantidade = quantidade + ?, preco = ?, localizacao = ? WHERE nome = ?", 
                                (quantidade, preco, localizacao, nome))
        else:  # Caso contrário, adiciona um novo produto ao banco de dados
            self.cursor.execute("INSERT INTO produtos (nome, quantidade, preco, localizacao) VALUES (?, ?, ?, ?)", 
                                (nome, quantidade, preco, localizacao))
        self.conn.commit()  # Confirma a operação

    # Método para registrar a saída de um produto, verificando se há estoque suficiente
    def registrar_saida_produto(self, nome, quantidade):
        self.cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome,))
        result = self.cursor.fetchone()
        if result:
            estoque_atual = result[0]
            if estoque_atual >= quantidade:  # Se houver quantidade suficiente, atualiza o estoque
                self.cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE nome = ?", 
                                    (quantidade, nome))
                self.conn.commit()
                return True
            else:
                return False  # Indica que o estoque não é suficiente
        return None  # Indica que o produto não foi encontrado

    # Método para buscar produtos por localização
    def buscar_por_localizacao(self, area):
        self.cursor.execute("SELECT nome, quantidade, preco, localizacao FROM produtos WHERE localizacao = ?", (area,))
        return self.cursor.fetchall()

    # Método para obter um relatório completo de todos os produtos
    def obter_relatorio_completo(self):
        self.cursor.execute("SELECT nome, quantidade, preco, localizacao FROM produtos")
        return self.cursor.fetchall()

    # Método para registrar um novo pedido
    def salvar_pedido(self, produto, quantidade):
        self.cursor.execute("INSERT INTO pedidos (produto, quantidade) VALUES (?, ?)", (produto, quantidade))
        self.conn.commit()

    # Método para obter pedidos pendentes
    def obter_pedidos_pendentes(self):
        self.cursor.execute("SELECT id, produto, quantidade, status FROM pedidos WHERE status = 'Pendente'")
        return self.cursor.fetchall()

    # Método para atualizar o status de um pedido
    def atualizar_status_pedido(self, pedido_id, status):
        self.cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
        self.conn.commit()

    # Método para fechar a conexão com o banco de dados
    def fechar(self):
        self.conn.close()
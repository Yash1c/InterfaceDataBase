from PyQt5.QtWidgets import QFormLayout, QDialog, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTabWidget, QMessageBox, QScrollArea, QHBoxLayout, QComboBox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

# Variável global com os valores permitidos para a role
ROLES_PERMITIDAS = ["admin", "gerente", "funcionario"]

# Configuração do banco de dados com SQLAlchemy para MariaDB
username = 'root'
password = ''
host = 'localhost'
port = '3306'
database = 'mercado_gui'

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')


Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Sincronizando a estrutura das tabelas no banco de dados
Base.metadata.create_all(engine)

# Modelo Cliente
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))
    numero = Column(String(50))
    cpf = Column(String(50))

# Modelo Produto
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    preco = Column(String(50))
    quantidade = Column(String(50))

# Modelo Fornecedor
class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))
    telefone = Column(String(50))

# Modelo Funcionário
class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))
    telefone = Column(String(50))

# Modelo Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))
    senha = Column(String(50))
    role = Column(String(50)) # 'admin, 'gerente', 'funcionario'

# -------------------------------------------------------

# Criando a base do banco
Base.metadata.create_all(engine)

# Interface gráfica com PyQt5
class MercadoGui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Mercado Gui")

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Abas:
        self.tab_widget.addTab(self.create_login_tab(), "Login")
        self.tab_widget.addTab(self.create_cliente_tab(), "Cliente")
        self.tab_widget.addTab(self.create_produto_tab(), "Produto")
        self.tab_widget.addTab(self.create_fornecedor_tab(), "Fornecedor")
        self.tab_widget.addTab(self.create_funcionario_tab(), "Funcionário")
        self.tab_widget.addTab(self.create_usuario_tab(), "Usuário")
        # A aba de consulta SQL será adicionada, mas desabilitada inicialmente
        self.query_tab = self.create_query_tab()
        self.tab_widget.addTab(self.query_tab, "Consulta SQL")

        # Desabilitar a aba de consulta SQL inicialmente
        self.tab_widget.setTabEnabled(self.tab_widget.indexOf(self.query_tab), False)

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    # --------------- LOGIN ----------------
    def login(self, nome, senha):
        user = session.query(Usuario).filter_by(nome=nome, senha=senha).first()
        if user:
            if user.role not in ROLES_PERMITIDAS:
                QMessageBox.warning(self, "Erro", "Usuário com role inválida! Contate o administrador.")
            else:
                self.current_user = user.role
                QMessageBox.information(self, "Sucesso", f"Bem-vindo, {user.nome}!")
                # Habilitar a aba de consulta SQL após o login
                self.tab_widget.setTabEnabled(self.tab_widget.indexOf(self.query_tab), True)
                # Mudar para a aba de consulta SQL (ou qualquer outra aba desejada)
                self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.query_tab))
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")

    # Verificar permissões antes de executar ações:
    def check_permission(self, role):
        if self.current_user != role:
            QMessageBox.warning(self, "Erro", "Você não tem permissão para executar esta ação!")
            return False
        return True
    
    # --------------- Controle de Gerenciamento de Transações ----------------
    def transactional_operation(self):
        try:
            session.begin()  # Inicia a transação
            session.commit()  # Commit da transação
            QMessageBox.information(self, "Sucesso", "Operação realizada com sucesso!")
        except Exception as e:
            session.rollback()  # Rollback em caso de erro
            QMessageBox.warning(self, "Erro", f"Erro ao executar operação: {e}")

# --------------- LOGIN ------------------
    def create_login_tab(self):
        login_widget = QWidget()
        layout = QFormLayout()

        self.nome_login_input = QLineEdit()
        self.senha_login_input = QLineEdit()
        self.senha_login_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Nome do Usuário:", self.nome_login_input)
        layout.addRow("Senha do Usuário:", self.senha_login_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(lambda: self.login(self.nome_login_input.text(), self.senha_login_input.text()))

        layout.addRow(self.login_btn)
        login_widget.setLayout(layout)
        return login_widget

# --------------- CLIENTE ----------------
    def create_cliente_tab(self):
        cliente_widget = QWidget()
        layout = QFormLayout()

        # Campos de texto:
        self.nome_input = QLineEdit()
        self.email_input = QLineEdit()
        self.numero_input = QLineEdit()
        self.cpf_input = QLineEdit()

        # Adicionando widgets ao layout
        layout.addRow("Nome do cliente:", self.nome_input)
        layout.addRow("Email do cliente:", self.email_input)
        layout.addRow("Número do cliente:", self.numero_input)
        layout.addRow("CPF do cliente:", self.cpf_input)

        # Botões CRUD
        btn_layout = QHBoxLayout()
        self.create_btn = QPushButton('Criar Cliente')
        self.read_btn = QPushButton('Ler Clientes')
        self.update_btn = QPushButton('Atualizar Cliente')
        self.delete_btn = QPushButton('Deletar Cliente')

        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.read_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addRow(btn_layout)

        # Conectar os botões às funções CRUD
        self.create_btn.clicked.connect(self.create_cliente)
        self.read_btn.clicked.connect(self.read_clientes)
        self.update_btn.clicked.connect(self.update_cliente)
        self.delete_btn.clicked.connect(self.delete_cliente)

        cliente_widget.setLayout(layout)
        return cliente_widget


# --------------- PRODUTO ----------------
    def create_produto_tab(self):
        produto_widget = QWidget()
        layout = QFormLayout()

        self.nome_produto_input = QLineEdit()
        self.preco_input = QLineEdit()
        self.quantidade_input = QLineEdit()

        # Campo de textos:
        layout.addRow("Nome do Produto:", self.nome_produto_input)
        layout.addRow("Preço do Produto:", self.preco_input)
        layout.addRow("Quantidade do Produto:", self.quantidade_input)

        # Botões CRUD
        btn_layout = QHBoxLayout()
        self.create_produto_btn = QPushButton('Criar Produto')
        self.read_produto_btn = QPushButton('Ler Produtos')
        self.update_produto_btn = QPushButton('Atualizar Produto')
        self.delete_produto_btn = QPushButton('Deletar Produto')

        # Adicionando widgets ao layout
        btn_layout.addWidget(self.create_produto_btn)
        btn_layout.addWidget(self.read_produto_btn)
        btn_layout.addWidget(self.update_produto_btn)
        btn_layout.addWidget(self.delete_produto_btn)
        
        layout.addRow(btn_layout)
        
        # Conectar os botões às funções CRUD
        self.create_produto_btn.clicked.connect(self.create_produto)
        self.read_produto_btn.clicked.connect(self.read_produtos)
        self.update_produto_btn.clicked.connect(self.update_produto)
        self.delete_produto_btn.clicked.connect(self.delete_produto)

        produto_widget.setLayout(layout)
        return produto_widget

# ----------------- FORNECEDOR ----------------

    def create_fornecedor_tab(self):
        Fornecedor_widget = QWidget()
        layout = QFormLayout()

        # Campo de textos:
        self.nome_fornecedor_input = QLineEdit()
        self.email_fornecedor_input = QLineEdit()
        self.telefone_fornecedor_input = QLineEdit()
        
        layout.addRow("Nome do Fornecedor:", self.nome_fornecedor_input)
        layout.addRow("Email do Fornecedor:", self.email_fornecedor_input)
        layout.addRow("Telefone do Fornecedor:", self.telefone_fornecedor_input)

        # Botões CRUD
        btn_layout = QHBoxLayout()
        self.create_fornecedor_btn = QPushButton('Criar Fornecedor')
        self.read_fornecedor_btn = QPushButton('Ler Fornecedores')
        self.update_fornecedor_btn = QPushButton('Atualizar Fornecedor')
        self.delete_fornecedor_btn = QPushButton('Deletar Fornecedor')

        # Adicionando widgets ao layout
        btn_layout.addWidget(self.create_fornecedor_btn)
        btn_layout.addWidget(self.read_fornecedor_btn)
        btn_layout.addWidget(self.update_fornecedor_btn)
        btn_layout.addWidget(self.delete_fornecedor_btn)

        layout.addRow(btn_layout)

        # Conectar os botões às funções CRUD
        self.create_fornecedor_btn.clicked.connect(self.create_fornecedor)
        self.read_fornecedor_btn.clicked.connect(self.read_fornecedores)
        self.update_fornecedor_btn.clicked.connect(self.update_fornecedor)
        self.delete_fornecedor_btn.clicked.connect(self.delete_fornecedor)

        Fornecedor_widget.setLayout(layout)
        return Fornecedor_widget

# ----------------- FUNCIONÁRIO ----------------
    def create_funcionario_tab(self):
        Funcionario_widget = QWidget()
        layout = QFormLayout()

        # Campo de textos:
        self.nome_funcionario_input = QLineEdit()
        self.email_funcionario_input = QLineEdit()
        self.telefone_funcionario_input = QLineEdit()

        layout.addRow("Nome do Funcionário:", self.nome_funcionario_input)
        layout.addRow("Email do Funcionário:", self.email_funcionario_input)
        layout.addRow("Telefone do Funcionário:", self.telefone_funcionario_input)

        # Botões CRUD
        btn_layout = QHBoxLayout()
        self.create_funcionario_btn = QPushButton('Criar Funcionário')
        self.read_funcionario_btn = QPushButton('Ler Funcionários')
        self.update_funcionario_btn = QPushButton('Atualizar Funcionário')
        self.delete_funcionario_btn = QPushButton('Deletar Funcionário')

        # Adicionando widgets ao layout
        btn_layout.addWidget(self.create_funcionario_btn)
        btn_layout.addWidget(self.read_funcionario_btn)
        btn_layout.addWidget(self.update_funcionario_btn)
        btn_layout.addWidget(self.delete_funcionario_btn)

        layout.addRow(btn_layout)

        # Conectar os botões às funções CRUD
        self.create_funcionario_btn.clicked.connect(self.create_funcionario)
        self.read_funcionario_btn.clicked.connect(self.read_funcionarios)
        self.update_funcionario_btn.clicked.connect(self.update_funcionario)
        self.delete_funcionario_btn.clicked.connect(self.delete_funcionario)

        Funcionario_widget.setLayout(layout)
        return Funcionario_widget
    

# ----------------- USUARIOS ----------------

    def create_usuario_tab(self):
        Usuario_widget = QWidget()
        layout = QFormLayout()

        # Campo de textos:
        self.nome_usuario_input = QLineEdit()
        self.email_usuario_input = QLineEdit()
        self.senha_usuario_input = QLineEdit()
        self.role_usuario_input = QComboBox()
        self.role_usuario_input.addItems(ROLES_PERMITIDAS)

        layout.addRow("Nome do Usuário:", self.nome_usuario_input)
        layout.addRow("Email do Usuário:", self.email_usuario_input)
        layout.addRow("Senha do Usuário:", self.senha_usuario_input)
        layout.addRow("Role do Usuário:", self.role_usuario_input)


        # Botões CRUD
        btn_layout = QHBoxLayout()
        self.create_usuario_btn = QPushButton('Criar Usuário')
        self.read_usuario_btn = QPushButton('Ler Usuários')
        self.update_usuario_btn = QPushButton('Atualizar Usuário')
        self.delete_usuario_btn = QPushButton('Deletar Usuário')

        # Adicionando widgets ao layout
        btn_layout.addWidget(self.create_usuario_btn)
        btn_layout.addWidget(self.read_usuario_btn)
        btn_layout.addWidget(self.update_usuario_btn)
        btn_layout.addWidget(self.delete_usuario_btn)

        layout.addRow(btn_layout)

        # Conectar os botões às funções CRUD
        self.create_usuario_btn.clicked.connect(self.create_usuario)
        self.read_usuario_btn.clicked.connect(self.read_usuarios)
        self.update_usuario_btn.clicked.connect(self.update_usuario)
        self.delete_usuario_btn.clicked.connect(self.delete_usuario)

        Usuario_widget.setLayout(layout)
        return Usuario_widget

# ----------------- FUNÇÕES CLIENTE CRUD -----------------
    def create_cliente(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        numero = self.numero_input.text()
        cpf = self.cpf_input.text()

        # Verifica se todos os campos estão preenchidos
        if nome and email and numero and cpf:
            novo_cliente = Cliente(nome=nome, email=email, numero=numero, cpf=cpf)
            session.add(novo_cliente)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Cliente criado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")

    def read_clientes(self):
        clientes = session.query(Cliente).all()
        if clientes:
            cliente_info = "\n".join([f"ID: {cliente.id}, Nome: {cliente.nome}, Email: {cliente.email}" for cliente in clientes])
            QMessageBox.information(self, "Clientes", cliente_info)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum cliente encontrado!")

    def update_cliente(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Atualizar Cliente')
        
        layout = QVBoxLayout()
        
        id_label = QLabel("ID do Cliente:")
        self.id_input_cliente = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_cliente)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_update_cliente(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_update_cliente(self, dialog):
        id_cliente = self.id_input_cliente.text()
        
        cliente = session.query(Cliente).filter_by(id=id_cliente).first()
        if cliente:
            cliente.nome = self.nome_input.text()
            cliente.email = self.email_input.text()
            cliente.numero = self.numero_input.text()
            cliente.cpf = self.cpf_input.text()
            session.commit()
            QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Cliente não encontrado!")

    def delete_cliente(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Deletar Cliente')
        
        layout = QVBoxLayout()
        
        id_label = QLabel("ID do Cliente:")
        self.id_input_cliente = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_cliente)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_delete_cliente(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_delete_cliente(self, dialog):
        id_cliente = self.id_input_cliente.text()
        
        cliente = session.query(Cliente).filter_by(id=id_cliente).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Cliente deletado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Cliente não encontrado!")


# ----------------- FUNÇÕES PRODUTO CRUD -----------------
    def create_produto(self):
        nome = self.nome_produto_input.text()
        preco = self.preco_input.text()
        quantidade = self.quantidade_input.text()

        # Verifica se todos os campos estão preenchidos
        if nome and preco and quantidade:
            novo_produto = Produto(nome=nome, preco=preco, quantidade=quantidade)
            session.add(novo_produto)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Produto criado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")

    def read_produtos(self):
        produtos = session.query(Produto).all()
        if produtos:
            produto_info = "\n".join([f"ID: {produto.id}, Nome: {produto.nome}, Preço: {produto.preco}, Quantidade: {produto.quantidade}" for produto in produtos])
            QMessageBox.information(self, "Produtos", produto_info)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum produto encontrado!")

    def update_produto(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Atualizar Produto')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Produto:")
        self.id_input_produto = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_produto)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_update_produto(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_update_produto(self, dialog):
        id_produto = self.id_input_produto.text()
        
        produto = session.query(Produto).filter_by(id=id_produto).first()
        if produto:
            produto.nome = self.nome_produto_input.text()
            produto.preco = self.preco_input.text()
            produto.quantidade = self.quantidade_input.text()
            session.commit()
            QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Produto não encontrado!")

    def delete_produto(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Deletar Produto')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Produto:")
        self.id_input_produto = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_produto)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_delete_produto(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_delete_produto(self, dialog):
        id_produto = self.id_input_produto.text()
        
        produto = session.query(Produto).filter_by(id=id_produto).first()
        if produto:
            session.delete(produto)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Produto deletado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Produto não encontrado!")
# ----------------- FUNÇÕES FORNECEDOR CRUD -----------------
    def create_fornecedor(self):
        nome = self.nome_fornecedor_input.text()
        email = self.email_fornecedor_input.text()
        telefone = self.telefone_fornecedor_input.text()

        # Verifica se todos os campos estão preenchidos
        if nome and email and telefone:
            novo_fornecedor = Fornecedor(nome=nome, email=email, telefone=telefone)
            session.add(novo_fornecedor)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Fornecedor criado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")

    def read_fornecedores(self):
        fornecedores = session.query(Fornecedor).all()
        if fornecedores:
            fornecedor_info = "\n".join([f"ID: {fornecedor.id}, Nome: {fornecedor.nome}, Email: {fornecedor.email}, Telefone: {fornecedor.telefone}" for fornecedor in fornecedores])
            QMessageBox.information(self, "Fornecedores", fornecedor_info)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum fornecedor encontrado!")

    def update_fornecedor(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Atualizar Fornecedor')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Fornecedor:")
        self.id_input_fornecedor = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_fornecedor)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_update_fornecedor(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_update_fornecedor(self, dialog):
        id_fornecedor = self.id_input_fornecedor.text()
        
        fornecedor = session.query(Fornecedor).filter_by(id=id_fornecedor).first()
        if fornecedor:
            fornecedor.nome = self.nome_fornecedor_input.text()
            fornecedor.email = self.email_fornecedor_input.text()
            fornecedor.telefone = self.telefone_fornecedor_input.text()
            session.commit()
            QMessageBox.information(self, "Sucesso", "Fornecedor atualizado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Fornecedor não encontrado!")

    def delete_fornecedor(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Deletar Fornecedor')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Fornecedor:")
        self.id_input_fornecedor = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_fornecedor)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_delete_fornecedor(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_delete_fornecedor(self, dialog):
        id_fornecedor = self.id_input_fornecedor.text()
        
        fornecedor = session.query(Fornecedor).filter_by(id=id_fornecedor).first()
        if fornecedor:
            session.delete(fornecedor)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Fornecedor deletado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Fornecedor não encontrado!")


# ----------------- FUNÇÕES FUNCIONÁRIO CRUD -----------------
    def create_funcionario(self):
        nome = self.nome_funcionario_input.text()
        email = self.email_funcionario_input.text()
        telefone = self.telefone_funcionario_input.text()

        # Verifica se todos os campos estão preenchidos
        if nome and email and telefone:
            novo_funcionario = Funcionario(nome=nome, email=email, telefone=telefone)
            session.add(novo_funcionario)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Funcionário criado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")

    def read_funcionarios(self):
        funcionarios = session.query(Funcionario).all()
        if funcionarios:
            funcionario_info = "\n".join([f"ID: {funcionario.id}, Nome: {funcionario.nome}, Email: {funcionario.email}, Telefone: {funcionario.telefone}" for funcionario in funcionarios])
            QMessageBox.information(self, "Funcionários", funcionario_info)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum funcionário encontrado!")

    def update_funcionario(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Atualizar Funcionário')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Funcionário:")
        self.id_input_funcionario = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_funcionario)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_update_funcionario(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_update_funcionario(self, dialog):
        id_funcionario = self.id_input_funcionario.text()
        
        funcionario = session.query(Funcionario).filter_by(id=id_funcionario).first()
        if funcionario:
            funcionario.nome = self.nome_funcionario_input.text()
            funcionario.email = self.email_funcionario_input.text()
            funcionario.telefone = self.telefone_funcionario_input.text()
            session.commit()
            QMessageBox.information(self, "Sucesso", "Funcionário atualizado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Funcionário não encontrado!")

    def delete_funcionario(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Deletar Funcionário')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Funcionário:")
        self.id_input_funcionario = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_funcionario)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_delete_funcionario(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_delete_funcionario(self, dialog):
        id_funcionario = self.id_input_funcionario.text()
        
        funcionario = session.query(Funcionario).filter_by(id=id_funcionario).first()
        if funcionario:
            session.delete(funcionario)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Funcionário deletado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Funcionário não encontrado!")

# ----------------- FUNÇÕES USUARIO CRUD -----------------

    def create_usuario(self):
        nome = self.nome_usuario_input.text()
        email = self.email_usuario_input.text()
        senha = self.senha_usuario_input.text()
        role = self.role_usuario_input.currentText()  

        # Verifica se todos os campos estão preenchidos
        if nome and email and senha:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha, role=role)
            session.add(novo_usuario)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Usuário criado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")

    def read_usuarios(self):
        usuarios = session.query(Usuario).all()
        if usuarios:
            usuario_info = "\n".join([f"ID: {usuario.id}, Nome: {usuario.nome}, Email: {usuario.email}, Role: {usuario.role}" for usuario in usuarios])
            QMessageBox.information(self, "Usuários", usuario_info)
        else:
            QMessageBox.warning(self, "Erro", "Nenhum usuário encontrado!")

    def update_usuario(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Atualizar Usuário')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Usuário:")
        self.id_input_usuario = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_usuario)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_update_usuario(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_update_usuario(self, dialog):
        id_usuario = self.id_input_usuario.text()
        
        usuario = session.query(Usuario).filter_by(id=id_usuario).first()
        if usuario:
            nome = self.nome_usuario_input.text()
            email = self.email_usuario_input.text()
            senha = self.senha_usuario_input.text()
            role = self.role_usuario_input.currentText()  # Alterado para usar currentText()

            # Verifica se os campos estão preenchidos
            if nome and email and senha:
                usuario.nome = nome
                usuario.email = email
                usuario.senha = senha
                usuario.role = role
                session.commit()
                QMessageBox.information(self, "Sucesso", "Usuário atualizado com sucesso!")
                dialog.close()
            else:
                QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")
        else:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado!")

    def delete_usuario(self):
        id_dialog = QDialog()
        id_dialog.setWindowTitle('Deletar Usuário')

        layout = QVBoxLayout()

        id_label = QLabel("ID do Usuário:")
        self.id_input_usuario = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input_usuario)

        confirm_btn = QPushButton('Confirmar')
        confirm_btn.clicked.connect(lambda: self.perform_delete_usuario(id_dialog))
        layout.addWidget(confirm_btn)

        id_dialog.setLayout(layout)
        id_dialog.exec_()

    def perform_delete_usuario(self, dialog):
        id_usuario = self.id_input_usuario.text()
        
        usuario = session.query(Usuario).filter_by(id=id_usuario).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Usuário deletado com sucesso!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado!")


# ----------------- ÁLGEBRA RELACIONAL -----------------

    # Adicionar aba de consulta SQL após login
    def create_query_tab(self):
        query_widget = QWidget()
        layout = QVBoxLayout()

        # ComboBox para selecionar o tipo de consulta
        self.query_select = QComboBox()
        self.query_select.addItem("Selecione uma consulta")
        self.query_select.addItem("Consulta: Todos os Clientes")
        self.query_select.addItem("Consulta: Todos os Produtos")
        self.query_select.addItem("Consulta: Todos os Fornecedores")
        self.query_select.addItem("Consulta: Clientes por Nome")
        self.query_select.addItem("Consulta: Produtos em Estoque")
        self.query_select.addItem("Consulta: Fornecedores por Telefone")

        # ComboBox para o operador (usado para consultas avançadas)
        self.query_operator = QComboBox()
        self.query_operator.addItem(">")
        self.query_operator.addItem("<")
        self.query_operator.addItem(">=")
        self.query_operator.addItem("<=")
        self.query_operator.addItem("=")
        self.query_operator.addItem("!=")

        # Campo para o nome do campo de pesquisa
        self.query_field = QComboBox()
        self.query_field.addItem("quantidade")
        self.query_field.addItem("preco")

        # Campo para entrada de valor
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Digite o valor da pesquisa...")

        # Botão para executar a consulta
        self.query_btn = QPushButton("Executar Consulta")
        self.query_btn.clicked.connect(self.execute_query)

        # Campo para mostrar o resultado da consulta
        self.query_result = QLabel("Resultado da consulta")
        self.query_result.setWordWrap(True)

        # Adicionando widgets ao layout
        layout.addWidget(QLabel("Selecione a consulta:"))
        layout.addWidget(self.query_select)
        layout.addWidget(QLabel("Escolha o campo (para Produtos em Estoque):"))
        layout.addWidget(self.query_field)
        layout.addWidget(QLabel("Escolha o operador (para Produtos em Estoque):"))
        layout.addWidget(self.query_operator)
        layout.addWidget(QLabel("Digite o valor para pesquisa:"))
        layout.addWidget(self.query_input)
        layout.addWidget(self.query_btn)
        layout.addWidget(QLabel("Resultado da consulta:"))
        layout.addWidget(self.query_result)

        query_widget.setLayout(layout)
        return query_widget

    def execute_query(self):
        selected_query = self.query_select.currentText()

        # Caso o usuário tenha escolhido uma consulta predefinida
        try:
            if selected_query == "Consulta: Todos os Clientes":
                query = "SELECT * FROM clientes"
                params = {}

            elif selected_query == "Consulta: Todos os Produtos":
                query = "SELECT * FROM produtos"
                params = {}

            elif selected_query == "Consulta: Todos os Fornecedores":
                query = "SELECT * FROM fornecedores"
                params = {}

            elif selected_query == "Consulta: Clientes por Nome":
                query = "SELECT * FROM clientes WHERE nome LIKE :nome"
                params = {'nome': f"%{self.query_input.text()}%"}

            elif selected_query == "Consulta: Produtos em Estoque":
                field = self.query_field.currentText()  # Campo: "quantidade" ou "preco"
                operator = self.query_operator.currentText()  # Operador: ">", "<", etc.
                value = self.query_input.text()  # Valor digitado pelo usuário

                # Construindo a consulta dinamicamente
                query = f"SELECT * FROM produtos WHERE {field} {operator} :value"
                params = {'value': value}

            elif selected_query == "Consulta: Fornecedores por Telefone":
                query = "SELECT * FROM fornecedores WHERE telefone LIKE :telefone"
                params = {'telefone': f"%{self.query_input.text()}%"}

            else:
                self.query_result.setText("Selecione uma consulta válida.")
                return

            # Executando a consulta
            result = session.execute(text(query), params).fetchall()

            # Formatando e exibindo o resultado
            result_str = "\n".join([str(row) for row in result])
            self.query_result.setText(result_str if result else "Nenhum resultado encontrado.")

        except Exception as e:
            self.query_result.setText(f"Erro ao executar consulta: {e}")
# ----------------- COMANDO FINAL -----------------
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gui = MercadoGui()
    gui.show()
    sys.exit(app.exec_())



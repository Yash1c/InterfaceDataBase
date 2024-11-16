from PyQt5.QtWidgets import QFormLayout, QDialog, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTabWidget, QMessageBox, QScrollArea, QHBoxLayout
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do banco de dados com SQLAlchemy para MariaDB
username = 'root'
password = '1234'
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

# -------------------------------------------------------

# Criando a base do banco
Base.metadata.create_all(engine)

# Interface gráfica com PyQt5
class MercadoGui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Mercado Gui")

        layout = QVBoxLayout()
        tab_widget = QTabWidget()

        tab_widget.addTab(self.create_cliente_tab(), "Cliente")
        tab_widget.addTab(self.create_produto_tab(), "Produto")
        tab_widget.addTab(self.create_fornecedor_tab(), "Fornecedor")
        tab_widget.addTab(self.create_funcionario_tab(), "Funcionário")

        layout.addWidget(tab_widget)
        self.setLayout(layout)

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

# ----------------- ÁLGEBRA RELACIONAL -----------------

    


# ----------------- COMANDO FINAL -----------------
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gui = MercadoGui()
    gui.show()
    sys.exit(app.exec_())

# ----------------- SCROLL -----------------
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Interface de rolagem")
#         self.setGeometry(100, 100, 400, 500)

#         scroll_area = QScrollArea(self)
#         scroll_area.setWidgetResizable(True)

#         ccontent_widget = QWidget()
#         content_layout = QVBoxLayout(ccontent_widget)

#         for i in range(20):
#             button = QPushButton(f"Botão {i+1}")
#             content_layout.addWidget(button)

#         scroll_area.setWidget(ccontent_widget)

#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(scroll_area)

#         self.setLayout(main_layout)

# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()





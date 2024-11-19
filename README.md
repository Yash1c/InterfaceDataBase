
# 🛒 Gerenciador de Mercado com Interface Gráfica  
**Projeto de Estudo para Gerenciamento de Banco de Dados**  

## 📖 Sobre o Projeto  
Este projeto foi desenvolvido como parte dos estudos acadêmicos em **banco de dados** e **desenvolvimento de software**. Ele é uma aplicação desktop em **Python**, utilizando as bibliotecas **Tkinter** e **SQLAlchemy**, com o objetivo de gerenciar dados de um mercado, como **clientes**, **produtos**, **pedidos** e **fornecedores**.  

Além de realizar operações CRUD, o projeto também explora conceitos fundamentais como:  
- **Álgebra Relacional** para consultas dinâmicas.  
- **Controle de Acesso** para diferentes níveis de usuários.  
- **Gerenciamento de Transações** para garantir a integridade dos dados.  

Este projeto é **exclusivamente educacional**, buscando consolidar práticas e habilidades essenciais em **desenvolvimento e gerenciamento de banco de dados**.
## 🔧 Funcionalidades  
- 📋 **CRUD Completo**: Criar, Ler, Atualizar e Deletar dados no banco de dados.  
- 🕵️‍♂️ **Consultas Dinâmicas**: Executar consultas personalizadas usando álgebra relacional.  
- 🔒 **Controle de Acesso**: Diferentes permissões para administradores, operadores e visualizadores.  
- 💾 **Transações ACID**: Garantia de consistência em operações críticas.  
- 🎨 **Interface Gráfica Intuitiva**: Criada em Tkinter para facilitar o uso.

---

## 🛠️ Tecnologias Utilizadas  
- **Python 3.x**  
- **Tkinter** (Interface Gráfica)  
- **SQLAlchemy** (ORM para interação com banco de dados)  
- **MariaDB/MySQL** (Banco de Dados Relacional)  
- **bcrypt** (Criptografia de Senhas)  

---

## 📚 Objetivo  
Este projeto tem como principal objetivo fortalecer o aprendizado sobre:  
- Estrutura e manipulação de bancos de dados relacionais.  
- Conceitos teóricos e práticos de álgebra relacional.  
- Desenvolvimento de interfaces gráficas com Python.  
- Implementação de boas práticas em segurança e gerenciamento de dados.  

---

## 🖥️ Execução do Projeto  
1. **Clone o Repositório**  
   ```bash
   git clone https://github.com/seu-usuario/projeto-gerenciador-mercado.git
   cd projeto-gerenciador-mercado
   ```  
2. **Instale as Dependências**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Configure o Banco de Dados**  
   - Certifique-se de que o MariaDB/MySQL está configurado e funcionando.  
   - Atualize as configurações de conexão no arquivo `config.py`.  

4. **Execute o Projeto**  
   ```bash
   python main.py
   ```  

---

## 📝 Observações  
- Este projeto **não deve ser utilizado em produção**.  
- É um projeto de estudo focado no aprendizado e na aplicação de conceitos teóricos.  

---

# 🛒 Market Manager with GUI  
**Study Project for Database Management**  

## 📖 About the Project  
This project was developed as part of academic studies in **databases** and **software development**. It is a desktop application built in **Python**, using **Tkinter** and **SQLAlchemy**, to manage market data such as **customers**, **products**, **orders**, and **suppliers**.  

In addition to CRUD operations, the project explores key concepts like:  
- **Relational Algebra** for dynamic queries.  
- **Access Control** for different user levels.  
- **Transaction Management** to ensure data integrity.  

This project is purely **educational**, aiming to consolidate essential skills and practices in **database management and development**.

---

## 🔧 Features  
- 📋 **Complete CRUD**: Create, Read, Update, and Delete data in the database.  
- 🕵️‍♂️ **Dynamic Queries**: Execute customized queries using relational algebra.  
- 🔒 **Access Control**: Different permissions for admins, operators, and viewers.  
- 💾 **ACID Transactions**: Ensure consistency in critical operations.  
- 🎨 **Intuitive GUI**: Built with Tkinter for ease of use.

---

## 🛠️ Technologies Used  
- **Python 3.x**  
- **Tkinter** (Graphical User Interface)  
- **SQLAlchemy** (ORM for database interaction)  
- **MariaDB/MySQL** (Relational Database)  
- **bcrypt** (Password Encryption)  

---

## 📚 Objective  
This project aims to strengthen knowledge on:  
- Structuring and managing relational databases.  
- Theoretical and practical concepts of relational algebra.  
- GUI development with Python.  
- Implementing best practices in security and data management.  

---

## 🖥️ How to Run the Project  
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/market-manager-project.git
   cd market-manager-project
   ```  
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Configure the Database**  
   - Ensure MariaDB/MySQL is set up and running.  
   - Update the connection settings in the `config.py` file.  

4. **Run the Project**  
   ```bash
   python main.py
   ```  

---

## 📝 Notes  
- This project **should not be used in production**.  
- It is a study-focused project, aimed at learning and applying theoretical concepts.  

---

**Atualização do README para incluir suporte ao SQLite (Português e Inglês):**

---

### 🇧🇷 **Para Configurar com SQLite**

O projeto também oferece suporte ao banco de dados SQLite para maior simplicidade durante os testes e aprendizado. Siga os passos abaixo para configurar o projeto utilizando SQLite:

#### 📂 Configuração com SQLite
1. Certifique-se de ter o SQLite3 instalado no seu sistema.
2. Atualize o arquivo `main.py` ou `interface.py` substituindo a configuração de banco de dados existente pela seguinte:
   ```python
   engine = create_engine('sqlite:///mercado_gui.db')
   ```
3. Não é necessário configurar usuário, senha ou host para SQLite.

#### 🖥️ Execução com SQLite
Após ajustar o código, siga os passos normais de execução:
```bash
python main.py
```

---

### 🇺🇸 **Configuring with SQLite**

The project also supports SQLite for simpler testing and learning purposes. Follow the steps below to set up the project using SQLite:

#### 📂 SQLite Configuration
1. Ensure SQLite3 is installed on your system.
2. Update the `main.py` or `interface.py` file, replacing the existing database configuration with:
   ```python
   engine = create_engine('sqlite:///mercado_gui.db')
   ```
3. There is no need to configure a username, password, or host for SQLite.

#### 🖥️ Running with SQLite
After adjusting the code, follow the standard execution steps:
```bash
python main.py
```

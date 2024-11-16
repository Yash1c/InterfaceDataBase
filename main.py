from PyQt5.QtWidgets import QApplication
from interface import MercadoGui

def main():
    import sys
    app = QApplication(sys.argv)

    # Criar uma instância da interface MercadoGui
    mercado_window = MercadoGui()
    mercado_window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



from banco.banco import SistemaDB
from telas.telas import TelaInicial

if __name__ == "__main__":
    banco = SistemaDB()
    TelaInicial(banco)
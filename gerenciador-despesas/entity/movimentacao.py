from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Movimentacao:
    descricao:str
    tipo:str
    valor:Decimal

    #& __post_init__ após rodar  o __init__ passa pelo post init que realiza validações de dados, etc...
    #& raise usada para lançar exceção, que o código por fora usa do try/except para capturar a excessão lançada
    #& ValueError é um tipo de excessão usada para mostrar um valor inadequado para operação
    def __post_init__(self):
        if not self.descricao or self.descricao.strip() == "":
            raise ValueError("Descrição não pode ser vazia")
        

    #* Retorna o valor de acordo com o tipo da movimentação
    def calcular_valor_assinado(self) -> Decimal:
        if self.tipo == "despesa":
            return -self.valor

        return self.valor

    #* Retorna o objeto referenciado é uma receita ou não
    def eh_receita(self) -> bool:
        if self.tipo == "receita":
            return True
        return False

    #* Exibe um resumo em string
    def exibir_resumo(self) -> str:
        return f"{self.descricao} | {self.tipo} | R$ {self.valor:.2f}"
        

receita = Movimentacao("Salário", "receita", Decimal("3500.00"))
despesa = Movimentacao("Mercado", "despesa", Decimal("250.00"))


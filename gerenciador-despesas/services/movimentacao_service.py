from decimal import Decimal
from repositories.movimentacao_repository import MovimentacaoRepository


class MovimentacaoService:
    #& Aqui se recebe a classe de repositório pronto;
    #& Isso é uma injeção de dependencia por construtor
    def __init__(self, repositorio: MovimentacaoRepository):
        self.repositorio = repositorio

    def calcular_saldo(self) -> Decimal:
        movimentacoes = self.repositorio.listar()

        # valores = [] 

        # for movimentacao in movimentacoes:
        #     valores.append(movimentacao.calcular_valor_assinado())
        
        # return Decimal(sum(valores))

        #! Outra forma de chagar ao mesmo resultado usando um "generator expression" porém economizando em variáveis intermediarias como os "valores" e um for deixando toda a execução mais simples
        return sum((mov.calcular_valor_assinado() for mov in movimentacoes),Decimal("0"))

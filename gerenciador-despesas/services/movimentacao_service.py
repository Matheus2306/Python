from decimal import Decimal, InvalidOperation
from repositories.movimentacao_repository import MovimentacaoRepository
from entity.movimentacao import Movimentacao


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

    def cadastrar(
        self, 
        descricao: str,
        tipo: str,
        valor: Decimal
        ) -> Movimentacao:

        movimentacao = Movimentacao(
            descricao= descricao,
            tipo= tipo,
            valor= valor
            )
        self.repositorio.salvar(movimentacao)
        return movimentacao

    def listar_movimentacoes(self) -> list[Movimentacao]:
        return self.repositorio.listar()

    def filtrar_por_tipo(self, tipo: str) -> list[Movimentacao]:
        
        normalizado = tipo.strip().upper()

        if normalizado not in ("R", "D"):
            raise ValueError("Selecione R para receita ou D para despesa.")
        
        tipo_selecionado = "receita" if normalizado == "R" else "despesa"

        movimentacoes = self.repositorio.listar()

        filtrados = []

        for mov in movimentacoes:
            if mov.tipo == tipo_selecionado:
                filtrados.append(mov)

        return filtrados
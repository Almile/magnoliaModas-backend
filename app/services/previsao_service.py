from app.routes.ml import SalesPredictor 
class PrevisaoService:
    def __init__(self):
        self.engine = SalesPredictor()

    def gerar_relatorio_compras(self, db):
        """
        Esta função faz o passo-a-passo para criar o relatório.
        """

        dados_vendas = [
            {"produto_id": 1, "data": "2024-01-01", "quantidade": 5},
            {"produto_id": 1, "data": "2024-01-08", "quantidade": 2},
            {"produto_id": 2, "data": "2024-01-01", "quantidade": 10},
            {"produto_id": 3, "data": "2024-01-08", "quantidade": 17},
            {"produto_id": 4, "data": "2024-01-01", "quantidade": 1},
            {"produto_id": 5, "data": "2024-01-08", "quantidade": 7},
        ]

        self.engine.treinar(dados_vendas)
        relatorio = []

        produtos = [{"id": 1, "nome": "Camiseta Branca", "estoque_atual": 5},
                    {"id": 2, "nome": "Calça Jeans", "estoque_atual": 8},
                    {"id": 3, "nome": "Vestido Floral", "estoque_atual": 15},
                    {"id": 4, "nome": "Jaqueta de Couro", "estoque_atual": 0},
                    {"id": 5, "nome": "Tênis Esportivo", "estoque_atual": 3}]


        for p in produtos:
            previsao_venda = self.engine.prever_proximo_periodo(p['id'])
            
            qtd_comprar = previsao_venda - p['estoque_atual']
            
            if qtd_comprar > 0:
                relatorio.append({
                    "produto": p['nome'],
                    "previsao_vendas": previsao_venda,
                    "estoque_hoje": p['estoque_atual'],
                    "sugestao_compra": qtd_comprar
                })

        return relatorio
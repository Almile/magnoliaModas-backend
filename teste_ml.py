import sys
import os
from app.services.previsao_service import SalesPredictor
import pandas as pd

sys.path.append(os.getcwd()) 

dados_falsos = pd.DataFrame([
       {"produto_id": 1, "data": "2024-01-01", "quantidade": 5},
       {"produto_id": 1, "data": "2024-01-08", "quantidade": 2},
       {"produto_id": 2, "data": "2024-01-01", "quantidade": 10},
       {"produto_id": 3, "data": "2024-01-08", "quantidade": 17},
       {"produto_id": 4, "data": "2024-01-01", "quantidade": 1},
       {"produto_id": 5, "data": "2024-01-08", "quantidade": 7},
])

print("Treinando o modelo...")
brain = SalesPredictor()
brain.treinar(dados_falsos)

resultado = brain.prever_proximo_periodo(produto_id=1)
resultado2 = brain.prever_proximo_periodo(produto_id=2)
resultado3= brain.prever_proximo_periodo(produto_id=3)
resultado4 = brain.prever_proximo_periodo(produto_id=4)
resultado5 = brain.prever_proximo_periodo(produto_id=5)

print(f"\n--- RESULTADO DO TESTE ---")
print(f"Previsão de vendas para o Produto 1: {resultado} unidades")
print(f"Previsão de vendas para o Produto 2: {resultado2} unidades")
print(f"Previsão de vendas para o Produto 3: {resultado3} unidades")
print(f"Previsão de vendas para o Produto 4: {resultado4} unidades")
print(f"Previsão de vendas para o Produto 5: {resultado5} unidades")
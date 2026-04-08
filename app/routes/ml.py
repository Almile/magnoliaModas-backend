import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import datetime

class SalesPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def preparar_dados(self, dados_vendas):
        df = pd.DataFrame(dados_vendas)
        df['data'] = pd.to_datetime(df['data'])
        df['mes'] = df['data'].dt.month
        df['dia_semana'] = df['data'].dt.dayofweek
        return df

    def treinar(self, dados_vendas):
        df = self.preparar_dados(dados_vendas)
        X = df[['produto_id', 'mes', 'dia_semana']]
        y = df['quantidade']
        self.model.fit(X, y)

    def prever_proximo_periodo(self, produto_id):
        hoje = datetime.datetime.now()
        X_novo = pd.DataFrame([[produto_id, hoje.month, hoje.weekday()]], 
                              columns=['produto_id', 'mes', 'dia_semana'])
        previsao = self.model.predict(X_novo)
        return round(previsao[0])
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('transacoes.csv', encoding='latin1')

df['valor'] = df.groupby('estado_cliente')['valor'].transform(
    lambda x: x.fillna(x.median())
)

df['plataforma'] = 'Mobile'

df['data_transacao'] = pd.to_datetime(df['data_transacao'])
df['data_transacao'] = df['data_transacao'].dt.tz_localize('America/Sao_Paulo')

df['dia_semana'] = df['data_transacao'].dt.day_name()
df['mes']        = df['data_transacao'].dt.month

df.drop_duplicates(keep='first', inplace=True)


filtro_setembro = (
    (df['mes'] == 9) &
    ((df['estado_cliente'] == 'SP') | (df['estado_cliente'] == 'RJ')) &
    (df['valor'] > 5000)
)
df_setembro_filtrado = df[filtro_setembro].copy()

print(f"Transações filtradas (Set/SP-RJ/>5k): {len(df_setembro_filtrado)}")


risco_dict = {'C100': 'Baixo', 'C101': 'Alto', 'C102': 'Médio',
              'C103': 'Alto',  'C104': 'Baixo'}

df['nivel_risco'] = df['id_cliente'].map(risco_dict)

pivot = pd.pivot_table(
    df,
    values='valor',
    index='mes',
    columns='nivel_risco',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
)

print("\nPivot Table — Soma de Valor por Mês e Nível de Risco:")
print(pivot.to_string())


def zscore_por_estado(series):
    return (series - series.mean()) / series.std()

df['zscore'] = df.groupby('estado_cliente')['valor'].transform(zscore_por_estado)

df_anomalias = df[df['zscore'] > 2.5].copy()

print(f"\nAnomalias detectadas (Z > 2.5): {len(df_anomalias)}")
print(df_anomalias[['id_cliente', 'data_transacao', 'valor', 'estado_cliente', 'zscore']].head(10).to_string())

df_diario = (
    df.set_index('data_transacao')['valor']
    .resample('D')
    .sum()
    .reset_index()
)
df_diario['media_movel_7d'] = df_diario['valor'].rolling(7).mean()

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df_diario['data_transacao'], df_diario['valor'],
        label='Valor Total Diário', alpha=0.6, linewidth=1.2)
ax.plot(df_diario['data_transacao'], df_diario['media_movel_7d'],
        label='Média Móvel 7 dias', linewidth=2, color='red')

ax.set_ylim(bottom=0)
ax.set_title('Valor Total de Transações Diárias com Média Móvel de 7 Dias')
ax.set_xlabel('Data')
ax.set_ylabel('Valor (R$)')
ax.legend()
fig.tight_layout()
plt.savefig('relatorio_transacoes.png', dpi=150)
plt.show()

print("\nGráfico salvo em 'relatorio_transacoes.png'")

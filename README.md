# Análise de Transações Financeiras — Fintech

Projeto de Ciência de Dados para limpeza, transformação, consolidação e visualização de dados de transações financeiras.

## Requisitos

```bash
pip install pandas numpy matplotlib
```

## Como executar

```bash
# 1. Gerar os dados
python criar_dados.py

# 2. Executar a análise
python solucao.py
```

## O que o script faz

- **Ingestão & Limpeza**: leitura com encoding `latin1`, imputação de valores ausentes pela mediana por estado
- **Engenharia Temporal**: conversão para `datetime64` com fuso `America/Sao_Paulo`, extração de dia da semana e mês
- **Filtros Bitwise**: filtra transações de setembro em SP/RJ com valor > R$ 5.000 usando operadores `&` e `|`
- **Pivot Table**: agrupamento por mês e nível de risco com subtotais
- **Detecção de Anomalias**: Z-Score vetorizado por estado, identifica transações com Z > 2.5
- **Visualização**: gráfico com valor diário total e média móvel de 7 dias (API OO do Matplotlib)

## Saídas

- Console: pivot table, contagem de anomalias e registros filtrados
- `relatorio_transacoes.png`: gráfico de série temporal gerado automaticamente

# Annual Expense Analyzer

A simple Python program that reads a CSV file of personal expenses and generates a report with monthly totals, spending by category, the biggest purchase of the year, and a comparison against a budget. It also generates two bar charts.

## About this project

This was the final project of a Python course offered by ICMC Júnior (USP São Carlos) in partnership with InfoBio Jr. I came from a C background and had almost no experience with Python before this, so this was my first real contact with the language, and with libraries like pandas and matplotlib. Still learning, but I'm happy with how this one came out.

## How to run

```bash
pip install pandas matplotlib
python analisador_despesas.py
```

The program will ask for the path to a CSV file and your annual budget.

## CSV format

```
Data,Categoria,Valor
01/01,Comida,50.00
03/01,Transporte,25.50
```

## What it generates

- `relatorio.txt` — text report with all the totals and comparisons
- `gastos_por_mes.png` — bar chart of spending by month
- `gastos_por_categoria.png` — bar chart of spending by category

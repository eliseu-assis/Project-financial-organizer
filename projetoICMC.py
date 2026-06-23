import csv
import pandas as pd
import matplotlib.pyplot as plt
import sys

def ler_csv(caminho_arquivo):
    try:
        dados = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Erro: o arquivo CSV está vazio.")
        sys.exit(1)

    colunas_esperadas = ["Data", "Categoria", "Valor"]
    for coluna in colunas_esperadas:
        if coluna not in dados.columns:
            print(f"Erro: coluna obrigatória '{coluna}' não encontrada no CSV.")
            sys.exit(1)

    dados["Valor"] = pd.to_numeric(dados["Valor"], errors="coerce")
    linhas_invalidas = dados["Valor"].isna().sum()
    if linhas_invalidas > 0:
        print(f"Aviso: {linhas_invalidas} linha(s) com valor inválido foram ignoradas.")
        dados = dados.dropna(subset=["Valor"])

    return dados

def obter_orcamento():
    while True:
        entrada = input("Informe seu orçamento anual: ")
        try:
            orcamento = float(entrada)
            return orcamento
        except ValueError:
            print("Valor inválido. Digite um número, por exemplo: 30000 ou 30000.50")

def calcular_gastos_por_mes(dados):
    dados["Mes"] = dados["Data"].str.split("/").str[1]    #pegar o nro do mes na posicao [1] dia/mes e cria uma coluna 'mes'
    gastos_por_mes = dados.groupby("Mes")["Valor"].sum()  #agrupa as linhas que tem o mesmo valor da coluna mes
    return gastos_por_mes

def encontrar_maior_compra(dados):
    indice_maior = dados["Valor"].idxmax()     #idmax vai percorrer a coluna valor e retornar o indice  q tem valor maximo
    maior_compra = dados.loc[indice_maior]     #o loc vai dar a linha inteira do indice_maior
    return maior_compra

def calcular_gastos_por_categoria(dados):
    gastos_por_categoria = dados.groupby("Categoria")["Valor"].sum()  #agrupa as categorias e em cada grupo soma .sum
    return gastos_por_categoria       #resultado será uma series

def calcular_total_anual(dados):
    total = dados["Valor"].sum()
    return total

def comparar_orcamento(total, orcamento):
    if total <= orcamento:
        diferenca = orcamento - total
        mensagem = f"Parabéns! Você ficou R$ {diferenca:.2f} abaixo do orçamento."
    else:
        diferenca = total - orcamento
        mensagem = f"Atenção! Você excedeu o orçamento em R$ {diferenca:.2f}."
    return mensagem

def gerar_graficos(gastos_por_mes, gastos_por_categoria):
    # Gráfico 1: gastos por mês
    plt.figure()
    gastos_por_mes.plot(kind="bar", color="steelblue")
    plt.title("Total Gasto por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Valor Gasto (R$)")
    plt.xticks(rotation=0)      #deixa na horizontal, sem rotacao
    plt.tight_layout()
    plt.savefig("gastos_por_mes.png")
    plt.close()

    # Gráfico 2: gastos por categoria
    plt.figure()
    gastos_por_categoria.plot(kind="bar", color="darkorange")
    plt.title("Total Gasto por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Valor Gasto (R$)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("gastos_por_categoria.png")
    plt.close()

def gerar_relatorio(gastos_por_mes, maior_compra, gastos_por_categoria, total_anual, mensagem_orcamento):
    nomes_meses = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }

    with open("relatorio.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("=== RELATÓRIO DE DESPESAS ANUAL ===\n\n")

        arquivo.write("--- Total Gasto por Mês ---\n")
        for mes, valor in gastos_por_mes.items():       #o items devolve indice-valor pois gasto_mes é uma series mes-total
            arquivo.write(f"{nomes_meses[mes]}: R$ {valor:.2f}\n")
        arquivo.write("\n")

        arquivo.write("--- Maior Compra ---\n")
        arquivo.write(f"Data: {maior_compra['Data']}\n")   #maior_compra é uma variavel da linha toda, ele vai na 'Data' e imprime oq tem la
        arquivo.write(f"Categoria: {maior_compra['Categoria']}\n")
        arquivo.write(f"Valor: R$ {maior_compra['Valor']:.2f}\n\n")

        arquivo.write("--- Gastos por Categoria ---\n")
        for categoria, valor in gastos_por_categoria.items():
            arquivo.write(f"{categoria}: R$ {valor:.2f}\n")
        arquivo.write("\n")

        arquivo.write(f"--- Total Anual ---\nR$ {total_anual:.2f}\n\n")

        arquivo.write("--- Comparação com Orçamento ---\n")
        arquivo.write(mensagem_orcamento + "\n")

    print("Relatório gerado com sucesso!")
    print("Arquivo salvo em: relatorio.txt")

def main():
    print("=== ANALISADOR DE DESPESAS ANUAL ===\n")

    caminho_arquivo = input("Informe o caminho do arquivo CSV: ")
    dados = ler_csv(caminho_arquivo)

    orcamento = obter_orcamento()

    print("\nProcessando dados...\n")

    gastos_mes = calcular_gastos_por_mes(dados)
    maior_compra = encontrar_maior_compra(dados)
    gastos_categoria = calcular_gastos_por_categoria(dados)
    total_anual = calcular_total_anual(dados)
    mensagem_orcamento = comparar_orcamento(total_anual, orcamento)

    gerar_graficos(gastos_mes, gastos_categoria)
    gerar_relatorio(gastos_mes, maior_compra, gastos_categoria, total_anual, mensagem_orcamento)

    print("Gráficos salvos na pasta atual.")


if __name__ == "__main__":
    main()
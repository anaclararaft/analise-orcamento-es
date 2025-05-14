import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario

def identificar_colunas_ano(df):
    return [col for col in df.columns if col.isdigit()]

def obter_linha(df, nome):
    linha = df[df['Descricao'].str.lower() == nome.lower()]
    return linha if not linha.empty else None

def main():
    print("📈 Gerador de Indicadores Macrofiscais")

    df = pd.read_csv(selecionar_arquivo_temporario())
    col_anos = identificar_colunas_ano(df)

    # Linhas necessárias
    linhas_necessarias = {
        "Gasto Social": None,
        "Despesas Não Financeiras": None,
        "Gasto Financeiro": None,
        "Total da Despesa": None,
        "Gasto Tributário": None  # opcional
    }

    for nome in linhas_necessarias:
        linha = obter_linha(df, nome)
        if linha is None and nome != "Gasto Tributário":
            print(f"❌ Linha obrigatória ausente: '{nome}'")
            return
        linhas_necessarias[nome] = linha

    # Indicadores
    indicadores = []

    gs = linhas_necessarias["Gasto Social"]
    dnf = linhas_necessarias["Despesas Não Financeiras"]
    gf = linhas_necessarias["Gasto Financeiro"]
    td = linhas_necessarias["Total da Despesa"]
    gt = linhas_necessarias["Gasto Tributário"]

    indicadores.append({
        "Descricao": "Gasto Social / Despesa Não Financeira",
        **{ano: gs[ano].values[0] / dnf[ano].values[0] if dnf[ano].values[0] else None for ano in col_anos}
    })

    indicadores.append({
        "Descricao": "Gasto Social / Total da Despesa",
        **{ano: gs[ano].values[0] / td[ano].values[0] if td[ano].values[0] else None for ano in col_anos}
    })

    indicadores.append({
        "Descricao": "Gasto Financeiro / Total da Despesa",
        **{ano: gf[ano].values[0] / td[ano].values[0] if td[ano].values[0] else None for ano in col_anos}
    })

    if gt is not None:
        indicadores.append({
            "Descricao": "Gasto Tributário / Total da Despesa",
            **{ano: gt[ano].values[0] / td[ano].values[0] if td[ano].values[0] else None for ano in col_anos}
        })

    df_indicadores = pd.DataFrame(indicadores)

    print("\n📊 Indicadores calculados:")
    print(df_indicadores.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/saida', exist_ok=True)
    nome_saida = f'indicadores_{agora}.csv'
    df_indicadores.to_csv(os.path.join('dados/saida', nome_saida), index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo salvo em: dados/saida/{nome_saida}")

if __name__ == '__main__':
    main()

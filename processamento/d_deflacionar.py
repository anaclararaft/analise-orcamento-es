import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario

def carregar_deflatores(caminho='dados/deflator.txt'):
    df = pd.read_csv(caminho, sep=';', header=None, names=['ano', 'indice'])
    return dict(zip(df['ano'].astype(str), df['indice']))

def main():
    print("📉 Deflacionador de Valores Monetários")

    df = pd.read_csv(selecionar_arquivo_temporario())
    deflatores = carregar_deflatores()

    anos_disponiveis = list(deflatores.keys())
    print(f"📅 Anos disponíveis: {anos_disponiveis}")
    ano_base = input("👉 Escolha o ano base (ex: 2022): ").strip()

    if ano_base not in deflatores:
        print(f"❌ Ano base '{ano_base}' não encontrado no índice de deflação.")
        return

    fator_base = deflatores[ano_base]
    col_anos = [col for col in df.columns if col.isdigit()]
    conversoes_nan = {}

    for ano in col_anos:
        if ano in deflatores:
            try:
                fator_ano = deflatores[ano]
                antes_nan = df[ano].isna().sum()
                df[ano] = df[ano] / (fator_ano / fator_base)
                depois_nan = df[ano].isna().sum()
                novos_nans = depois_nan - antes_nan
                if novos_nans > 0:
                    conversoes_nan[ano] = novos_nans
            except Exception as e:
                print(f"⚠️ Erro ao aplicar deflator para {ano}: {e}")
        else:
            print(f"⚠️ Ano {ano} não encontrado no índice. Ignorado.")

    if conversoes_nan:
        print("\n⚠️ Valores inválidos convertidos em NaN durante deflação:")
        for ano, qtde in conversoes_nan.items():
            print(f"   → {ano}: {qtde} valores")

    print("\n🔍 Preview após deflação:")
    print(df.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/temporario', exist_ok=True)
    nome_saida = f'dados-deflacionado-{agora}.csv'
    df.to_csv(os.path.join('dados/temporario', nome_saida), index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo salvo em: dados/temporario/{nome_saida}")

if __name__ == '__main__':
    main()

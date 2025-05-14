import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario
from processamento.normalizador import normalizar_coluna

def main():
    print("🧼 Normalizador de Dados Textuais")

    caminho = selecionar_arquivo_temporario()
    df = pd.read_csv(caminho)

    print("\n📄 Colunas disponíveis:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    selecao = input("\n👉 Digite os números das colunas a normalizar (ex: 1,3): ")
    indices = [int(i.strip()) - 1 for i in selecao.split(',') if i.strip().isdigit()]
    colunas_escolhidas = [df.columns[i] for i in indices if 0 <= i < len(df.columns)]

    if not colunas_escolhidas:
        print("❌ Nenhuma coluna válida selecionada.")
        return

    for col in colunas_escolhidas:
        df = normalizar_coluna(df, col)
        print(f"✅ Coluna '{col}' normalizada.")

    # Verifica colunas de ano
    col_anos = [col for col in df.columns if col.isdigit()]
    col_invalidas = []

    for col in col_anos:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().sum() > 0:
                col_invalidas.append((col, df[col].isna().sum()))

    if col_invalidas:
        print("\n⚠️ Valores não numéricos encontrados e convertidos para NaN:")
        for col, n in col_invalidas:
            print(f"   → {col}: {n} valores")

    print("\n🔍 Preview dos dados normalizados:")
    print(df.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/temporario', exist_ok=True)
    nome_saida = f'dados-padrao-{agora}.csv'
    df.to_csv(os.path.join('dados/temporario', nome_saida), index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo normalizado salvo em: dados/temporario/{nome_saida}")

if __name__ == '__main__':
    main()

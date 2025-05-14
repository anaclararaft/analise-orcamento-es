import pandas as pd
import os
from processamento.utils import selecionar_arquivo_temporario

def identificar_colunas_ano(df):
    return [col for col in df.columns if str(col).isdigit()]

def identificar_valores_invalidos(df, col_anos):
    print("\n🔎 Iniciando verificação de colunas numéricas...\n")
    total_erros = 0

    for col in col_anos:
        print(f"📅 Coluna: {col}")
        serie = df[col].astype(str).str.strip()

        # Detecta valores que não são convertíveis para número
        erros = serie[~serie.str.replace('.', '', regex=False)
                             .str.replace(',', '', regex=False)
                             .str.replace('-', '', regex=False)
                             .str.replace(' ', '', regex=False)
                             .str.match(r'^-?\d+(\.\d+)?$')]

        n_erros = len(erros)
        total_erros += n_erros

        if n_erros == 0:
            print("✅ Nenhum valor inválido.\n")
        else:
            print(f"❌ {n_erros} valores inválidos encontrados.")
            print("🧪 Exemplos:")
            print(erros.value_counts().head(10).to_string())
            print()

    print(f"🔚 Verificação finalizada. Total de valores inválidos: {total_erros}")

def main():
    print("🧪 Verificador de valores numéricos em colunas de ano")
    try:
        caminho = selecionar_arquivo_temporario()
        df = pd.read_csv(caminho)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return

    col_anos = identificar_colunas_ano(df)
    if not col_anos:
        print("⚠️ Nenhuma coluna de ano identificada.")
        return

    identificar_valores_invalidos(df, col_anos)

if __name__ == '__main__':
    main()

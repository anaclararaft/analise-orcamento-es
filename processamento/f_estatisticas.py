import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario
from processamento.utils import calcular_total_despesas


def identificar_colunas_ano(df):
    return [col for col in df.columns if str(col).isdigit()]

def main():
    print("📊 Gerador de Estatísticas por Macroárea (Grupo)")

    caminho = selecionar_arquivo_temporario()
    df = pd.read_csv(caminho)

    if 'Grupo' not in df.columns:
        print("❌ Coluna 'Grupo' não encontrada. Execute a etapa de macroárea antes.")
        return

    col_anos = identificar_colunas_ano(df)

    # Garantir que os valores estão como float
    for col in col_anos:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Detalhado: por Descricao + Grupo
    colunas_detalhado = ['Grupo', 'Descricao'] + col_anos
    df_detalhado = df[colunas_detalhado].copy()
    df_detalhado = df_detalhado.sort_values(['Grupo', 'Descricao'])

    # Resumo: soma por Grupo
    df_resumo = df.groupby('Grupo')[col_anos].sum().reset_index()
    df_total = calcular_total_despesas(df, col_anos)
    df_resumo = pd.concat([df_resumo, df_total], ignore_index=True)

    print("\n📍 Preview: Resumo por Grupo")
    print(df_resumo.head(10))

    print("\n📍 Preview: Detalhado por Descricao")
    print(df_detalhado.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/saida', exist_ok=True)
    df_resumo.to_csv(f'dados/saida/resumo_grupo_{agora}.csv', index=False, encoding='utf-8-sig')
    df_detalhado.to_csv(f'dados/saida/detalhado_grupo_{agora}.csv', index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivos exportados para a pasta dados/saida/ com timestamp {agora}")

if __name__ == '__main__':
    main()

import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario, calcular_total_despesas

def identificar_colunas_ano(df):
    return [col for col in df.columns if str(col).isdigit()]

def selecionar_arquivo_saida():
    arquivos = os.listdir('dados/saida')
    arquivos_csv = [f for f in arquivos if f.endswith('.csv')]

    if not arquivos_csv:
        print("❌ Nenhum CSV encontrado na pasta dados/saida.")
        return None

    print("\n📁 Arquivos disponíveis em dados/saida:")
    for i, nome in enumerate(arquivos_csv):
        print(f"  {i+1}. {nome}")

    opcao = input("👉 Selecione o número do arquivo ao qual deseja adicionar o resumo por grupo: ")
    try:
        idx = int(opcao) - 1
        return os.path.join('dados/saida', arquivos_csv[idx])
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return None

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

    # Resumo: soma por Grupo + total geral
    df_resumo = df.groupby('Grupo')[col_anos].sum().reset_index()
    df_total = calcular_total_despesas(df, col_anos)
    df_resumo = pd.concat([df_resumo, df_total], ignore_index=True)

    print("\n📍 Preview: Resumo por Grupo")
    print(df_resumo.head(10))

    print("\n📍 Preview: Detalhado por Descricao")
    print(df_detalhado.head(10))

    # Exporta detalhado com timestamp
    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/saida', exist_ok=True)
    df_detalhado.to_csv(f'dados/saida/detalhado_grupo_{agora}.csv', index=False, encoding='utf-8-sig')

    # Seleciona arquivo de saída para adicionar o resumo
    caminho_saida = selecionar_arquivo_saida()
    if not caminho_saida:
        return

    try:
        df_existente = pd.read_csv(caminho_saida)
        df_final = pd.concat([df_existente, df_resumo], ignore_index=True)
        df_final.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
        print(f"\n✅ Resumo por grupo adicionado ao arquivo: {caminho_saida}")
    except Exception as e:
        print(f"❌ Erro ao atualizar arquivo destino: {e}")

if __name__ == '__main__':
    main()

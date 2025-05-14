import os
import pandas as pd
import re
from datetime import datetime
from processamento.utils import selecionar_arquivos

def extrair_ano_do_nome(nome_arquivo):
    match = re.search(r'20\d{2}', nome_arquivo)
    return match.group(0) if match else None

def converter_valores_para_float(coluna):
    return (
        coluna.astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .apply(pd.to_numeric, errors='coerce')
    )

def main():
    print("📂 Leitor e Unificador de Arquivos Orçamentários")

    arquivos = selecionar_arquivos()
    if not arquivos:
        print("❌ Nenhum arquivo selecionado.")
        return

    dfs = []
    niveis_detectados = set()

    for caminho in arquivos:
        nome = os.path.basename(caminho)
        ano = extrair_ano_do_nome(nome)

        if not ano:
            print(f"⚠️ Ano não encontrado no nome do arquivo: {nome}")
            continue

        df = pd.read_csv(caminho, sep=None, engine='python')
        colunas = df.columns.tolist()

        if len(colunas) < 2:
            print(f"⚠️ Arquivo com menos de duas colunas: {nome}")
            continue

        descricao = df.iloc[:, 0].astype(str).str.strip()
        valores = converter_valores_para_float(df.iloc[:, -1])

        df_filtrado = pd.DataFrame({
            'Descricao': descricao,
            ano: valores
        })

        dfs.append(df_filtrado)

        print(f"✅ Lido: {nome} com {len(df_filtrado)} linhas.")

    if not dfs:
        print("❌ Nenhum dado válido encontrado.")
        return

    df_geral = dfs[0]
    for df in dfs[1:]:
        df_geral = pd.merge(df_geral, df, on='Descricao', how='outer')

    # Verificação de descrições duplicadas
    duplicadas = df_geral['Descricao'].duplicated().sum()
    if duplicadas > 0:
        print(f"⚠️ {duplicadas} descrições duplicadas detectadas após a unificação.")

    print("\n📌 Estrutura do dataframe final:")
    print(df_geral.dtypes)
    print(df_geral.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs("dados/temporario", exist_ok=True)
    nome_saida = f"dados-leitor-{agora}.csv"
    caminho_saida = os.path.join("dados/temporario", nome_saida)

    df_geral.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
    print(f"\n✅ Arquivo unificado salvo em: {caminho_saida}")

if __name__ == '__main__':
    main()

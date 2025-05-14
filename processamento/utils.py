import os
import pandas as pd
from tkinter import Tk, filedialog
import yaml
from datetime import datetime

def selecionar_arquivo_temporario():
    arquivos = os.listdir('dados/temporario')
    arquivos_csv = [f for f in arquivos if f.endswith('.csv')]

    if not arquivos_csv:
        print("❌ Nenhum CSV encontrado na pasta dados/temporario.")
        return None

    print("\n📁 Arquivos disponíveis em dados/temporario:")
    for i, nome in enumerate(arquivos_csv):
        print(f"  {i+1}. {nome}")

    opcao = input("👉 Selecione o número do arquivo desejado: ")
    try:
        idx = int(opcao) - 1
        return os.path.join('dados/temporario', arquivos_csv[idx])
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return None

def selecionar_arquivos(filtro=None):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    caminhos = filedialog.askopenfilenames(
        title='Selecione os arquivos CSV de entrada',
        filetypes=[('Arquivos CSV', '*.csv')]
    )

    if not caminhos:
        return []

    if filtro:
        caminhos = [p for p in caminhos if filtro in os.path.basename(p)]

    return list(caminhos)

def carregar_macroareas(yaml_path='dados/macroareas.yaml'):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("❌ Estrutura inválida no macroareas.yaml")
    return data

def carregar_index_funcao_subfuncao(caminho='dados/index_funcao_subfuncao.csv'):
    df_index = pd.read_csv(caminho)
    df_index['Descricao'] = df_index['Descricao'].astype(str).str.strip().str.lower()
    return df_index

def timestamp_str():
    return datetime.now().strftime('%d%m_%Hh')

def identificar_colunas_ano(df):
    return [col for col in df.columns if str(col).isdigit()]

def calcular_total_despesas(df, col_anos):
    totais = df[col_anos].sum(numeric_only=True)
    total_df = pd.DataFrame([totais])
    total_df.insert(0, 'Grupo', 'Total Geral')
    return total_df
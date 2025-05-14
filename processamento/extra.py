import pandas as pd
import yaml
from collections import defaultdict

# Regras do usuário
funcoes_social = {'08', '09', '10', '12', '13', '14', '18', '19', '24', '27'}
funcoes_financeiro = {'28'}

def classificar_grupos(df):
    grupos = {
        'Gasto Social': defaultdict(set),
        'Gasto Financeiro': defaultdict(set),
        'Despesas Diversas': defaultdict(set),
    }

    for _, row in df.iterrows():
        cod_funcao = str(row['codigo_funcao']).zfill(2)
        cod_subfuncao = str(row['codigo_subfuncao']).zfill(3)

        if cod_funcao in funcoes_social:
            grupo = 'Gasto Social'
        elif cod_funcao in funcoes_financeiro:
            grupo = 'Gasto Financeiro'
        else:
            grupo = 'Despesas Diversas'

        grupos[grupo]['codigos_funcao'].add(cod_funcao)
        grupos[grupo]['codigos_subfuncao'].add(cod_subfuncao)

    return grupos

def exibir_em_yaml(grupos):
    for nome, valores in grupos.items():
        print(f"\n{nome}:")
        print(yaml.dump({
            'codigos_funcao': sorted(valores['codigos_funcao']),
            'codigos_subfuncao': sorted(valores['codigos_subfuncao']),
        }, sort_keys=False, allow_unicode=True, default_flow_style=False))

def main():
    path = 'dados/index_funcao_subfuncao.csv'
    df = pd.read_csv(path, dtype=str)

    if not {'codigo_funcao', 'codigo_subfuncao'}.issubset(df.columns):
        raise ValueError("❌ CSV deve conter as colunas 'codigo_funcao' e 'codigo_subfuncao'.")

    grupos = classificar_grupos(df)
    exibir_em_yaml(grupos)

if __name__ == '__main__':
    main()

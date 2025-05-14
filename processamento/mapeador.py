import pandas as pd
from processamento.normalizador import normalizar_texto

def carregar_index_funcao_subfuncao(caminho='dados/index_funcao_subfuncao.csv'):
    df_index = pd.read_csv(caminho, dtype=str)
    df_index['funcao'] = df_index['funcao'].apply(normalizar_texto)
    df_index['subfuncao'] = df_index['subfuncao'].apply(normalizar_texto)
    return df_index

def mapear_codigo(df, tipo='subfuncao', caminho='dados/index_funcao_subfuncao.csv'):
    index = carregar_index_funcao_subfuncao(caminho)

    cod_funcao = []
    cod_subfuncao = []

    for valor in df['Descricao']:
        desc = normalizar_texto(valor)

        if tipo == 'funcao':
            match = index[index['funcao'] == desc]
            if not match.empty:
                cod_funcao.append(match.iloc[0]['codigo_funcao'])
                cod_subfuncao.append('-')
            else:
                cod_funcao.append('NA')
                cod_subfuncao.append('-')

        elif tipo == 'subfuncao':
            match = index[index['subfuncao'] == desc]
            if not match.empty:
                cod_funcao.append(match.iloc[0]['codigo_funcao'])
                cod_subfuncao.append(match.iloc[0]['codigo_subfuncao'])
            else:
                cod_funcao.append('NA')
                cod_subfuncao.append('NA')
        else:
            raise ValueError("Tipo inválido. Use 'funcao' ou 'subfuncao'.")

    df.insert(0, 'codigo_funcao', cod_funcao)
    df.insert(1, 'codigo_subfuncao', cod_subfuncao)

    return df

import pandas as pd

def adicionar_total_geral(df):
    col_anos = [col for col in df.columns if str(col).isdigit()]
    totais = df[col_anos].sum(numeric_only=True)
    total_row = {
        'codigo_funcao': 'TOTAL',
        'codigo_subfuncao': '-',
        'Descricao': 'Total Geral',
        **totais.to_dict()
    }
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

def adicionar_total_parcial(df, codigos_funcao):
    if 'codigo_funcao' not in df.columns:
        raise ValueError("❌ Coluna 'codigo_funcao' ausente no DataFrame.")

    col_anos = [col for col in df.columns if str(col).isdigit()]
    codigos_funcao = [str(c) for c in codigos_funcao]
    df_filtrado = df[df['codigo_funcao'].astype(str).isin(codigos_funcao)]
    
    totais = df_filtrado[col_anos].sum(numeric_only=True)
    total_row = {
        'codigo_funcao': 'PARCIAL',
        'codigo_subfuncao': '-',
        'Descricao': 'Total Parcial',
        **totais.to_dict()
    }
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

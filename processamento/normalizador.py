import pandas as pd
import unicodedata
import re

def normalizar_texto(texto):
    """
    Remove acentos, símbolos e pontuação de um texto.
    Transforma em minúsculas e limpa espaços duplicados.
    """
    if pd.isnull(texto):
        return ''
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^a-z0-9\s]', '', texto)  # remove símbolos/pontuação
    texto = re.sub(r'\s+', ' ', texto)         # normaliza espaços
    return texto.strip()

def normalizar_coluna(df, coluna_nome, nova_coluna=False):
    """
    Aplica a função de normalização à coluna especificada.
    
    Se nova_coluna=True, cria uma nova com sufixo '_normalizado'.
    Se nova_coluna=False, sobrescreve a original.
    """
    if coluna_nome not in df.columns:
        raise ValueError(f"❌ Coluna '{coluna_nome}' não encontrada no DataFrame.")
    
    if nova_coluna:
        nova = f"{coluna_nome}_normalizado"
        df[nova] = df[coluna_nome].apply(normalizar_texto)
    else:
        df[coluna_nome] = df[coluna_nome].apply(normalizar_texto)

    return df

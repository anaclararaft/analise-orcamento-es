import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario

def identificar_colunas_ano(df):
    return [col for col in df.columns if col.isdigit()]

def main():
    print("📤 Exportador para BI (formato tidy/long)")

    df = pd.read_csv(selecionar_arquivo_temporario())
    col_anos = identificar_colunas_ano(df)

    colunas_obrigatorias = ['Descricao']
    faltando = [col for col in colunas_obrigatorias if col not in df.columns]

    if faltando:
        print(f"❌ Colunas obrigatórias ausentes: {faltando}")
        return

    # Inferir colunas extras se existirem
    id_vars = ['Descricao']
    if 'codigo_funcao' in df.columns:
        id_vars.append('codigo_funcao')
    if 'codigo_subfuncao' in df.columns:
        id_vars.append('codigo_subfuncao')
    if 'nivel' in df.columns:
        id_vars.append('nivel')
    if 'Grupo' in df.columns:
        id_vars.append('Grupo')
    if 'tipo_linha' in df.columns:
        id_vars.append('tipo_linha')
    else:
        df['tipo_linha'] = 'dado'  # padrão, se não especificado

    df_tidy = df.melt(id_vars=id_vars, value_vars=col_anos,
                      var_name='ano', value_name='valor')

    print("\n🔍 Preview dos dados em formato tidy:")
    print(df_tidy.head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/saida', exist_ok=True)
    nome_saida = f'bi_export_{agora}.csv'
    df_tidy.to_csv(os.path.join('dados/saida', nome_saida), index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo tidy exportado para: dados/saida/{nome_saida}")

if __name__ == '__main__':
    main()

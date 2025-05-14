import pandas as pd
import os
from datetime import datetime
import yaml
from processamento.utils import selecionar_arquivo_temporario

def carregar_macroareas(yaml_path='dados/macroareas.yaml'):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def mapear_grupo_por_codigo(codigo, macroareas):
    for grupo, regras in macroareas.items():
        codigos = regras.get('codigos_funcao', []) + regras.get('codigos_subfuncao', [])
        if str(codigo) in map(str, codigos):
            return grupo
    return "Não classificado"

def main():
    print("🏷️ Aplicador de Macroáreas")

    caminho = selecionar_arquivo_temporario()
    df = pd.read_csv(caminho)

    if 'codigo_funcao' not in df.columns and 'codigo_subfuncao' not in df.columns:
        print("❌ É necessário ter 'codigo_funcao' ou 'codigo_subfuncao' no arquivo.")
        return

    macroareas = carregar_macroareas()

    def aplicar_grupo(row):
        cod_sub = row.get('codigo_subfuncao', '-')
        cod_fun = row.get('codigo_funcao', '-')
        if pd.notna(cod_sub) and cod_sub != '-':
            return mapear_grupo_por_codigo(cod_sub, macroareas)
        elif pd.notna(cod_fun) and cod_fun != '-':
            return mapear_grupo_por_codigo(cod_fun, macroareas)
        else:
            return "Não classificado"

    df['Grupo'] = df.apply(aplicar_grupo, axis=1)

    total = len(df)
    classificados = (df['Grupo'] != 'Não classificado').sum()
    print(f"\n✅ Classificação concluída: {classificados} de {total} registros classificados.")

    print("\n🔍 Preview das macroáreas aplicadas:")
    print(df[['codigo_funcao', 'codigo_subfuncao', 'Grupo']].head(10))

    agora = datetime.now().strftime('%d%m_%Hh')
    os.makedirs('dados/temporario', exist_ok=True)
    nome_saida = f'dados-macroarea-{agora}.csv'
    df.to_csv(os.path.join('dados/temporario', nome_saida), index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo salvo em: dados/temporario/{nome_saida}")

if __name__ == '__main__':
    main()

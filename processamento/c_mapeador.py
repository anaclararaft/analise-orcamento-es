import pandas as pd
import os
from datetime import datetime
from processamento.utils import selecionar_arquivo_temporario
from processamento.mapeador import mapear_codigo

def main():
    print("🧭 Mapeador de funções e subfunções")

    # Selecionar arquivo CSV da pasta temporária
    caminho = selecionar_arquivo_temporario()
    df = pd.read_csv(caminho)

    # Solicitar tipo de mapeamento
    tipo = input("🔎 Tipo de mapeamento [funcao / subfuncao]: ").strip().lower()
    if tipo not in ['funcao', 'subfuncao']:
        print("❌ Tipo inválido.")
        return

    # Aplicar mapeamento
    df = mapear_codigo(df, tipo=tipo)

    # Exportar
    agora = datetime.now()
    nome_saida = f"dados_mapeado_{agora.strftime('%d%m_%Hh')}.csv"
    caminho_saida = os.path.join('dados/temporario', nome_saida)
    df.to_csv(caminho_saida, index=False, encoding='utf-8-sig')

    print(f"\n✅ Arquivo mapeado exportado para: {caminho_saida}")
    print(f"🔢 Total de linhas mapeadas: {len(df)}")

if __name__ == '__main__':
    main()

import subprocess

etapas = [
    ("a_leitor.py", "📂 Etapa A: Leitura e unificação dos arquivos CSV"),
    ("b_normalizar.py", "🧼 Etapa B: Normalização textual e valores"),
    ("c_mapeador.py", "🧭 Etapa C: Mapeamento de função ou subfunção"),
    ("d_deflacionar.py", "📉 Etapa D: Aplicação de deflação"),
    ("e_macroarea.py", "🏷️ Etapa E: Aplicação de macroáreas (grupo)"),
    ("f_estatisticas.py", "📊 Etapa F: Geração de totais e detalhado por grupo"),
    ("g_indicadores.py", "📈 Etapa G: Geração de indicadores macrofiscais"),
    ("h_exportar_bi.py", "📤 Etapa H: Exportação para BI (formato tidy)")
]

def rodar_etapa(script, descricao):
    print(f"\n{descricao}")
    opcao = input("→ Deseja executar esta etapa? (s/n): ").strip().lower()
    if opcao == 's':
        subprocess.run(["python", f"processamento/{script}"])

def main():
    print("\n🚦 Início do Pipeline Interativo de Indicadores Macrofiscais\n")
    for script, descricao in etapas:
        rodar_etapa(script, descricao)

    print("\n✅ Pipeline concluído com sucesso.\n")

if __name__ == "__main__":
    main()

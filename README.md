# Análise do Orçamento Público do ES - EM CONSTRUÇÃO

Este projeto, ainda em andamento, pretende consolidar, padronizar e analisar os dados de orçamento público do Estado do Espírito Santo. A partir de arquivos brutos por função e subfunção, o pipeline realiza a normalização dos dados, aplica deflacionamento com base no IPCA, mapeia áreas temáticas (macroáreas) e gera indicadores consolidados para análise de políticas públicas e planejamento orçamentário.

## 🛠 Funcionalidades principais

- Leitura incremental de arquivos por ano e categoria
- Padronização de textos e categorias (funções, subfunções, fontes de recursos)
- Mapeamento de funções para macroáreas temáticas (educação, saúde, etc.)
- Deflacionamento com IGP-DI e no base.
- Geração de indicadores por ano, macroárea e categoria de gasto
- Exportação de resultados consolidados para uso em dashboards ou relatórios
- Arquitetura modular: cada etapa do processo é separada em scripts próprios para manutenção e reuso.

## 📁 Estrutura do projeto

```
analise-orcamento-es/
├── main.py
├── processamento/
│   ├── a_leitor.py
│   ├── b_normalizar.py
│   ├── c_mapeador.py
│   ├── d_deflacionar.py
│   ├── e_macroareas.py
│   ├── f_estatisticas.py
│   ├── g_indicadores.py
│   ├── h_export.py
│   ├── i_tributario.py
│   ├── utils.py
│   └── ...
├── dados/
│   ├── entrada/
│   │   ├── funcao-2015.csv ... funcao-2022.csv
│   │   ├── subfuncao-2015.csv ... subfuncao-2022.csv
│   │   └── arrecadacao_corrigida_2015_2022.csv
│   ├── saida/
│   └── arquivos_processados.json
├── config/
│   ├── macroareas.yaml
│   ├── indices_deflacao.txt
│   └── index_funcao_subfuncao.csv
├── fluxo_dados.txt
├── .gitignore
└── README.md
```

## 🚀 Como executar

1. Instale as dependências do projeto (se necessário):
```
pip install pandas numpy pyyaml
```

2. Execute o script principal:

```
python main.py
```

3. Os resultados serão salvos em `dados/saida/`.

## 📊 Tecnologias utilizadas

- Python 3
- Pandas
- NumPy
- YAML

## 👩‍💻 Autoria

Projeto desenvolvido por [Ana Clara](https://github.com/anaclararaft) como parte de um portfólio aplicado à análise de dados públicos e automação de processos para suporte à tomada de decisão.

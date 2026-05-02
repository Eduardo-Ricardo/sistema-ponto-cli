📊 Arquitetura do Projeto: ETL de Ponto Eletrônico

1. Visão Geral

Este projeto consiste no desenvolvimento de um pipeline de dados (ETL - Extração, Transformação e Carga) escrito em Python. O objetivo é processar logs brutos de um relógio de ponto físico (arquivo TXT), aplicar regras de negócio (limpeza de spam/duplicatas) e estruturar as batidas em uma hierarquia temporal limpa para posterior cálculo de folha de pagamento ou dashboards.

2. Padrão Arquitetural (Modular ETL Pipeline)

Dada a natureza de processamento de dados do projeto, utilizaremos a arquitetura de Pipeline Modular de Dados.

O projeto rejeita padrões de interface (como MVC) em favor de um fluxo funcional estrito:

Orquestração: Um bloco main que coordena o fluxo de dados.

Modularidade: Cada fase do ETL (Leitura, Limpeza, Anti-Spam, Estruturação e Exportação) será encapsulada em sua própria função isolada.

Desacoplamento: Funções auxiliares pesadas estarão no arquivo utils.py, mantendo o etl_pipeline.py limpo e legível.

3. Pontos de Partida e Chegada (Milestones)

Ponto de Partida (As-Is): Arquivo bruto AGL_001.TXT extraído diretamente da máquina.

Estrutura suja, separada por tabulações (\t), contendo colunas inúteis e batidas duplicadas (spam de leitura do dedo do funcionário).

Ponto de Chegada (To-Be): Um pipeline automatizado que converte o TXT sujo em um arquivo estruturado (JSON e/ou Excel).

Dados padronizados e organizados na seguinte hierarquia cronológica estrita: Ano -> Mês -> Funcionário -> Data -> [Batida 1, Batida 2, ...].

4. Metodologia de Trabalho (Workflow Iterativo e Git Flow)

Para garantir a integridade dos dados e a qualidade do código, este projeto segue um ciclo estrito de validação e versionamento:

Isolamento de Funcionalidade (Branches): Cada nova fase ou módulo é desenvolvido estritamente em uma branch separada (ex: feature/fase-1-leitura).

Desenvolvimento Segmentado: O código é escrito bloco a bloco dentro de sua respectiva branch.

Validação de Output: Cada bloco é testado localmente para garantir que as regras de negócio foram aplicadas.

Versionamento e Integração (Merge): Após a aprovação do teste, o bloco recebe um commit. Em seguida, é feito o merge (integração) com a branch main (principal).

5. Estrutura do Repositório

A estrutura de pastas do projeto deve seguir as boas práticas de Engenharia de Dados:
/
├── data/
│   ├── raw/                  # Onde os arquivos TXT originais serão colocados (ex: AGL_001.TXT)
│   └── processed/            # Onde os arquivos JSON/Excel limpos serão salvos
├── src/
│   ├── etl_pipeline.py       # Script principal do ETL
│   └── utils.py              # (Opcional) Funções auxiliares de cálculo de horas
├── README.md                 # Este documento de arquitetura
├── requirements.txt          # Dependências do projeto (ex: pandas)
└── .gitignore                # Ignorar ambientes virtuais e dados sensíveis

6. Fases de Desenvolvimento e Regras de Negócio (O Pipeline)

Fase 1: Extração (Extract)

Ação: Ler o arquivo /data/raw/AGL_001.TXT.

Desafio: Lidar com codificação de caracteres (encoding) e separadores de tabulação.

Fase 2: Transformação Nível 1 (Limpeza Estrutural)

Drop de Colunas: Descartar as colunas No, TMNo, GMNo e Mode.

Tipagem Forte: Converter a coluna DateTime obrigatoriamente para o formato datetime do Pandas.

Limpeza de Strings: Padronizar a coluna Name (remover espaços em branco no início/fim, converter para formato "Title Case").

Fase 3: Transformação Nível 2 (Regras de Negócio & Anti-Spam)

Identificação de Batida: Um funcionário é unicamente identificado pela combinação do seu EnNo (ID) e Name.

Regra Anti-Spam (Tolerância): Agrupar os dados por funcionário e ordenar por data/hora. Se a diferença de tempo entre duas marcações consecutivas do mesmo funcionário for inferior a 5 minutos, a segunda marcação deve ser considerada um "duplo clique" acidental no leitor e deve ser descartada.

Fase 4: Transformação Nível 3 (Estruturação Hierárquica)

Extrair o Ano, Mês e Dia a partir da coluna de Data tratada.

Agrupar as marcações limpas criando a estrutura aninhada final.

Garantir que, dentro de cada dia, a lista de batidas (["08:00", "12:00", "13:00", "18:00"]) esteja estritamente ordenada do menor para o maior.

Fase 5: Carga (Load)

Ação: Exportar a estrutura hierárquica construída na Fase 4 para o diretório /data/processed/.

Formato Primário: Salvar como dados_ponto.json para garantir a preservação da hierarquia.

7. Roadmap de Execução (Checklist)

Acompanhamento conceitual do progresso do projeto. Marcar com [x] ao concluir cada etapa.

[ ] Fase 0: Setup Inicial

[x] Definição da Arquitetura e Regras

[x] Criação da estrutura de pastas

[ ] Configuração do repositório Git

[ ] Fase 1: Extração (Extract)

[ ] Carregamento do TXT bruto

[ ] Tratamento de encoding e separadores

[ ] Fase 2: Transformação Nível 1 (Limpeza)

[ ] Remoção de colunas desnecessárias

[ ] Conversão e tipagem do DateTime

[ ] Padronização dos nomes

[ ] Fase 3: Transformação Nível 2 (Anti-Spam)

[ ] Agrupamento por funcionário (ID + Nome)

[ ] Aplicação da regra de exclusão (gap < 5 min)

[ ] Fase 4: Transformação Nível 3 (Hierarquia)

[ ] Extração de chaves temporais (Ano, Mês, Dia)

[ ] Construção do dicionário aninhado

[ ] Ordenação cronológica das listas de batidas

[ ] Fase 5: Carga (Load)

[ ] Exportação do arquivo .json final
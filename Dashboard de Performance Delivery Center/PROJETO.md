📊 Projeto: Dashboard de Performance - Delivery Center

Aluno: Patrick Soares Mendes

Curso: MBA em Big Data e Machine Learning

Disciplina: Unidade Curricular 16 - Ferramentas de Business Intelligence

🎯 Objetivo do Projeto

O objetivo desta atividade foi conceber e desenvolver um projeto completo de análise de dados, transformando dados brutos em insights estratégicos. O desafio consistiu na criação de um dashboard interativo utilizando técnicas de ETL, modelagem de dados, definição de KPIs e storytelling, aplicados a um cenário real de logística e delivery.

🗂️ Sobre o Dataset

O projeto foi elaborado a partir do dataset Delivery Center: Food & Goods orders in Brazil, disponível no Kaggle. O dataset contém aproximadamente 370.000 pedidos e é composto pelas seguintes tabelas:

Tabela

Descrição

Channels

Informações sobre canais de venda (marketplaces).

Deliveries

Dados sobre as entregas realizadas.

Drivers

Informações sobre os entregadores parceiros.

Hubs

Centros de distribuição dos pedidos.

Orders

Vendas processadas através da plataforma (Tabela Fato).

Payments

Informações sobre pagamentos realizados.

Stores

Informações sobre os lojistas cadastrados.

🚀 Etapas do Desenvolvimento

1. Estudo dos Dados

A análise exploratória inicial identificou que a base opera sob uma lógica relacional, conectando transações centrais a entidades de cadastro via chaves estrangeiras.

Tabela Fato (F): A tabela orders foi definida como a fato principal, contendo eventos granulares (pedidos) e métricas quantitativas. As tabelas payments e deliveries atuam como fatos auxiliares.

Tabelas Dimensão (D): As tabelas stores, hubs, channels e drivers foram classificadas como dimensões, fornecendo contexto descritivo para as análises.

2. Planejamento

O dashboard foi planejado em duas perspectivas distintas: Estratégica (Financeira) e Tática (Operacional).

KPIs Definidos:

Volume: Faturamento Bruto (GMV) e Quantidade de Pedidos Válidos.

Eficiência: Ticket Médio e Taxa de Cancelamento.

Logística: Tempo Médio de Ciclo (segmentado obrigatoriamente entre Food e Good devido à disparidade de natureza dos pedidos).

Visualizações Escolhidas:

Cartões (Big Numbers): Para destaque de números macro.

Gráfico de Área: Para análise de tendência temporal e crescimento (MoM).

Gráfico de Barras: Para análise de Pareto (Ranking de Hubs).

Scatter Plot (Dispersão): Para correlação entre Distância e Tempo de Entrega.

Matriz Hierárquica: Para drill-down (Hub -> Loja) com alertas visuais.

3. Processo de ETL (Power Query)

O tratamento de dados foi essencial para garantir a integridade da análise, com destaque para as seguintes ações:

Correção de Localidade (Regional Settings): Conversão manual de colunas financeiras (order_amount) e de tempo (order_metric_cycle_time) que utilizavam padrão americano (ponto decimal). A leitura automática incorreta multiplicava os valores (ex: 62.7 virava 627).

Remoção de Outliers: Identificação e exclusão do registro "HUBLESS SHOPPING", que apresentava métricas irreais (Distância > 270km e Tempo > 9.600 min), distorcendo as escalas gráficas.

Padronização Temporal: Conversão de colunas de timestamp para formato Data/Hora, permitindo relacionamentos corretos.

4. Modelagem de Dados

Utilizou-se o esquema Star Schema para otimização de performance e facilidade de cálculo.

Relacionamentos: Estabelecidos relacionamentos Um-para-Muitos (1:*) entre as dimensões e a tabela fato orders.

Tabela Calendário: Criada via DAX (CALENDARAUTO) para garantir continuidade temporal.

Medidas DAX:

CALCULATE: Utilizado para filtrar estritamente pedidos finalizados (order_status = "FINISHED").

ALL: Aplicado para cálculos de Market Share (ignorando filtros de contexto).

DIVIDE: Utilizado para evitar erros de divisão por zero em médias e taxas.

5. Composição Visual e Storytelling

A estrutura de navegação simula um aplicativo, dividida em duas narrativas:

Página 1 - Visão Executiva (O "Quê"): Leitura macro da saúde financeira seguindo o padrão em "Z". Inicia-se pelos KPIs, passa pelo Pareto de Hubs e Risco de Canal, finalizando com a Tendência Mensal.

Página 2 - Visão Operacional (O "Porquê"): Foco na identificação de gargalos. O destaque central é o Gráfico de Dispersão (comprovando a baixa correlação distância/atraso) e a Matriz Hierárquica com formatação condicional (alerta vermelho para entregas > 60 min).

💡 Principais Insights

Paradoxo da Eficiência Logística: O Golden Shopping, apesar de líder em faturamento, apresenta gargalos operacionais significativos com tempos acima da média. Em contrapartida, o Fortran Shopping demonstra ser um benchmark de agilidade, mantendo eficiência mesmo em longas distâncias. O Canal Próprio (OWN CHANNEL) apresenta alta variabilidade, indicando processos logísticos menos robustos que os marketplaces.

Risco de Dependência de Canal: Os Marketplaces dominam aproximadamente 79% do faturamento. Essa alta dependência reduz as margens de lucro devido às taxas de comissão e expõe a empresa a riscos de mudanças de algoritmo. Recomenda-se ações para migração de clientes fiéis para o app próprio.

Consolidação de Crescimento em Março: O mês de março consolidou a base de clientes, superando significativamente os meses de janeiro e fevereiro e estabelecendo um novo patamar de faturamento. A análise sugere investigação para determinar se o crescimento foi orgânico ou sazonal, utilizando este novo patamar como meta mínima para o próximo trimestre.

Projeto desenvolvido como requisito avaliativo para a disciplina de Ferramentas de BI.
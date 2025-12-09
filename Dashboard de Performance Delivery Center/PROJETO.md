📊 Projeto: Dashboard de Performance - Delivery Center

Aluno: Patrick Soares Mendes
Curso: MBA em Big Data e Machine Learning
Disciplina: Unidade Curricular 16 - Ferramentas de Business Intelligence

🎯 Objetivo do Projeto

O objetivo desta atividade foi conceber e desenvolver um projeto completo de análise de dados, transformando dados brutos em insights estratégicos. O desafio consistiu na criação de um dashboard interativo utilizando técnicas de ETL, modelagem de dados, definição de KPIs e storytelling.

🗂️ Sobre o Dataset

O projeto foi elaborado a partir do dataset Delivery Center: Food & Goods orders in Brazil, disponível no Kaggle. O dataset contém aproximadamente 370.000 pedidos e é composto pelas seguintes tabelas:

Channels: Informações sobre canais de venda (marketplaces).

Deliveries: Dados sobre as entregas realizadas.

Drivers: Informações sobre os entregadores parceiros.

Hubs: Centros de distribuição dos pedidos.

Orders: Vendas processadas através da plataforma (Tabela Fato).

Payments: Informações sobre pagamentos realizados.

Stores: Informações sobre os lojistas cadastrados.

🚀 Etapas do Desenvolvimento

1. Estudo dos Dados

A análise inicial identificou que a base opera sob uma lógica relacional, conectando transações centrais a entidades de cadastro via chaves estrangeiras.

Tabela Fato (F): A tabela orders foi definida como a fato principal, contendo eventos granulares e métricas quantitativas. As tabelas payments e deliveries atuam como fatos auxiliares.

Tabelas Dimensão (D): As tabelas stores, hubs, channels e drivers foram classificadas como dimensões, fornecendo contexto descritivo.

2. Planejamento

O dashboard foi escopado em duas perspectivas: Estratégica (Financeira) e Tática (Operacional).

KPIs Definidos:

Volume: Faturamento Bruto e Quantidade de Pedidos Válidos.

Eficiência: Ticket Médio e Taxa de Cancelamento.

Logística: Tempo Médio de Ciclo (segmentado entre Food e Good).

Visualizações Escolhidas:

Cartões (Big Numbers): Para números macro.

Gráfico de Área: Para tendência temporal e crescimento.

Gráfico de Barras: Para análise de Pareto (Ranking de Hubs).

Scatter Plot (Dispersão): Para correlação Distância vs. Tempo.

Matriz Hierárquica: Para drill-down com alertas visuais.

3. Processo de ETL (Power Query)

O tratamento de dados garantiu a integridade da análise através das seguintes ações:

Correção de Localidade: Conversão manual de colunas financeiras (order_amount) e de tempo (order_metric_cycle_time) que utilizavam padrão americano (ponto), evitando erros de multiplicação.

Remoção de Outliers: Exclusão do registro "HUBLESS SHOPPING", que apresentava métricas irreais (Distância > 270km e Tempo > 9.600 min).

Padronização: Conversão de colunas de timestamp para formato Data/Hora.

4. Modelagem de Dados

Utilizou-se o esquema Star Schema para otimização de performance.

Relacionamentos: Estabelecidos relacionamentos Um-para-Muitos (1:*) entre dimensões e a tabela fato orders.

Tabela Calendário: Criada via DAX (CALENDARAUTO) para análises temporais.

Medidas DAX:

CALCULATE: Para filtrar pedidos finalizados (order_status = "FINISHED").

ALL: Para cálculo de Market Share.

DIVIDE: Para evitar erros de divisão por zero.

5. Composição Visual e Storytelling

A estrutura foi dividida em duas narrativas:

Página 1 - Visão Executiva (O "Quê"): Leitura macro da saúde financeira seguindo o padrão em "Z" (KPIs -> Pareto -> Risco de Canal -> Tendência).

Página 2 - Visão Operacional (O "Porquê"): Foco em gargalos. O destaque é o Gráfico de Dispersão (comprovando baixa correlação distância/atraso) e a Matriz Hierárquica com formatação condicional (alerta vermelho para entregas > 60 min).

💡 Principais Insights

Paradoxo da Eficiência: O Golden Shopping, apesar de líder em faturamento, apresenta gargalos operacionais com tempos acima da média. Em contrapartida, o Fortran Shopping é um benchmark de agilidade, mesmo em longas distâncias. O Canal Próprio (OWN CHANNEL) apresenta alta variabilidade e processos logísticos menos robustos que os marketplaces.

Risco de Dependência: Os Marketplaces dominam 79% do faturamento. Essa dependência reduz margens devido às taxas e expõe a empresa a mudanças de algoritmo. Sugere-se migração de clientes fiéis para o app próprio.

Consolidação em Março: O mês de março consolidou a base de clientes, superando janeiro e fevereiro e estabelecendo um novo patamar de faturamento. Deve-se investigar se o crescimento foi orgânico ou sazonal para o planejamento futuro.
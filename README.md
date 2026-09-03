# 📊 Análise de Impacto de Manutenções no Churn de Telecomunicações

## 📌 Contexto de Negócio
Em empresas de Telecom, janelas de manutenção na infraestrutura de rede são inevitáveis. No entanto, quando a comunicação preventiva falha, os clientes percebem a queda na conexão como instabilidade contínua e entram em contato com o suporte insatisfeitos.

O objetivo deste projeto foi mapear a jornada do cliente durante eventos de manutenção para quantificar o **custo financeiro da perda de clientes (Churn e MRR perdido)** decorrente de falhas operacionais na comunicação preventiva.

---

## 🎯 O Funil de Análise (4 Etapas)
A análise foi construída dividindo a base de dados em 4 níveis encadeados de conversão:

1. **Base Total de Clientes:** Universo total de assinantes monitorados.
2. **Clientes em Regiões com Manutenção:** Clientes localizados em áreas afetadas por eventos preventivos ou emergenciais.
3. **Clientes Impactados (Contataram o Suporte):** Assinantes que sentiram a oscilação/queda e ligaram para o suporte durante a janela da manutenção.
4. **Churn Causado por Manutenção:** Clientes que cancelaram o contrato dentro da janela de 30 dias após o registro do chamado.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Python (`pandas`, `numpy`, `openpyxl`):** Geração da base sintética de dados e simulação das regras de negócio.
* **SQL (`CTEs` e `Cross Join`):** Criação das consultas para cálculo de conversão do funil e perda recorrente de receita (MRR).
* **Excel Avançado:** Construção do Dashboard Executivo com cartões de KPIs e tabela de visão geral.

---

## 📈 Principais Insights Obtidos

* **Taxa de Churn 11x Maior:** Enquanto a taxa de cancelamento natural da base é de **~3%**, clientes que ligaram para o suporte durante uma manutenção apresentaram uma taxa de cancelamento de **33.3%** nos 30 dias subsequentes.
* **Custo do Suporte Não Preventivo:** A falta de aviso prévio (SMS/Push) resultou na perda direta de **R$ 13.910,10 em MRR** no período analisado.
* **Região Crítica:** Eventos emergenciais do tipo *"Rompimento de Fibra"* tiveram o maior índice de chamados por cliente comparados a manutenções preventivas programadas.

---

## 📁 Estrutura dos Arquivos do Repositório
* `Dashboard_Churn_Manutencao_Telecom.xlsx`: Planilha com a visão executiva e dados brutos.
* `consulta_funnel_churn.sql`: Script SQL contendo as queries para extração dos dados.
* `telecom_churn_manutencao.csv`: Dataset em formato CSV utilizado no estudo.
* `gerar_dados_churn.py`: Script Python para reproduzir a geração da base fictícia.# churn-manutencao-telecom
Análise de impacto financeiro e churn de clientes causados por manutenções de rede.

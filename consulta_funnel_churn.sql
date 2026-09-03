-- =====================================================================
-- PROJETO: Análise de Impacto de Manutenções no Churn de Telecom
-- AUTOR: Analista de Dados
-- FERRAMENTA: PostgreSQL / SQLite / MySQL
-- OBJETIVO: Mapear o funil de impacto de manutenções de rede no cancelamento
-- =====================================================================

WITH 
-- 1. Base Total de Clientes na Empresa
Base_Total AS (
    SELECT 
        COUNT(DISTINCT id_cliente) AS total_clientes,
        SUM(valor_mensalidade) AS mrr_total
    FROM base_clientes_chamados
),

-- 2. Clientes localizados em regiões que sofreram intervenção/manutenção
Clientes_Em_Manutencao AS (
    SELECT 
        COUNT(DISTINCT id_cliente) AS clientes_afetados
    FROM base_clientes_chamados
    WHERE id_manutencao != 'N/A'
),

-- 3. Clientes que sentiram o impacto direto e ligaram no suporte durante a manutenção
Clientes_Impactados AS (
    SELECT 
        COUNT(DISTINCT id_cliente) AS clientes_ligaram
    FROM base_clientes_chamados
    WHERE entrou_em_contato_manutencao = 1
),

-- 4. Clientes que cancelaram o serviço dentro do range de 30 dias após a ligação
Churn_Manutencao AS (
    SELECT 
        COUNT(DISTINCT id_cliente) AS clientes_churn_30d,
        SUM(valor_mensalidade) AS receita_perdida_mrr
    FROM base_clientes_chamados
    WHERE entrou_em_contato_manutencao = 1 
      AND churn = 1 
      AND dias_ate_cancelamento <= 30
)

-- RESULTADO FINAL: Mapeamento do Funil de Conversão do Churn por Manutenção
SELECT 
    bt.total_clientes,
    cm.clientes_afetados,
    ci.clientes_ligaram,
    ROUND((ci.clientes_ligaram * 100.0 / cm.clientes_afetados), 2) AS pct_afetados_que_ligaram,
    ch.clientes_churn_30d,
    ROUND((ch.clientes_churn_30d * 100.0 / ci.clientes_ligaram), 2) AS pct_churn_dos_que_ligaram,
    ch.receita_perdida_mrr,
    ROUND((ch.receita_perdida_mrr * 100.0 / bt.mrr_total), 2) AS pct_mrr_perdido_total
FROM Base_Total bt
CROSS JOIN Clientes_Em_Manutencao cm
CROSS JOIN Clientes_Impactados ci
CROSS JOIN Churn_Manutencao ch;


-- =====================================================================
-- QUERY SECUNDÁRIA: Detalhamento por Região e Motivo do Chamado
-- =====================================================================
SELECT 
    regiao,
    motivo_contato,
    COUNT(DISTINCT id_cliente) AS total_chamados,
    SUM(churn) AS total_churn,
    ROUND((SUM(churn) * 100.0 / COUNT(DISTINCT id_cliente)), 2) AS taxa_churn_pct,
    SUM(CASE WHEN churn = 1 THEN valor_mensalidade ELSE 0 END) AS mrr_perdido_regiao
FROM base_clientes_chamados
WHERE entrou_em_contato_manutencao = 1
GROUP BY regiao, motivo_contato
ORDER BY total_churn DESC;

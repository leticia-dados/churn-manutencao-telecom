from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

maintenances = [
    {
        "id_manutencao": "MNT-2026-001",
        "regiao": "Zona Sul - SP",
        "data_inicio": datetime(2026, 1, 10, 8, 0),
        "data_fim": datetime(2026, 1, 10, 18, 0),
        "tipo": "Emergencial - Rompimento de Fibra",
    },
    {
        "id_manutencao": "MNT-2026-002",
        "regiao": "Centro - RJ",
        "data_inicio": datetime(2026, 1, 15, 22, 0),
        "data_fim": datetime(2026, 1, 16, 6, 0),
        "tipo": "Preventiva - Upgrade de OLTs",
    },
    {
        "id_manutencao": "MNT-2026-003",
        "regiao": "Zona Leste - SP",
        "data_inicio": datetime(2026, 2, 1, 9, 0),
        "data_fim": datetime(2026, 2, 1, 15, 0),
        "tipo": "Corretiva - Troca de Switches",
    },
    {
        "id_manutencao": "MNT-2026-004",
        "regiao": "Centro - BH",
        "data_inicio": datetime(2026, 2, 10, 10, 0),
        "data_fim": datetime(2026, 2, 10, 20, 0),
        "tipo": "Emergencial - Instabilidade no Backbone",
    },
    {
        "id_manutencao": "MNT-2026-005",
        "regiao": "Zona Sul - RJ",
        "data_inicio": datetime(2026, 2, 18, 1, 0),
        "data_fim": datetime(2026, 2, 18, 5, 0),
        "tipo": "Preventiva - Manutenção Programada",
    },
]

# Configurações de clientes
n_customers = 1000
regions = [
    "Zona Sul - SP",
    "Zona Norte - SP",
    "Zona Leste - SP",
    "Centro - RJ",
    "Zona Sul - RJ",
    "Barra - RJ",
    "Centro - BH",
    "Savassi - BH",
]
plans = ["Fibra 200 Mega", "Fibra 400 Mega", "Fibra 600 Mega", "Fibra 1 Giga"]
plan_prices = {
    "Fibra 200 Mega": 99.90,
    "Fibra 400 Mega": 129.90,
    "Fibra 600 Mega": 159.90,
    "Fibra 1 Giga": 199.90,
}

customer_ids = [f"CLI-{1000 + i}" for i in range(n_customers)]
cust_regions = np.random.choice(
    regions, n_customers, p=[0.2, 0.15, 0.15, 0.15, 0.1, 0.1, 0.08, 0.07]
)
cust_plans = np.random.choice(plans, n_customers, p=[0.3, 0.4, 0.2, 0.1])

records = []

# 3. Lógica do Churn Impactado por Manutenção
for cid, reg, pl in zip(customer_ids, cust_regions, cust_plans):
  price = plan_prices[pl]
  mnt_in_region = [m for m in maintenances if m["regiao"] == reg]

  contacted_during_mnt = False
  id_mnt, data_ligacao, motivo_contato = None, None, None
  churn, data_cancelamento, dias_ate_cancelamento = 0, None, None

  if mnt_in_region:
    mnt = mnt_in_region[0]
    # 45% de chance de o cliente ligar durante a janela da manutenção
    if random.random() < 0.45:
      contacted_during_mnt = True
      id_mnt = mnt["id_manutencao"]

      # Simula data/hora exata do chamado dentro do horário da manutenção
      start_ts = int(mnt["data_inicio"].timestamp())
      end_ts = int(mnt["data_fim"].timestamp())
      data_ligacao = datetime.fromtimestamp(random.randint(start_ts, end_ts))
      motivo_contato = random.choice([
          "Sem Conexão / Queda Geral",
          "Lentidão Extrema",
          "Perda de Pacotes / Oscilação",
      ])

      if random.random() < 0.33:
        churn = 1
        dias_after = random.randint(1, 30)
        data_cancelamento = data_ligacao + timedelta(days=dias_after)
        dias_ate_cancelamento = dias_after
    else:
      # Churn base natural (apenas 3%)
      if random.random() < 0.03:
        churn = 1
        data_cancelamento = datetime(2026, 2, 25) - timedelta(
            days=random.randint(1, 30)
        )
  else:
    if random.random() < 0.03:
      churn = 1
      data_cancelamento = datetime(2026, 2, 25) - timedelta(
          days=random.randint(1, 30)
      )

  records.append({
      "id_cliente": cid,
      "regiao": reg,
      "plano": pl,
      "valor_mensalidade": price,
      "entrou_em_contato_manutencao": 1 if contacted_during_mnt else 0,
      "id_manutencao": id_mnt if contacted_during_mnt else "N/A",
      "data_ligacao": (
          data_ligacao.strftime("%Y-%m-%d %H:%M:%S") if data_ligacao else None
      ),
      "motivo_contato": motivo_contato if contacted_during_mnt else "N/A",
      "churn": churn,
      "data_cancelamento": (
          data_cancelamento.strftime("%Y-%m-%d") if data_cancelamento else None
      ),
      "dias_ate_cancelamento": dias_ate_cancelamento,
  })

# 4. Exportar os resultados
df_telecom = pd.DataFrame(records)
df_mnt = pd.DataFrame(maintenances)

df_telecom.to_csv(
    "telecom_churn_manutencao.csv", index=False, encoding="utf-8-sig"
)

with pd.ExcelWriter("telecom_churn_manutencao.xlsx") as writer:
  df_telecom.to_excel(writer, sheet_name="Base_Clientes_Chamados", index=False)
  df_mnt.to_excel(writer, sheet_name="Historico_Manutencoes", index=False)
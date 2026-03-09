select
    t.transaction_id,
    t.merchant_id,
    m.merchant_name,
    m.segment,
    m.city,
    t.customer_id,
    c.client_name,
    c.job as client_job,
    c.income as client_income,
    c.credit_risk as client_credit_risk,
    c.classification as client_classification,
    t.purchase_value,
    t.installments,
    t.transaction_date,
    strftime('%Y-%m', t.transaction_date) as origination_month
from {{ ref('stg_transactions') }} t
left join {{ ref('stg_merchants') }} m
    on t.merchant_id = m.merchant_id
left join {{ ref('stg_clients') }} c
    on t.customer_id = c.client_id

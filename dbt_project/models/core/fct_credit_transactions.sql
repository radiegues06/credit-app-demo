select
    t.transaction_id,
    t.merchant_id,
    m.merchant_name,
    m.segment,
    m.city,
    t.customer_id,
    t.purchase_value,
    t.installments,
    t.transaction_date,
    strftime('%Y-%m', t.transaction_date) as origination_month
from {{ ref('stg_transactions') }} t
left join {{ ref('stg_merchants') }} m
    on t.merchant_id = m.merchant_id

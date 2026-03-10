with transaction_metrics as (
    select
        t.transaction_id,
        t.customer_id,
        t.client_credit_risk,
        t.purchase_value,
        max(case when i.status = 'default' then 1 else 0 end) as is_defaulted
    from {{ ref('fct_credit_transactions') }} t
    join {{ ref('fct_installments') }} i
        on t.transaction_id = i.transaction_id
    group by 1, 2, 3, 4
)

select
    client_credit_risk,
    count(distinct customer_id) as total_clients,
    count(distinct transaction_id) as total_transactions,
    sum(purchase_value) as total_financed,
    sum(case when is_defaulted = 1 then purchase_value else 0 end) as defaulted_amount,
    case
        when sum(purchase_value) > 0 then (sum(case when is_defaulted = 1 then purchase_value else 0 end) / sum(purchase_value))
        else 0
    end as default_rate
from transaction_metrics
group by 1


with transactions as (
    select * from {{ ref('fct_credit_transactions') }}
),
installments as (
    select * from {{ ref('fct_installments') }}
)

select
    t.client_credit_risk,
    count(distinct t.customer_id) as total_clients,
    count(distinct t.transaction_id) as total_transactions,
    sum(i.principal) as total_financed,
    sum(case when i.status = 'default' then i.principal else 0 end) as defaulted_amount,
    case
        when sum(i.principal) > 0 then sum(case when i.status = 'default' then i.principal else 0 end) / sum(i.principal)
        else 0
    end as default_rate
from transactions t
join installments i
    on t.transaction_id = i.transaction_id
group by 1

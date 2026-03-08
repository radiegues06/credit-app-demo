with defaulted_installments as (
    select
        transaction_id,
        sum(principal) as defaulted_amount
    from {{ ref('fct_installments') }}
    where status = 'default'
    group by transaction_id
),
vintage_base as (
    select
        t.origination_month,
        sum(t.purchase_value) as total_financed,
        sum(coalesce(d.defaulted_amount, 0)) as defaulted_amount
    from {{ ref('fct_credit_transactions') }} t
    left join defaulted_installments d
        on t.transaction_id = d.transaction_id
    group by t.origination_month
)
select
    origination_month,
    total_financed,
    defaulted_amount,
    case
        when total_financed > 0 then (defaulted_amount / total_financed)
        else 0
    end as default_rate
from vintage_base
order by origination_month

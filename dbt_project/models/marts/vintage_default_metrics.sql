with transaction_defaults as (
    select
        transaction_id,
        max(case when status = 'default' then 1 else 0 end) as is_defaulted
    from {{ ref('fct_installments') }}
    group by 1
),
vintage_base as (
    select
        t.origination_month,
        sum(t.purchase_value) as total_financed,
        sum(case when d.is_defaulted = 1 then t.purchase_value else 0 end) as defaulted_amount
    from {{ ref('fct_credit_transactions') }} t
    left join transaction_defaults d
        on t.transaction_id = d.transaction_id
    group by 1
)
select
    origination_month,
    total_financed,
    defaulted_amount,
    case
        when total_financed > 0 then (cast(defaulted_amount as real) / total_financed)
        else 0
    end as default_rate
from vintage_base
order by origination_month


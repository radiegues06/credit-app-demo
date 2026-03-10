with transaction_exposure as (
    select
        transaction_id,
        sum(case when status in ('pending', 'late', 'default') then principal else 0 end) as outstanding_principal,
        max(days_past_due) as max_dpd
    from {{ ref('fct_installments') }}
    group by 1
),
portfolio_summary as (
    select
        sum(outstanding_principal) as total_outstanding_principal,
        sum(case when max_dpd > 30 then outstanding_principal else 0 end) as par30_exposure,
        sum(case when max_dpd > 90 then outstanding_principal else 0 end) as par90_exposure
    from transaction_exposure
),
transaction_stats as (
    select
        sum(purchase_value) as total_financed_value,
        avg(purchase_value) as average_ticket
    from {{ ref('fct_credit_transactions') }}
)
select
    t.total_financed_value,
    p.total_outstanding_principal as outstanding_principal,
    t.average_ticket,
    case when p.total_outstanding_principal > 0 then (cast(p.par30_exposure as real) / p.total_outstanding_principal) else 0 end as par30,
    case when p.total_outstanding_principal > 0 then (cast(p.par90_exposure as real) / p.total_outstanding_principal) else 0 end as par90
from transaction_stats t
cross join portfolio_summary p


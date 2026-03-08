with transactions as (
    select
        sum(purchase_value) as total_financed_value,
        avg(purchase_value) as average_ticket
    from {{ ref('fct_credit_transactions') }}
),
installments as (
    select
        sum(case when status in ('pending', 'late', 'default') then principal else 0 end) as outstanding_principal,
        sum(case when days_past_due > 30 then principal else 0 end) as par30_principal,
        sum(case when days_past_due > 90 then principal else 0 end) as par90_principal
    from {{ ref('fct_installments') }}
)
select
    t.total_financed_value,
    i.outstanding_principal,
    t.average_ticket,
    case when i.outstanding_principal > 0 then (i.par30_principal / i.outstanding_principal) else 0 end as par30,
    case when i.outstanding_principal > 0 then (i.par90_principal / i.outstanding_principal) else 0 end as par90
from transactions t
cross join installments i

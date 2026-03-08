with payments as (
    select count(*) as total_payments, sum(amount) as expected_cash
    from {{ ref('fct_payments') }}
),
settlements as (
    select count(*) as reconciled_payments, sum(amount) as settled_cash
    from {{ ref('stg_settlements') }}
)
select
    p.expected_cash,
    coalesce(s.settled_cash, 0) as settled_cash,
    p.expected_cash - coalesce(s.settled_cash, 0) as difference,
    case when p.total_payments > 0 then (cast(s.reconciled_payments as real) / p.total_payments) else 0 end as reconciliation_rate,
    p.total_payments - coalesce(s.reconciled_payments, 0) as unmatched_payments
from payments p
cross join settlements s

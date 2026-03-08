with all_installments as (
    select
        sum(expected_amount) as total_expected
    from {{ ref('fct_installments') }}
    where date(due_date) <= date('now')
),
all_payments as (
    select
        sum(amount) as actual_collection
    from {{ ref('fct_payments') }}
)
select
    i.total_expected as expected_collection,
    coalesce(p.actual_collection, 0) as actual_collection,
    case
        when i.total_expected > 0
        then (coalesce(p.actual_collection, 0) / i.total_expected)
        else 0
    end as collection_rate
from all_installments i
cross join all_payments p

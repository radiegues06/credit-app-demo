select
    i.installment_id,
    i.transaction_id,
    i.installment_number,
    i.due_date,
    i.principal,
    i.interest,
    (i.principal + i.interest) as expected_amount,
    i.status,
    case
        when i.status in ('late', 'default', 'pending') and date('now') > date(i.due_date)
        then cast(julianday('now') - julianday(i.due_date) as integer)
        else 0
    end as days_past_due,
    case
        when status = 'paid' then 'paid'
        when status = 'pending' and date('now') <= date(i.due_date) then 'current'
        when cast(julianday('now') - julianday(i.due_date) as integer) <= 30 then '0-30'
        when cast(julianday('now') - julianday(i.due_date) as integer) <= 60 then '31-60'
        when cast(julianday('now') - julianday(i.due_date) as integer) <= 90 then '61-90'
        else '90+'
    end as delinquency_bucket
from {{ ref('stg_installments') }} i

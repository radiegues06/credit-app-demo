with transactions as (
    select * from {{ ref('stg_transactions') }}
),
installments as (
    select * from {{ ref('stg_installments') }}
),
payments as (
    select * from {{ ref('stg_payments') }}
),
settlements as (
    select * from {{ ref('stg_settlements') }}
)

select
    t.transaction_id,
    t.transaction_date,
    t.merchant_id,
    t.customer_id,
    t.purchase_value,
    i.installment_id,
    i.installment_number,
    i.due_date,
    i.principal as installment_principal,
    i.interest as installment_interest,
    (i.principal + i.interest) as expected_installment_amount,
    i.status as installment_status,
    p.payment_id,
    p.payment_date,
    p.amount as paid_amount,
    p.payment_channel,
    s.settlement_id,
    s.settlement_date,
    s.amount as settled_amount,
    s.bank_reference,
    case 
        when s.settlement_id is not null then 'Settled'
        when p.payment_id is not null then 'Paid (Awaiting Settlement)'
        when date('now') > date(i.due_date) then 'Late'
        else 'Pending'
    end as reconciliation_status
from transactions t
join installments i on t.transaction_id = i.transaction_id
left join payments p on i.installment_id = p.installment_id
left join settlements s on p.payment_id = s.payment_id

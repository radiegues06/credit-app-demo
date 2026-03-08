select
    p.payment_id,
    p.installment_id,
    p.payment_date,
    p.amount,
    p.payment_channel,
    i.transaction_id,
    i.principal as installment_principal,
    i.interest as installment_interest,
    (i.principal + i.interest) as expected_amount,
    case
        when p.amount < (i.principal + i.interest) * 0.99 then true
        else false
    end as is_partial
from {{ ref('stg_payments') }} p
left join {{ ref('stg_installments') }} i
    on p.installment_id = i.installment_id

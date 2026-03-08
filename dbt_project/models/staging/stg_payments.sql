select
    payment_id,
    installment_id,
    payment_date,
    cast(amount as real) as amount,
    payment_channel
from {{ source('raw', 'raw_payments') }}

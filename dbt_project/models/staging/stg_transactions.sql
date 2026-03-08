select
    transaction_id,
    merchant_id,
    customer_id,
    cast(purchase_value as real) as purchase_value,
    cast(installments as integer) as installments,
    transaction_date
from {{ source('raw', 'raw_transactions') }}

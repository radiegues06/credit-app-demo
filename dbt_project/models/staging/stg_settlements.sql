select
    settlement_id,
    payment_id,
    settlement_date,
    cast(amount as real) as amount,
    bank_reference
from {{ source('raw', 'raw_settlements') }}

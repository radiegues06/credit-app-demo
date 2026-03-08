select
    installment_id,
    transaction_id,
    cast(installment_number as integer) as installment_number,
    due_date,
    cast(principal as real) as principal,
    cast(interest as real) as interest,
    status
from {{ source('raw', 'raw_installments') }}

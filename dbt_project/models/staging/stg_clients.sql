with source as (
    select * from {{ source('raw', 'raw_clients') }}
)

select
    client_id,
    name as client_name,
    address,
    job,
    email,
    phone_number,
    cast(income as real) as income,
    credit_risk,
    classification
from source

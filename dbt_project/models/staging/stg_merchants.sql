select
    merchant_id,
    merchant_name,
    segment,
    city
from {{ source('raw', 'raw_merchants') }}

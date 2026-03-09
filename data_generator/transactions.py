import uuid
import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')
np.random.seed(Config.SEED)

def generate_transactions(n=Config.NUM_TRANSACTIONS, merchant_ids=None, client_ids=None):
    if merchant_ids is None or client_ids is None:
        raise ValueError("merchant_ids and client_ids logic requires a list of valid IDs")
        
    transactions = []
    
    # 1 year range
    start_date = pd.Timestamp.now() - pd.DateOffset(years=1)
    
    for _ in range(n):
        # Lognormal distribution for ticket size, mean ~ AVG_TICKET
        mu = np.log(Config.AVG_TICKET) - 0.5
        ticket = np.random.lognormal(mean=mu, sigma=0.8)
        # Cap limits
        ticket = max(Config.MIN_TICKET, min(ticket, Config.MAX_TICKET))
        
        tx_date = fake.date_time_between(start_date=start_date, end_date="now")
        
        t = {
            "transaction_id": fake.uuid4(),
            "merchant_id": np.random.choice(merchant_ids),
            "customer_id": np.random.choice(client_ids),
            "purchase_value": round(ticket, 2),
            "installments": np.random.choice(Config.INSTALLMENTS_OPTIONS),
            "transaction_date": tx_date
        }
        transactions.append(t)
        
    return pd.DataFrame(transactions)

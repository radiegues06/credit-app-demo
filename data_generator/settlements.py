import pandas as pd
import numpy as np
from faker import Faker
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')
np.random.seed(Config.SEED)

def generate_settlements(payments_df):
    settlements = []
    
    for _, pay in payments_df.iterrows():
        # Missing settlements simulation
        if np.random.random() < Config.MISSING_SETTLEMENT_RATE:
            continue
            
        pay_date = pd.to_datetime(pay["payment_date"])
        
        # Determine settlement date
        # Pix: same/next day
        # Boleto: +1 to +3 business days
        # Credit Card: +30 days (simplified) or +2 days for anticipation
        if pay["payment_channel"] == "pix":
            delay = np.random.randint(0, 2)
        elif pay["payment_channel"] == "boleto":
            delay = np.random.randint(1, 4)
        else:
            delay = np.random.choice([2, 30])
            
        settlement_date = pay_date + pd.DateOffset(days=delay)
        
        stlt = {
            "settlement_id": fake.uuid4(),
            "payment_id": pay["payment_id"],
            "settlement_date": settlement_date,
            "amount": pay["amount"], # Simplification: assume zero fees extracted for now, or match exactly
            "bank_reference": fake.uuid4()
        }
        settlements.append(stlt)
        
    return pd.DataFrame(settlements)

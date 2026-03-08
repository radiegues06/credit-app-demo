import pandas as pd
import numpy as np
from faker import Faker
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')
np.random.seed(Config.SEED)

def generate_payments(installments_df):
    payments = []
    
    channels = ["pix", "boleto", "credit_card"]
    
    for _, inst in installments_df.iterrows():
        if inst["status"] not in ["paid", "late"]:
            continue
            
        due = pd.to_datetime(inst["due_date"])
        
        if inst["status"] == "paid":
            # On time or slightly early/late
            offset = np.random.randint(-5, 2)
            payment_date = due + pd.DateOffset(days=offset)
        else: # late
            offset = np.random.randint(5, 60)
            payment_date = due + pd.DateOffset(days=offset)
            
        base_amt = inst["principal"] + inst["interest"]
        
        # Partial payments
        if np.random.random() < Config.PARTIAL_PAYMENT_RATE:
            base_amt *= np.random.uniform(0.7, 0.95)
            
        payment = {
            "payment_id": fake.uuid4(),
            "installment_id": inst["installment_id"],
            "payment_date": payment_date,
            "amount": round(base_amt, 2),
            "payment_channel": np.random.choice(channels, p=[0.6, 0.3, 0.1])
        }
        payments.append(payment)
        
    return pd.DataFrame(payments)

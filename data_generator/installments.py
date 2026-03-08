import pandas as pd
import numpy as np
from datetime import timedelta
from faker import Faker
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')
np.random.seed(Config.SEED)

def generate_installments(transactions_df):
    installments = []
    
    now = pd.Timestamp.now()
    
    for _, tx in transactions_df.iterrows():
        n_inst = tx["installments"]
        base_principal = tx["purchase_value"] / n_inst
        interest = base_principal * Config.INTEREST_RATE
        
        tx_date = pd.to_datetime(tx["transaction_date"])
        
        for i in range(1, n_inst + 1):
            due_date = tx_date + pd.DateOffset(months=i)
            
            # Determine status
            if due_date > now:
                status = "pending"
            else:
                rand_val = np.random.random()
                if rand_val < Config.DEFAULT_RATE:
                    status = "default"
                elif rand_val < Config.DEFAULT_RATE + Config.LATE_PAYMENT_RATE:
                    status = "late"
                else:
                    status = "paid"
                    
            inst = {
                "installment_id": fake.uuid4(),
                "transaction_id": tx["transaction_id"],
                "installment_number": i,
                "due_date": due_date,
                "principal": round(base_principal, 2),
                "interest": round(interest, 2),
                "status": status
            }
            installments.append(inst)
            
    return pd.DataFrame(installments)

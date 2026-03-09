import uuid
import pandas as pd
import numpy as np
from faker import Faker
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')
np.random.seed(Config.SEED)

def generate_clients(n=Config.NUM_CLIENTS):
    clients = []
    
    # Credit risk classes and their probabilities
    risk_classes = ['A', 'B', 'C', 'D', 'E']
    risk_probs = [0.15, 0.30, 0.35, 0.15, 0.05]
    
    # Classifications
    classifications = ['Bronze', 'Silver', 'Gold', 'Platinum']
    
    for _ in range(n):
        # Generate varied income using a lognormal distribution to be realistic
        mu = np.log(4000) - 0.5
        income = np.random.lognormal(mean=mu, sigma=0.6)
        income = round(max(1412.0, min(income, 50000.0)), 2) # min limit around minimum wage
        
        client = {
            "client_id": fake.uuid4(),
            "name": fake.name(),
            "address": fake.address().replace('\n', ', '),
            "job": fake.job(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "income": income,
            "credit_risk": np.random.choice(risk_classes, p=risk_probs),
            "classification": np.random.choice(classifications)
        }
        clients.append(client)
        
    return pd.DataFrame(clients)

import pandas as pd
from faker import Faker
from .config import Config

Faker.seed(Config.SEED)
fake = Faker('pt_BR')

def generate_merchants(n=Config.NUM_MERCHANTS):
    merchants = []
    segments = ["electronics", "furniture", "fashion", "home_appliances", "sports"]
    
    for _ in range(n):
        merchant = {
            "merchant_id": fake.uuid4(),
            "merchant_name": fake.company(),
            "segment": fake.random_element(elements=segments),
            "city": fake.city()
        }
        merchants.append(merchant)
        
    return pd.DataFrame(merchants)

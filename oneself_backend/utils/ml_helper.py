import pickle
from datetime import datetime, timedelta

with open("models/ml_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_next_period(last_period, cycle_length):
    predicted_days = model.predict([[cycle_length]])[0]
    last_date = datetime.strptime(last_period, "%Y-%m-%d")
    next_period = last_date + timedelta(days=predicted_days)
    return next_period.strftime("%Y-%m-%d")

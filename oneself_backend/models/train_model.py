import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

def train_model():
    df = pd.read_csv("models/training_data.csv")

    X = df[['cycle_length']]
    y = df['next_cycle_length']

    model = LinearRegression()
    model.fit(X, y)

    with open("models/ml_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("ML model trained & saved")

if __name__ == "__main__":
    train_model()

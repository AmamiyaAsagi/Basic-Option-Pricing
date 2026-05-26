import numpy as np
import pandas as pd

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"

df = pd.read_csv(url)
df["SOFR"] = pd.to_numeric(df["SOFR"], errors="coerce")
df = df.dropna(subset=["SOFR"])

latest = df.iloc[-1]

S = float(input("Please enter S: "))
K = float(input("Please enter K: "))
T = float(input("Please enter T(in years): "))
Option_type = input("Call/Put: ")

r = float(latest["SOFR"]) / 100
q = 0.0
sigma = 0.2

steps = int(input("Please enter steps: "))
N = int(input("Please enter trials: "))

def MC(S, T, r, q, sigma, steps, N):
    dt = T / steps

    increments = (
        (r - q - 0.5 * sigma ** 2) * dt
        + sigma * np.sqrt(dt) * np.random.normal(size=(steps, N))
    )

    log_paths = np.log(S) + np.cumsum(increments, axis=0)
    return np.exp(log_paths)

def call_price(paths, K, r, T):
    payoffs = np.maximum(paths[-1] - K, 0)
    price = np.mean(payoffs) * np.exp(-r * T)
    return price

def put_price(paths, K, r, T):
    payoffs = np.maximum(K - paths[-1], 0)
    price = np.mean(payoffs) * np.exp(-r * T)
    return price

paths = MC(S, T, r, q, sigma, steps, N)

print(f"Latest SOFR date: {latest['observation_date']}")
print(f"Risk-free rate used: {r:.4%}")

if Option_type.lower() == "call":
    price = call_price(paths, K, r, T)
    print(f"Simulated European call price is {price:.4f}")
elif Option_type.lower() == "put":
    price = put_price(paths, K, r, T)
    print(f"Simulated European put price is {price:.4f}")
else:
    print("Invalid option type. Please enter Call or Put.")
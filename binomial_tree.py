import numpy as np
import pandas as pd
import math

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"

df = pd.read_csv(url)
df["SOFR"] = pd.to_numeric(df["SOFR"], errors="coerce")
df = df.dropna(subset=["SOFR"])

latest = df.iloc[-1]

S = float(input("Please enter S: "))
K = float(input("Please enter K: "))
T = float(input("Please enter T(in years): "))
Option_type = input("Call/Put: ")

steps = int(input("Please enter steps: "))

if S <= 0 or K <= 0 or T <= 0 or steps <= 0:
    raise ValueError("S, K, T, and steps must be positive.")

r = float(latest["SOFR"]) / 100
q = 0.0
sigma = 0.2

delta_t = T / steps

u = np.exp(sigma * np.sqrt(delta_t))
d = np.exp(-sigma * np.sqrt(delta_t))

p = (np.exp((r - q) * delta_t) - d) / (u - d)

if not (0 <= p <= 1):
    raise ValueError("Risk-neutral probability p is outside [0, 1]. Check parameters.")

price = 0

for k in range(steps + 1):
    probability = math.comb(steps, k) * p ** k * (1 - p) ** (steps - k)
    ST = S * u ** k * d ** (steps - k)

    if Option_type.lower() == "call":
        payoff = max(ST - K, 0)
    elif Option_type.lower() == "put":
        payoff = max(K - ST, 0)
    else:
        raise ValueError("Invalid option type. Please enter Call or Put.")

    price += payoff * probability

price *= np.exp(-r * T)

print(f"Latest SOFR date: {latest['observation_date']}")
print(f"Risk-free rate used: {r:.4%}")

if Option_type.lower() == "call":
    print(f"Binomial European call price is {price:.4f}")
elif Option_type.lower() == "put":
    print(f"Binomial European put price is {price:.4f}")
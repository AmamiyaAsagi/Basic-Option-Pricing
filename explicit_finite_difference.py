import numpy as np
import pandas as pd

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"

df = pd.read_csv(url)
df["SOFR"] = pd.to_numeric(df["SOFR"], errors="coerce")
df = df.dropna(subset=["SOFR"])

latest = df.iloc[-1]

S0 = float(input("Please enter S: "))
K = float(input("Please enter K: "))
T = float(input("Please enter T(in years): "))
r = float(latest["SOFR"]) / 100
delta_S = float(input("Please enter delta_S: "))
delta_t = float(input("Please enter delta_t(in years): "))

sigma = 0.2
q = 0.0

def explicit_finite_difference(S0, K, T, sigma, r, q, delta_S, delta_t, option_type):
    if S0 <= 0 or K <= 0:
        raise ValueError("S and K must be positive")
    if T < 0:
        raise ValueError("T must be non-negative")
    if delta_S <= 0 or delta_t <= 0:
        raise ValueError("delta_S and delta_t must be positive")

    Smax = max(3 * S0, 3 * K)
    M = max(3, int(np.ceil(Smax / delta_S)))
    Smax = M * delta_S

    max_dt = 0.9 / (sigma ** 2 * M ** 2 + r)
    N = max(1, int(np.ceil(T / min(delta_t, max_dt))))
    dt = T / N

    S = np.linspace(0, Smax, M + 1)

    if option_type == "Call":
        V = np.maximum(S - K, 0)
    elif option_type == "Put":
        V = np.maximum(K - S, 0)
    else:
        raise ValueError("option_type must be 'Call' or 'Put'")

    for n in range(N - 1, -1, -1):
        tau = T - n * dt
        V_new = V.copy()

        for i in range(1, M):
            a = 0.5 * dt * (sigma ** 2 * i ** 2 - (r - q) * i)
            b = 1 - dt * (sigma ** 2 * i ** 2 + r)
            c = 0.5 * dt * (sigma ** 2 * i ** 2 + (r - q) * i)

            V_new[i] = a * V[i - 1] + b * V[i] + c * V[i + 1]

        if option_type == "Call":
            V_new[0] = 0
            V_new[M] = Smax * np.exp(-q * tau) - K * np.exp(-r * tau)
        else:
            V_new[0] = K * np.exp(-r * tau)
            V_new[M] = 0

        V = V_new

    return np.interp(S0, S, V)

call_price = explicit_finite_difference(S0, K, T, sigma, r, q, delta_S, delta_t, "Call")
put_price = explicit_finite_difference(S0, K, T, sigma, r, q, delta_S, delta_t, "Put")

print(f"SOFR used: {r:.6%}")
print(f"Call price: {call_price:.4f}")
print(f"Put price: {put_price:.4f}")
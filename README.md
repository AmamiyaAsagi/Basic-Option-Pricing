# Basic Option Pricing

This project implements basic European option pricing methods in Python.  
It compares three numerical approaches: Monte Carlo simulation, binomial tree, and explicit finite difference method.

A key feature of this project is that the risk-free rate is retrieved from the latest SOFR data provided by FRED, rather than being manually fixed.

## Methods Implemented

### Monte Carlo Simulation

The Monte Carlo model simulates stock price paths under the geometric Brownian motion assumption and estimates the discounted expected payoff of European call or put options.

### Binomial Tree Model

The binomial tree model uses a discrete-time risk-neutral pricing framework.  
The model calculates the terminal payoff across possible stock price paths and discounts the expected payoff back to the present.

### Explicit Finite Difference Method

The explicit finite difference method numerically solves the Black-Scholes partial differential equation.  
The implementation prices both European call and put options using a discretized stock price and time grid.

## Key Features

- European call and put option pricing
- Monte Carlo simulation of stock price paths
- Binomial risk-neutral pricing
- Explicit finite difference approximation
- Real-time SOFR-based risk-free rate from FRED
- User-defined stock price, strike price, maturity, and numerical parameters

## Files

- `monte_carlo.py`: Monte Carlo simulation pricing model
- `binomial_tree.py`: Binomial tree pricing model
- `explicit_finite_difference.py`: Explicit finite difference pricing model

## Main Assumptions

- Constant volatility
- Zero dividend yield
- European-style options
- SOFR is used as the proxy for the risk-free rate

## Tools Used

- Python
- NumPy
- Pandas
- FRED SOFR data

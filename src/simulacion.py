import numpy as np

# 1. Cálculo del Valor Futuro (VF) de una anualidad discreta con datos del PDF
P = 161                     # Aporte mensual (Bs.)
r_annual = 0          # Tasa anual como 0.03 (3%)
r_monthly = r_annual / 12   # Tasa mensual efectiva
n_months = 120              # Número de meses (10 años)

if r_monthly != 0:
    FV = P * ((1 + r_monthly)**n_months - 1) / r_monthly
else:
    FV = P * n_months

print(f"1) Valor Futuro (anualidad discreta): Bs. {FV:,.2f}")

# 2. Simulación del modelo continuo (EDO) con RK4 usando parámetros de ejemplo
def dAdt(t, A, I0, g, c0, c1, c2, r):
    I = I0 * np.exp(g * t)
    C = c0 + c1 * I - c2 * A
    return I - C + r * A

# Parámetros de ejemplo para la EDO
I0 = 2061      # Ingreso inicial
g = 0.05       # Tasa de crecimiento de ingreso (anual)
c0 = 50        # Consumo autónomo
c1 = 0.9       # Propensión marginal al consumo
c2 = 0.1       # Efecto ahorro en consumo
r = 0      # Tasa de rendimiento (anual)
A = 161        # Ahorro inicial
t0 = 0         # Tiempo inicial (años)
T = 10         # Tiempo final (años)
dt = 0.1       # Paso de integración (años)

n_steps = int((T - t0) / dt)
t = t0

for _ in range(n_steps):
    k1 = dAdt(t, A, I0, g, c0, c1, c2, r)
    k2 = dAdt(t + dt/2, A + k1 * dt/2, I0, g, c0, c1, c2, r)
    k3 = dAdt(t + dt/2, A + k2 * dt/2, I0, g, c0, c1, c2, r)
    k4 = dAdt(t + dt, A + k3 * dt, I0, g, c0, c1, c2, r)
    A = A + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
    t += dt

print(f"2) Valor acumulado (modelo continuo EDO): Bs. {A:,.2f}")

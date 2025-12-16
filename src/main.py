import pandas as pd
from src.models import sir_model
from src.explicit_solvers import euler_explicit
from src.stiff_solvers import solve_ivp_solver
from src.visualization import (
    plot_failure,
    plot_comparison,
    plot_model_vs_data
)
from src.dataset import load_dbd_data

# =========================
# LOAD DATASET DBD
# =========================
data_dbd = load_dbd_data()

# =========================
# INITIAL CONDITION
# =========================
I0 = data_dbd["cases_norm"].iloc[0]
y0 = [1 - I0, I0, 0.0]
t_span = (0, len(data_dbd))

# =========================
# EULER FAILURE
# =========================
t_euler, y_euler = euler_explicit(
    lambda t,y: sir_model(t,y),
    t_span,
    y0,
    h=0.01
)
plot_failure(t_euler, y_euler, "output/euler_failure.png")

# =========================
# STIFF SOLVERS
# =========================
sol_rk45 = solve_ivp_solver(sir_model, t_span, y0, "RK45")
sol_bdf   = solve_ivp_solver(sir_model, t_span, y0, "BDF")
sol_radau = solve_ivp_solver(sir_model, t_span, y0, "Radau")

plot_comparison(sol_rk45, sol_bdf, sol_radau,
                "output/solver_comparison.png")

# =========================
# MODEL vs DATA
# =========================
plot_model_vs_data(
    sol_bdf,
    data_dbd,
    "output/model_vs_data.png"
)

# =========================
# PERFORMANCE TABLE
# =========================
df_perf = pd.DataFrame({
    "Solver": ["RK45", "BDF", "Radau"],
    "nfev": [sol_rk45.nfev, sol_bdf.nfev, sol_radau.nfev],
    "Status": [sol_rk45.success, sol_bdf.success, sol_radau.success]
})

df_perf.to_csv("output/performance_table.csv", index=False)
print(df_perf)

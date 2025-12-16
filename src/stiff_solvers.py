from scipy.integrate import solve_ivp

def solve_ivp_solver(f, t_span, y0, method):
    return solve_ivp(
        f,
        t_span,
        y0,
        method=method,
        atol=1e-8,
        rtol=1e-6
    )

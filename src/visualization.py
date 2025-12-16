import matplotlib.pyplot as plt

def plot_failure(t, y, filename):
    plt.figure()
    plt.plot(t, y[:,1])
    plt.title("Euler Explicit Failure (Stiff System)")
    plt.xlabel("Time")
    plt.ylabel("Infected")
    plt.savefig(filename)
    plt.close()

def plot_comparison(sol_rk45, sol_bdf, sol_radau, filename):
    plt.figure()
    plt.plot(sol_rk45.t, sol_rk45.y[1], '--', label="RK45")
    plt.plot(sol_bdf.t, sol_bdf.y[1], label="BDF")
    plt.plot(sol_radau.t, sol_radau.y[1], label="Radau")
    plt.xlabel("Time")
    plt.ylabel("Infected")
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_model_vs_data(sol, data, filename):
    plt.figure()
    plt.plot(sol.t, sol.y[1], label="Model")
    plt.scatter(data["time"], data["cases_norm"],
                color="red", s=20, label="Data DBD")
    plt.legend()
    plt.savefig(filename)
    plt.close()

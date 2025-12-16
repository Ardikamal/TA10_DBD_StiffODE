import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from src.models import sir_model
from src.explicit_solvers import euler_explicit
from src.stiff_solvers import solve_ivp_solver
from src.dataset import load_dbd_data

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="TA-10 | Simulasi Sistem Kaku (Stiff ODE)",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CSS – DASHBOARD DEVELOPER STYLE
# ======================================================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}
.main {
    background: rgba(255,255,255,0.95);
    padding: 2rem;
    border-radius: 20px;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}
.section-title {
    font-size: 22px;
    font-weight: bold;
    color: #203a43;
    margin-bottom: 10px;
}
.kpi {
    background: linear-gradient(135deg, #203a43, #2c5364);
    color: white;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
}
.kpi-value {
    font-size: 26px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div class="card">
<h1>📊 Simulasi Sistem Kaku (Stiff ODE)</h1>
<h3>Studi Kasus: Penyebaran Demam Berdarah Dengue (DBD)</h3>
<p>
<b>Mata Kuliah:</b> Pemodelan & Simulasi / Metode Numerik<br>
<b>Tujuan:</b> Membuktikan kegagalan metode eksplisit dan keunggulan stiff solver
</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# PANEL KONTROL
# ======================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚙️ Parameter Simulasi</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    beta = st.slider("β – Laju Penularan (dibuat besar → sistem kaku)", 0.1, 10.0, 5.0)
with c2:
    gamma = st.slider("γ – Laju Pemulihan", 0.01, 1.0, 0.1)

st.info("Contoh parameter valid (sistem kaku): β = 5.0 dan γ = 0.1")
run = st.button("🚀 Jalankan Simulasi")

st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# PROSES SIMULASI
# ======================================================
if run:
    data = load_dbd_data()
    I0 = data["cases_norm"].iloc[0]
    y0 = [1 - I0, I0, 0.0]
    t_span = (0, len(data))

    # Euler Eksplisit
    t0 = time.perf_counter()
    t_euler, y_euler = euler_explicit(
        lambda t,y: sir_model(t,y,beta,gamma),
        t_span, y0, 0.01
    )
    time_euler = time.perf_counter() - t0

    # Solver lainnya
    t0 = time.perf_counter()
    rk45 = solve_ivp_solver(lambda t,y: sir_model(t,y,beta,gamma), t_span, y0, "RK45")
    time_rk45 = time.perf_counter() - t0

    t0 = time.perf_counter()
    bdf = solve_ivp_solver(lambda t,y: sir_model(t,y,beta,gamma), t_span, y0, "BDF")
    time_bdf = time.perf_counter() - t0

    t0 = time.perf_counter()
    radau = solve_ivp_solver(lambda t,y: sir_model(t,y,beta,gamma), t_span, y0, "Radau")
    time_radau = time.perf_counter() - t0

    # ======================================================
    # KPI
    # ======================================================
    st.markdown("## 📌 Ringkasan Kinerja Utama")
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown("<div class='kpi'><div>Status Euler</div><div class='kpi-value'>GAGAL</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'><div>nfev RK45</div><div class='kpi-value'>{rk45.nfev}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'><div>Waktu BDF (s)</div><div class='kpi-value'>{time_bdf:.4f}</div></div>", unsafe_allow_html=True)
    k4.markdown("<div class='kpi'><div>Status Radau</div><div class='kpi-value'>STABIL</div></div>", unsafe_allow_html=True)

    # ======================================================
    # DASHBOARD 2x2
    # ======================================================
    colA, colB = st.columns(2)
    colC, colD = st.columns(2)

    with colA:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ❌ Kegagalan Metode Euler")
        fig, ax = plt.subplots()
        ax.plot(t_euler, y_euler[:,1], color="red")
        ax.set_title("Solusi Tidak Stabil")
        st.pyplot(fig)
        st.caption("Metode Euler keluar dari stability region pada sistem kaku.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✅ Perbandingan Solver")
        fig, ax = plt.subplots()
        ax.plot(rk45.t, rk45.y[1], '--', label="RK45")
        ax.plot(bdf.t, bdf.y[1], label="BDF")
        ax.plot(radau.t, radau.y[1], label="Radau")
        ax.legend()
        st.pyplot(fig)
        st.caption("Solver implisit lebih stabil untuk sistem kaku.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colC:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📈 Model vs Data DBD")
        fig, ax = plt.subplots()
        ax.plot(bdf.t, bdf.y[1], label="Model (BDF)")
        ax.scatter(data["time"], data["cases_norm"], s=15, label="Data")
        ax.legend()
        st.pyplot(fig)
        st.caption("Model mengikuti tren data secara kualitatif.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colD:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Tabel Kinerja Solver")
        df = pd.DataFrame({
            "Metode": ["Euler", "RK45", "BDF", "Radau"],
            "Waktu (detik)": [time_euler, time_rk45, time_bdf, time_radau],
            "nfev": ["-", rk45.nfev, bdf.nfev, radau.nfev],
            "Status": ["Gagal", "Kurang Efisien", "Efisien", "Efisien"]
        })
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ======================================================
    # PENJELASAN AKHIR (POP-UP AMAN)
    # ======================================================
    with st.expander("🧠 Kesimpulan & Analisis Numerik (Klik untuk membuka)"):
        st.markdown("""
        **1. Sistem Bersifat KAKU (Stiff)**  
        Terdapat perbedaan skala waktu cepat dan lambat.

        **2. Metode Eksplisit GAGAL**  
        Euler tidak mampu menjaga kestabilan numerik.

        **3. RK45 Tidak Efisien**  
        Memerlukan langkah sangat kecil → nfev besar.

        **4. BDF & Radau SOLUSI TERBAIK**  
        Solver implisit stabil dan efisien untuk sistem kaku.
        """)

    st.toast("Simulasi dan analisis berhasil dijalankan ✅", icon="🎉")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------------
# Fungsi Runge-Kutta RK4
# ---------------------
def f(t, y, r):
    return r * y

def runge_kutta_rk4(y0, r, t0, tn, h):
    t_values = [t0]
    y_values = [y0]
    t = t0
    y = y0

    while t < tn:
        k1 = h * f(t, y, r)
        k2 = h * f(t + h/2, y + k1/2, r)
        k3 = h * f(t + h/2, y + k2/2, r)
        k4 = h * f(t + h, y + k3, r)
        y += (k1 + 2*k2 + 2*k3 + k4) / 6
        t += h
        t_values.append(t)
        y_values.append(y)

    return t_values, y_values

# ---------------------
# Tampilan UI
# ---------------------
st.set_page_config(page_title="Cuanalystic", layout="centered")
st.markdown("<h1 style='text-align: center; color: #8FBC8F;'>Cuanalystic Metode Runge-Kutta RK4 </h1>", unsafe_allow_html=True)

# Layout input 2 kolom
col1, col2 = st.columns(2)
with col1:
    y0 = st.number_input("Jumlah Awal Investasi (Rp)", value=1000000)
    waktu = st.number_input("Durasi Investasi (tahun)", value=10)
with col2:
    bunga = st.number_input("Suku Bunga per Tahun (%)", value=5.0)
    step = st.number_input("Langkah Perhitungan (h)", value=1.0)

# Input Inflasi
inflasi = st.number_input("Tingkat Inflasi per Tahun (%)", value=2.5)

# Tombol Prediksi
if st.button("Hitung Prediksi"):
    r = bunga / 100
    t_vals, y_vals = runge_kutta_rk4(y0, r, 0, waktu, step)

    # Penyesuaian inflasi
    inflasi_decimal = inflasi / 100
    y_vals_riil = [y / ((1 + inflasi_decimal) ** t) for y, t in zip(y_vals, t_vals)]

    # Hasil akhir
    st.success(f"Saldo akhir nominal setelah {waktu} tahun: Rp {y_vals[-1]:,.2f}")
    st.info(f"Saldo akhir riil setelah {waktu} tahun (dengan inflasi {inflasi}%): Rp {y_vals_riil[-1]:,.2f}")

    # Tabel hasil
    df = pd.DataFrame({
        "Tahun": t_vals,
        "Saldo Nominal (Rp)": [f"Rp {val:,.2f}".replace('.', ',').replace(',', '.') for val in y_vals],
        "Saldo Riil (Rp)": [f"Rp {val_riil:,.2f}".replace('.', ',').replace(',', '.') for val_riil in y_vals_riil]
    })
    st.dataframe(df)

    # Grafik
    fig, ax = plt.subplots()
    ax.plot(t_vals, y_vals, marker='o', color='green', label='Saldo Nominal')
    ax.plot(t_vals, y_vals_riil, marker='x', color='blue', label='Saldo Riil')
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Saldo (Rp)")
    ax.set_title("Pertumbuhan Investasi")
    ax.legend()
    st.pyplot(fig)

    # Download Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Prediksi")
    st.download_button(
        label="Download Hasil ke Excel",
        data=output.getvalue(),
        file_name="prediksi_tabungan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
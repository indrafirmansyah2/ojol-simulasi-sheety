import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Simulasi Penghasilan Ojol Maxim", layout="centered")

st.title("💰 Simulasi Penghasilan Ojol Maxim")

nama = st.text_input("Nama:")
lokasi = st.text_input("Lokasi:")
penghasilan_kotor = st.number_input("Penghasilan Kotor (per hari):", min_value=0, step=1000)
tip = st.number_input("Tip (opsional):", min_value=0, step=500)

if penghasilan_kotor > 0:
    # Potongan wajib
    komisi_maxim = penghasilan_kotor * 0.12  # 12%
    bbm = penghasilan_kotor * 0.16           # 16%
    total_potongan = komisi_maxim + bbm

    # Penyisihan
    oli = penghasilan_kotor * 0.02
    servis_ringan = penghasilan_kotor * 0.015
    servis_berat = penghasilan_kotor * 0.025
    ban = penghasilan_kotor * 0.02
    aki = penghasilan_kotor * 0.01
    dana_darurat = penghasilan_kotor * 0.03
    total_penyisihan = oli + servis_ringan + servis_berat + ban + aki + dana_darurat

    # Sisa
    dibawa_tanpa_penyisihan = penghasilan_kotor - total_potongan + tip
    dibawa_bersih = dibawa_tanpa_penyisihan - total_penyisihan

    st.subheader("🧾 Rincian Potongan")
    st.write(f"🛵 Komisi Maxim (12%): Rp {komisi_maxim:,.0f}")
    st.write(f"⛽ BBM (16%): Rp {bbm:,.0f}")
    st.success(f"Total Potongan: Rp {total_potongan:,.0f}")

    st.subheader("🔧 Rincian Penyisihan")
    st.write(f"🔧 Oli (2%): Rp {oli:,.0f}")
    st.write(f"🛠️ Servis Ringan (1.5%): Rp {servis_ringan:,.0f}")
    st.write(f"⚙️ Servis Berat (2.5%): Rp {servis_berat:,.0f}")
    st.write(f"🚗 Ban (2%):

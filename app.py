import streamlit as st
import datetime
import pandas as pd
import requests

SHEET_URL = "https://api.sheety.co/3c5236c6b6460d3f9f3fcb96a92ad3aa/simulasiPendapatanOjolMaxim/sheet1"

st.set_page_config(page_title="Simulasi Ojol Maxim", layout="centered")
st.title("🛵 Simulasi Penghasilan Ojol Maxim")

# Input Data
penghasilan_kotor = st.number_input("Penghasilan Kotor (per hari):", min_value=0, value=80000, step=1000)
tanggal = st.date_input("Tanggal", value=datetime.date.today())
tip = st.number_input("Tip dari Pelanggan (jika ada):", min_value=0, value=0, step=1000)

# Perhitungan
komisi = 0.10 * penghasilan_kotor
bbm = 0.18 * penghasilan_kotor
total_potongan = komisi + bbm
oli = 0.02 * penghasilan_kotor
servis_ringan = 0.015 * penghasilan_kotor
servis_berat = 0.025 * penghasilan_kotor
ban = 0.02 * penghasilan_kotor
aki = 0.01 * penghasilan_kotor
dana_darurat = 0.03 * penghasilan_kotor
total_penyisihan = oli + servis_ringan + servis_berat + ban + aki + dana_darurat
bersih = (penghasilan_kotor - total_potongan - total_penyisihan) + tip

# Tampilkan Ringkasan
st.markdown("---")
st.subheader("💡 Ringkasan Harian")
st.write(f"📆 Tanggal: {tanggal}")
st.write(f"💰 Penghasilan Kotor: Rp {penghasilan_kotor:,.0f}")
st.write(f"🎁 Tip: Rp {tip:,.0f}")
st.write(f"💼 Bersih Dibawa Pulang: Rp {bersih:,.0f}")

# Simpan ke Sheety
if st.button("💾 Simpan ke Google Sheet"):
    payload = {
        "sheet1": {
            "tanggal": str(tanggal),
            "penghasilan_kotor": penghasilan_kotor,
            "tip": tip,
            "bersih_dibawa_pulang": int(bersih)
        }
    }
    res = requests.post(SHEET_URL, json=payload)
    if res.status_code == 201:
        st.success("✅ Data berhasil disimpan ke Sheety!")
    else:
        st.error(f"❌ Gagal menyimpan: {res.status_code}")

# Ambil dan tampilkan tabel
st.markdown("---")
st.subheader("📊 Riwayat Simulasi")
try:
    resp = requests.get(SHEET_URL)
    resp.raise_for_status()
    data = resp.json().get("sheet1", [])
    df = pd.DataFrame(data)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="riwayat_simulasi.csv", mime="text/csv")
except Exception as e:
    st.error("❌ Gagal memuat data dari Sheety.")


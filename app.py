import streamlit as st
import requests
import pandas as pd
from io import StringIO

API_URL = "https://api.sheety.co/3c5236c6b6460d3f9f3fcb96a92ad3aa/simulasiPendapatanOjolMaxim/sheet1"

st.title("Simulasi Pendapatan Ojol (Maxim)")
st.markdown("Aplikasi ini menghitung pendapatan bersih dan menyimpannya ke Google Sheets.")

# Form
with st.form("simulasi_form"):
    nama = st.text_input("Nama")
    lokasi = st.text_input("Lokasi")
    jumlah_orderan = st.number_input("Jumlah Orderan", min_value=0, step=1)
    penghasilan = st.number_input("Total Penghasilan (Rp)", min_value=0)
    bensin = st.number_input("Biaya Bensin (Rp)", min_value=0)
    makan = st.number_input("Biaya Makan (Rp)", min_value=0)
    lain = st.number_input("Biaya Lain-Lain (Rp)", min_value=0)
    submitted = st.form_submit_button("Hitung & Simpan")

    if submitted:
        total_biaya = bensin + makan + lain
        pendapatan_bersih = penghasilan - total_biaya

        st.success(f"Pendapatan Bersih: Rp{pendapatan_bersih:,.0f}")

        data = {
            "sheet1": {
                "nama": nama,
                "lokasi": lokasi,
                "jumlahOrderan": jumlah_orderan,
                "penghasilan": penghasilan,
                "bensin": bensin,
                "makan": makan,
                "lain": lain,
                "pendapatanBersih": pendapatan_bersih
            }
        }

        # Kirim ke Sheety
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            st.success("Data berhasil disimpan ke Google Sheets!")
        else:
            st.error("Gagal menyimpan data. Periksa API.")

# Ambil semua data dari Google Sheets
if st.button("Lihat Data & Download"):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json().get("sheet1", [])
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "data_ojol.csv", "text/csv")
    else:
        st.error("Gagal mengambil data.")

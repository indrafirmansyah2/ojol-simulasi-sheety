import streamlit as st
import requests
import datetime

st.title("Simulasi Pendapatan Ojol Maxim")

nama = st.text_input("Nama")
lokasi = st.text_input("Lokasi")
biaya = st.number_input("Biaya perjalanan (Rp)", min_value=0)
tip = st.number_input("Tip tambahan (Rp)", min_value=0)

if st.button("Kirim dan Simpan"):
    total = biaya + tip
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    url = "https://api.sheety.co/3c5236c6b6460d3f9f3fcb96a92ad3aa/simulasiPendapatanOjolMaxim/sheet1"
    body = {
        "sheet1": {
            "nama": nama,
            "lokasi": lokasi,
            "biaya": biaya,
            "tip": tip,
            "total": total,
            "tanggal": tanggal
        }
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        st.success("Data berhasil disimpan!")
    else:
        st.error("Gagal menyimpan data.")

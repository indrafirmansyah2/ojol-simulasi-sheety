import streamlit as st
import requests
from datetime import datetime

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

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
    st.write(f"🛵 Komisi Maxim (12%): {format_rupiah(komisi_maxim)}")
    st.write(f"⛽ BBM (16%): {format_rupiah(bbm)}")
    st.success(f"Total Potongan: {format_rupiah(total_potongan)}")

    st.subheader("🔧 Rincian Penyisihan")
    st.write(f"🔧 Oli (2%): {format_rupiah(oli)}")
    st.write(f"🛠️ Servis Ringan (1.5%): {format_rupiah(servis_ringan)}")
    st.write(f"⚙️ Servis Berat (2.5%): {format_rupiah(servis_berat)}")
    st.write(f"🚗 Ban (2%): {format_rupiah(ban)}")
    st.write(f"🔋 Aki (1%): {format_rupiah(aki)}")
    st.write(f"💰 Dana Darurat (3%): {format_rupiah(dana_darurat)}")
    st.success(f"Total Penyisihan: {format_rupiah(total_penyisihan)}")

    st.subheader("📦 Hasil Bersih")
    st.write(f"🧾 Dibawa Pulang (tanpa penyisihan): {format_rupiah(dibawa_tanpa_penyisihan)}")
    st.success(f"💼 Bersih Dibawa Pulang: {format_rupiah(dibawa_bersih)}")

    # Simpan ke Sheety
    if st.button("💾 Simpan ke Google Sheets"):
        url = "https://api.sheety.co/3c5236c6b6460d3f9f3fcb96a92ad3aa/simulasiPendapatanOjolMaxim/sheet1"
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "sheet1": {
                "nama": nama,
                "lokasi": lokasi,
                "kotor": penghasilan_kotor,
                "tip": tip,
                "totalPotongan": round(total_potongan),
                "totalPenyisihan": round(total_penyisihan),
                "dibawaTanpaPenyisihan": round(dibawa_tanpa_penyisihan),
                "dibawaBersih": round(dibawa_bersih),
                "tanggal": tanggal
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == 201:
            st.success("✅ Data berhasil disimpan ke Google Sheets.")
        else:
            st.error("❌ Gagal menyimpan data.")

import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Simulasi Ojol Maxim", page_icon="🛵")

st.title("🛵 Simulasi Penghasilan Ojol Maxim")

# Input pengguna
nama = st.text_input("Nama")
lokasi = st.text_input("Lokasi")
kotor = st.number_input("Penghasilan Kotor (per hari):", min_value=0, step=1000, format="%d")
tip = st.number_input("Tip (opsional):", min_value=0, step=1000, format="%d")

# Hitungan potongan dan penyisihan
komisi = 0.10 * kotor
bbm = 0.18 * kotor
total_potongan = komisi + bbm

oli = 0.02 * kotor
servis_ringan = 0.015 * kotor
servis_berat = 0.025 * kotor
ban = 0.02 * kotor
aki = 0.01 * kotor
darurat = 0.03 * kotor
total_penyisihan = oli + servis_ringan + servis_berat + ban + aki + darurat

dibawa_tanpa_penyisihan = kotor + tip - total_potongan
dibawa_bersih = dibawa_tanpa_penyisihan - total_penyisihan
tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tampilkan hasil
st.divider()
st.subheader("📋 Rincian")

st.write(f"🛵 **Komisi Maxim (10%)**: Rp {komisi:,.0f}")
st.write(f"⛽ **BBM (18%)**: Rp {bbm:,.0f}")
st.info(f"**Total Potongan**: Rp {total_potongan:,.0f}")

st.write(f"🔧 **Oli (2%)**: Rp {oli:,.0f}")
st.write(f"🔧 **Servis Ringan (1.5%)**: Rp {servis_ringan:,.0f}")
st.write(f"⚙️ **Servis Berat (2.5%)**: Rp {servis_berat:,.0f}")
st.write(f"🚗 **Ban (2%)**: Rp {ban:,.0f}")
st.write(f"🔋 **Aki (1%)**: Rp {aki:,.0f}")
st.write(f"💰 **Dana Darurat (3%)**: Rp {darurat:,.0f}")
st.info(f"**Total Penyisihan**: Rp {total_penyisihan:,.0f}")

st.write(f"💵 **Dibawa Pulang (tanpa penyisihan)**: Rp {dibawa_tanpa_penyisihan:,.0f}")
st.success(f"💼 **Bersih Dibawa Pulang**: Rp {dibawa_bersih:,.0f}")

# Kirim ke Sheety
if st.button("Simpan ke Google Sheets"):
    url = "https://api.sheety.co/3c5236c6b6460d3f9f3fcb96a92ad3aa/simulasiPendapatanOjolMaxim/sheet1"  # GANTI kalau ID kamu beda
    body = {
        "sheet1": {
            "nama": nama,
            "lokasi": lokasi,
            "kotor": kotor,
            "tip": tip,
            "totalPotongan": total_potongan,
            "totalPenyisihan": total_penyisihan,
            "dibawaTanpaPenyisihan": dibawa_tanpa_penyisihan,
            "dibawaBersih": dibawa_bersih,
            "tanggal": tanggal
        }
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        st.success("✅ Data berhasil disimpan ke Google Sheets!")
    else:
        st.error(f"❌ Gagal menyimpan data. Kode: {response.status_code}")

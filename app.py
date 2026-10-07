import streamlit as st
import pandas as pd

from scrapers.sbb import get_sbb_ilanlari
from scrapers.ilan_gov import get_ilan_gov_tr_ilanlari
from scrapers.resmi_gazete import get_resmi_gazete_ilanlari
from scrapers.kariyer_kapisi import get_kariyer_kapisi_ilanlari
from scrapers.iskur import get_iskur_kamu_ilanlari

st.set_page_config(
    page_title="KPSS & Kamu Atama Takip Paneli",
    page_icon="📌",
    layout="wide"
)

st.title("📌 KPSS Kamu Atama & İlan Takip Paneli")
st.caption("Kariyer Kapısı, SBB Kamu İlan, ilan.gov.tr, Resmi Gazete ve İŞKUR ilanları")

# Session state başlatma (Hafızayı koru)
if 'raw_ilanlar' not in st.session_state:
    st.session_state['raw_ilanlar'] = []

# Yan Menü (Sidebar) - Filtreler
st.sidebar.header("🔍 İlan Filtreleri")
secilen_kaynaklar = st.sidebar.multiselect(
    "Takip Edilecek Kaynaklar:",
    ["Kamu İlan (SBB)", "ilan.gov.tr", "Resmi Gazete", "Kariyer Kapısı", "İŞKUR"],
    default=["Kamu İlan (SBB)", "ilan.gov.tr", "Resmi Gazete", "Kariyer Kapısı", "İŞKUR"]
)

arama_kelimesi = st.sidebar.text_input("Anahtar Kelime Ara (Örn: Büro, Mühendis, Temizlik):")

# Taramayı Başlat Butonu
if st.button("🔄 Seçili Siteleri Tara ve Güncelle", type="primary"):
    with st.spinner("Seçtiğin kamu siteleri taranıyor, lütfen bekleyin..."):
        tum_ilanlar = []
        
        if "Kamu İlan (SBB)" in secilen_kaynaklar:
            tum_ilanlar.extend(get_sbb_ilanlari())
            
        if "ilan.gov.tr" in secilen_kaynaklar:
            tum_ilanlar.extend(get_ilan_gov_tr_ilanlari())
            
        if "Resmi Gazete" in secilen_kaynaklar:
            tum_ilanlar.extend(get_resmi_gazete_ilanlari())
            
        if "Kariyer Kapısı" in secilen_kaynaklar:
            tum_ilanlar.extend(get_kariyer_kapisi_ilanlari())
            
        if "İŞKUR" in secilen_kaynaklar:
            tum_ilanlar.extend(get_iskur_kamu_ilanlari())
            
        st.session_state['raw_ilanlar'] = tum_ilanlar
        st.success(f"Tarama tamamlandı! Toplam {len(tum_ilanlar)} ilan çekildi.")

# Hafızadaki verileri göster
ilanlar = st.session_state['raw_ilanlar']

if ilanlar:
    df = pd.DataFrame(ilanlar)
    
    # Arama filtresi uygula
    if arama_kelimesi.strip():
        df = df[df['Başlık'].str.contains(arama_kelimesi.strip(), case=False, na=False)]
        
    st.markdown(f"### 📋 Güncel İlan Listesi ({len(df)} İlan Gösteriliyor)")
    
    if df.empty:
        st.warning("Aradığınız kelimeye uygun ilan bulunamadı. Lütfen arama kutusunu temizleyin.")
    else:
        for idx, row in df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 5, 1])
                with col1:
                    st.subheader(row['Kurum'])
                    st.caption(f"Kaynak: {row['Kaynak']}")
                with col2:
                    st.write(f"**{row['Başlık']}**")
                with col3:
                    if row['Link']:
                        st.link_button("İlana Git 🔗", row['Link'])
                st.divider()
else:
    st.info("İlanları listelemek için **'Seçili Siteleri Tara ve Güncelle'** butonuna tıklayın.")

import streamlit as st
import pandas as pd
from scrapers.sbb import get_sbb_ilanlari
from scrapers.ilan_gov import get_ilan_gov_tr_ilanlari

st.set_page_config(
    page_title="KPSS & Kamu Atama Takip Paneli",
    page_icon="📌",
    layout="wide"
)

st.title("📌 KPSS Kamu Atama & İlan Takip Paneli")
st.caption("Resmi kamu kaynaklarından anlık ilan takibi")

# Yan Menü (Sidebar)
st.sidebar.header("🔍 İlan Filtreleri")
secilen_kaynaklar = st.sidebar.multiselect(
    "Takip Edilecek Kaynaklar:",
    ["Kamu İlan (SBB)", "ilan.gov.tr", "Kariyer Kapısı", "Resmi Gazete", "İŞKUR"],
    default=["Kamu İlan (SBB)", "ilan.gov.tr"]
)

arama_kelimesi = st.sidebar.text_input("Anahtar Kelime Ara (Örn: Büro, Mühendis, Temizlik):")

# Taramayı Başlat Butonu
if st.button("🔄 Seçili Siteleri Tara ve Güncelle", type="primary"):
    with st.spinner("Kamu siteleri taranıyor, lütfen bekleyin..."):
        tum_ilanlar = []
        
        if "Kamu İlan (SBB)" in secilen_kaynaklar:
            tum_ilanlar.extend(get_sbb_ilanlari())
            
        if "ilan.gov.tr" in secilen_kaynaklar:
            tum_ilanlar.extend(get_ilan_gov_tr_ilanlari())
            
        st.session_state['ilanlar'] = tum_ilanlar
        st.success(f"Tarama tamamlandı! Toplam {len(tum_ilanlar)} ilan bulundu.")

# İlanları Ekrana Bas
if 'ilanlar' in st.session_state and st.session_state['ilanlar']:
    df = pd.DataFrame(st.session_state['ilanlar'])
    
    # Filtreleme
    if arama_kelimesi:
        df = df[df['Başlık'].str.contains(arama_kelimesi, case=False, na=False)]
        
    st.markdown(f"### 📋 Güncel İlan Listesi ({len(df)} İlan)")
    
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
    st.info("İlanları listelemek için soldan kaynakları seçip **'Seçili Siteleri Tara ve Güncelle'** butonuna tıklayın.")

import requests
from bs4 import BeautifulSoup

def get_resmi_gazete_ilanlari():
    """Resmi Gazete Çeşitli İlanlar / Personel Alım İlanlarını çeker."""
    url = "https://www.resmigazete.gov.tr/cesitli-ilanlar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    ilanlar = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        
        # İlan bağlantılarını bul
        links = soup.find_all("a")
        for a in links:
            title = a.get_text(strip=True)
            href = a.get("href", "")
            
            # Personel, alım veya kpss geçen ilanları filtrele
            if any(k in title.lower() for k in ["personel", "alım", "müfettiş", "uzman", "sözleşmeli", "memur", "kpss"]):
                if href and not href.startswith("http"):
                    href = f"https://www.resmigazete.gov.tr/{href.lstrip('/')}"
                
                ilanlar.append({
                    "Kurum": "Resmi Gazete İlanı",
                    "Başlık": title,
                    "Tarih": "Güncel",
                    "Link": href,
                    "Kaynak": "Resmi Gazete"
                })
    except Exception as e:
        print(f"Resmi Gazete çekme hatası: {e}")
        
    return ilanlar

import requests
from bs4 import BeautifulSoup

def get_iskur_kamu_ilanlari():
    """İŞKUR Kamu Memur/Personel Alım ilanlarını çeker."""
    url = "https://www.iskur.gov.tr/is-arayan/kamu-memur-alim-ilanlari/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    ilanlar = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        
        rows = soup.find_all("tr") or soup.find_all("div", class_="news-item")
        for row in rows:
            link_elem = row.find("a")
            if link_elem:
                title = link_elem.get_text(strip=True)
                link = link_elem.get("href", "")
                
                if link and not link.startswith("http"):
                    link = f"https://www.iskur.gov.tr{link}"
                
                if len(title) > 10 and ("alım" in title.lower() or "personel" in title.lower() or "memur" in title.lower()):
                    ilanlar.append({
                        "Kurum": "İŞKUR Kamu Alımları",
                        "Başlık": title,
                        "Tarih": "Güncel",
                        "Link": link,
                        "Kaynak": "İŞKUR"
                    })
    except Exception as e:
        print(f"İŞKUR çekme hatası: {e}")
        
    return ilanlar

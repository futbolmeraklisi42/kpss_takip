import requests
from bs4 import BeautifulSoup

def get_ilan_gov_tr_ilanlari():
    url = "https://www.ilan.gov.tr/kategori-tum-ilanlar/personel-alimi-akademik-kadro-ilanlari"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    ilanlar = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        items = soup.find_all("a", class_="ng-star-inserted") or soup.find_all("div", class_="row")
        
        for item in items:
            title = item.get_text(strip=True)
            link = item.get("href", "")
            
            if "personel" in title.lower() or "alım" in title.lower() or "kpss" in title.lower():
                if link and not link.startswith("http"):
                    link = f"https://www.ilan.gov.tr{link}"
                
                ilanlar.append({
                    "Kurum": "Resmi Kurum",
                    "Başlık": title,
                    "Tarih": "Güncel",
                    "Link": link,
                    "Kaynak": "ilan.gov.tr"
                })
    except Exception as e:
        print(f"ilan.gov.tr çekme hatası: {e}")
        
    return ilanlar

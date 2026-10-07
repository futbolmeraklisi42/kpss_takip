import requests
from bs4 import BeautifulSoup

def get_sbb_ilanlari():
    url = "https://kamuilan.sbb.gov.tr/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    ilanlar = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        
        cards = soup.find_all("div", class_="card") or soup.find_all("tr")
        
        for item in cards:
            title_elem = item.find("a") or item.find("h5")
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                if link and not link.startswith("http"):
                    link = f"https://kamuilan.sbb.gov.tr{link}"
                
                if len(title) > 10:
                    ilanlar.append({
                        "Kurum": "Kamu İlan (SBB)",
                        "Başlık": title,
                        "Tarih": "Güncel",
                        "Link": link,
                        "Kaynak": "SBB Kamu İlan"
                    })
    except Exception as e:
        print(f"SBB çekme hatası: {e}")
        
    return ilanlar

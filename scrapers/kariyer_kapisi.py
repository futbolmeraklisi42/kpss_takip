from playwright.sync_api import sync_playwright

def get_kariyer_kapisi_ilanlari():
    """Kariyer Kapısı üzerindeki kamu alım ilanlarını çeker."""
    url = "https://kariyerkapisi.cbiko.gov.tr/IseAlimIlanlari"
    ilanlar = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Sayfadaki ilan öğelerini çek
            cards = page.query_selector_all(".card") or page.query_selector_all(".job-item") or page.query_selector_all("tr")
            
            for card in cards:
                text = card.inner_text().strip()
                link_elem = card.query_selector("a")
                link = link_elem.get_attribute("href") if link_elem else url
                
                if link and not link.startswith("http"):
                    link = f"https://kariyerkapisi.cbiko.gov.tr{link}"
                
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                if lines:
                    title = lines[0]
                    if len(title) > 8:
                        ilanlar.append({
                            "Kurum": "Kariyer Kapısı (CBİKO)",
                            "Başlık": title,
                            "Tarih": "Güncel",
                            "Link": link,
                            "Kaynak": "Kariyer Kapısı"
                        })
            browser.close()
    except Exception as e:
        print(f"Kariyer Kapısı çekme hatası: {e}")
        
    return ilanlar

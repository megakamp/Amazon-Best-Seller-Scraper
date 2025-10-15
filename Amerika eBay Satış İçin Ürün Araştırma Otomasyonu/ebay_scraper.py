#!/usr/bin/env python3
"""
eBay Piyasa Araştırması Otomasyonu
Bu script eBay'den en çok satan ve satış potansiyeli yüksek ürünleri toplar.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import csv
from datetime import datetime
import logging
from urllib.parse import urljoin, quote
import re
from typing import List, Dict, Any

# ProductAnalyzer sınıfını import et
from product_analyzer import ProductAnalyzer

# Logging ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class EbayScraper:
    def __init__(self):
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # En çok satan kategoriler
        self.categories = [
            "Clothing, Shoes & Accessories",
            "Home & Garden", 
            "Jewelry & Watches",
            "Collectibles",
            "Health & Beauty",
            "Electronics",
            "Sporting Goods",
            "Toys & Hobbies",
            "Business & Industrial",
            "Motors"
        ]
        
        # Arama terimleri
        self.trending_keywords = [
            "trending", "hot selling", "best seller", "popular", "top rated",
            "most watched", "fast shipping", "new arrival", "limited edition"
        ]
        
        self.analyzer = ProductAnalyzer()
    
    def get_random_delay(self, min_delay=1, max_delay=3):
        """Rastgele bekleme süresi"""
        return random.uniform(min_delay, max_delay)
    
    def search_category_products(self, category, sort_by="BestMatch", limit=50):
        """Belirli bir kategoride ürün arama"""
        try:
            # URL oluştur
            base_url = "https://www.ebay.com/sch/i.html"
            params = {
                '_nkw': category,
                '_sacat': '0',
                '_sop': '12',  # En çok satanlar
                '_ipg': str(limit),
                '_from': 'R40',
                'LH_Sold': '1', # Satılan ürünler
                'LH_Complete': '1' # Tamamlanmış listelemeler
            }
            
            # İstek gönder
            response = self.session.get(base_url, params=params)
            response.raise_for_status()
            
            # HTML parse et
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Ürün listelerini bul
            items = soup.select('li.s-item:not(.s-item__pl-on-bottom)') # li etiketini kullan
            
            for item in items[:limit]:
                try:
                    product_data = self.extract_product_data(item)
                    if product_data:
                        product_data['search_keyword'] = category # Kategori bilgisini ekle
                        products.append(product_data)
                except Exception as e:
                    logger.warning(f"Ürün verisi çıkarılırken hata: {e}")
                    continue
            
            logger.info(f"{category} kategorisinde {len(products)} ürün bulundu")
            return products
            
        except Exception as e:
            logger.error(f"Kategori arama hatası ({category}): {e}")
            return []
    
    def extract_product_data(self, item_element):
        """Ürün verisini çıkar"""
        try:
            product = {}
            
            # Başlık
            title_elem = item_element.find('h3', {'class': 's-item__title'}) 
            if title_elem:
                product['title'] = title_elem.get_text(strip=True)
            else:
                product['title'] = 'N/A'
            
            # Fiyat
            price_elem = item_element.find('span', {'class': 's-item__price'})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                product['price'] = self.clean_price(price_text)
            else:
                product['price'] = 0.0
            
            # Link
            link_elem = item_element.find('a', {'class': 's-item__link'})
            if link_elem:
                product['url'] = link_elem.get('href')
            else:
                product['url'] = 'N/A'
            
            # Satıcı bilgisi
            seller_elem = item_element.find('span', {'class': 's-item__seller-info-text'})
            if seller_elem:
                product['seller'] = seller_elem.get_text(strip=True)
            else:
                product['seller'] = 'N/A'
            
            # Kargo bilgisi
            shipping_elem = item_element.find('span', {'class': 's-item__shipping'})
            if shipping_elem:
                product['shipping'] = shipping_elem.get_text(strip=True)
            else:
                product['shipping'] = 'N/A'
            
            # Satış sayısı (varsa)
            sold_elem = item_element.find('span', {'class': 's-item__hotness-count'}) or item_element.find('span', {'class': 's-item__quantity-sold'})
            if sold_elem:
                sold_text = sold_elem.get_text(strip=True)
                product['sold_count'] = self.extract_sold_count(sold_text)
            else:
                product['sold_count'] = 0
            
            # Görüntülenme/izlenme sayısı (varsa)
            watchers_elem = item_element.find('span', {'class': 's-item__watchers'})
            if watchers_elem:
                watchers_text = watchers_elem.get_text(strip=True)
                product['watchers'] = self.extract_watchers_count(watchers_text)
            else:
                product['watchers'] = 0
            
            # Resim URL'si
            img_elem = item_element.find('img', {'class': 's-item__image-img'})
            if img_elem:
                product['image_url'] = img_elem.get('src')
            else:
                product['image_url'] = 'N/A'
            
            # Timestamp
            product['scraped_at'] = datetime.now().isoformat()
            
            return product if product.get('title') != 'N/A' else None
            
        except Exception as e:
            logger.warning(f"Ürün verisi çıkarma hatası: {e}")
            return None
    
    def clean_price(self, price_text):
        """Fiyat metnini temizle"""
        try:
            # Sadece sayıları ve nokta/virgül karakterlerini al
            price_clean = re.sub(r'[^\d.,]', '', price_text)
            if price_clean:
                # Virgülü noktaya çevir ve float'a dönüştür
                return float(price_clean.replace(',', '.'))
            return 0.0 # Hata durumunda 0.0 döndür
        except:
            return 0.0 # Hata durumunda 0.0 döndür
    
    def extract_sold_count(self, sold_text):
        """Satış sayısını çıkar"""
        try:
            numbers = re.findall(r'\d+', sold_text)
            return int(numbers[0]) if numbers else 0
        except:
            return 0
    
    def extract_watchers_count(self, watchers_text):
        """İzleyici sayısını çıkar"""
        try:
            numbers = re.findall(r'\d+', watchers_text)
            return int(numbers[0]) if numbers else 0
        except:
            return 0
    
    def search_trending_products(self, keyword, limit=20):
        """Trend ürünleri ara"""
        try:
            base_url = "https://www.ebay.com/sch/i.html"
            params = {
                '_nkw': keyword,
                '_sacat': '0',
                '_sop': '12',  # En çok satanlar
                '_ipg': str(limit),
                '_from': 'R40',
                'LH_Sold': '1', # Satılan ürünler
                'LH_Complete': '1' # Tamamlanmış listelemeler
            }
            
            response = self.session.get(base_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            items = soup.select('li.s-item:not(.s-item__pl-on-bottom)')
            
            for item in items[:limit]:
                try:
                    product_data = self.extract_product_data(item)
                    if product_data:
                        product_data['search_keyword'] = keyword
                        products.append(product_data)
                except Exception as e:
                    continue
            
            logger.info(f"'{keyword}' için {len(products)} trend ürün bulundu")
            return products
            
        except Exception as e:
            logger.error(f"Trend ürün arama hatası ({keyword}): {e}")
            return []
    
    def run_market_research(self):
        """Tam piyasa araştırması çalıştır"""
        logger.info("eBay piyasa araştırması başlatılıyor...")
        
        all_products = []
        
        # Kategorilerde arama yap
        for category in self.categories:
            logger.info(f"Kategori araştırılıyor: {category}")
            products = self.search_category_products(category, limit=20)
            all_products.extend(products)
            
            # Bekleme süresi
            time.sleep(self.get_random_delay(2, 4))
        
        # Trend anahtar kelimelerle arama yap
        for keyword in self.trending_keywords:
            logger.info(f"Trend anahtar kelime araştırılıyor: {keyword}")
            products = self.search_trending_products(keyword, limit=15)
            all_products.extend(products)
            
            # Bekleme süresi
            time.sleep(self.get_random_delay(2, 4))
        
        # Ürünleri analiz et ve skorla
        analyzed_products = self.analyzer.analyze_products(all_products)
        
        # Kategorilere ayır
        categorized_products = self.analyzer.categorize_products(analyzed_products)
        
        # İçgörüler üret
        insights = self.analyzer.generate_insights(analyzed_products)
        
        logger.info(f"Toplam {len(analyzed_products)} ürün analiz edildi")
        
        # En çok satan ve yüksek potansiyelli ürünleri al
        # Burada 'top_selling_products' ve 'high_potential_products' listelerini doldurmak için
        # skorlama algoritmasından gelen 'high_potential' ve 'medium_potential' kategorilerini kullanıyorum.
        # Ayrıca, en çok satanlar için genel sıralamayı da dikkate alıyorum.
        
        top_selling = []
        high_potential = []

        # Tüm analiz edilmiş ürünleri skora göre sırala
        sorted_all_products = sorted(analyzed_products, key=lambda x: x.get('advanced_score', 0), reverse=True)

        # En çok satanlar (genel olarak en yüksek skorlular)
        top_selling = sorted_all_products[:10]

        # Yüksek potansiyelliler (belirli bir eşiğin üzerindeki ürünler)
        high_potential = [p for p in sorted_all_products if p.get('advanced_score', 0) >= 70][:10]

        return {
            'timestamp': datetime.now().isoformat(),
            'total_products_analyzed': len(analyzed_products),
            'top_selling_products': top_selling,
            'high_potential_products': high_potential,
            'insights': insights
        }
    
    def save_results(self, results, filename_prefix="ebay_market_research"):
        """Sonuçları kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON formatında kaydet
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # CSV formatında kaydet (top_selling_products)
        csv_filename_top_selling = f"{filename_prefix}_top_selling_{timestamp}.csv"
        with open(csv_filename_top_selling, 'w', newline='', encoding='utf-8') as f:
            if results['top_selling_products']:
                fieldnames = results['top_selling_products'][0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results['top_selling_products'])
        
        # CSV formatında kaydet (high_potential_products)
        csv_filename_high_potential = f"{filename_prefix}_high_potential_{timestamp}.csv"
        with open(csv_filename_high_potential, 'w', newline='', encoding='utf-8') as f:
            if results['high_potential_products']:
                fieldnames = results['high_potential_products'][0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results['high_potential_products'])
        
        logger.info(f"Sonuçlar kaydedildi: {json_filename}, {csv_filename_top_selling}, {csv_filename_high_potential}")
        return json_filename, csv_filename_top_selling, csv_filename_high_potential

def main():
    """Ana fonksiyon"""
    scraper = EbayScraper()
    
    try:
        # Piyasa araştırması çalıştır
        results = scraper.run_market_research()
        
        # Sonuçları kaydet
        json_file, csv_top_selling_file, csv_high_potential_file = scraper.save_results(results)
        
        # Özet rapor yazdır
        print("\n" + "="*50)
        print("eBay PIYASA ARAŞTIRMASI RAPORU")
        print("="*50)
        print(f"Tarih: {results['timestamp']}")
        print(f"Analiz edilen toplam ürün sayısı: {results['total_products_analyzed']}")
        print(f"En çok satan ürün sayısı: {len(results['top_selling_products'])}")
        print(f"Yüksek potansiyelli ürün sayısı: {len(results['high_potential_products'])}")
        
        print("\nEN ÇOK SATAN İLK 10 ÜRÜN:")
        print("-" * 30)
        for i, product in enumerate(results['top_selling_products'], 1):
            print(f"{i}. {product.get('title', 'N/A')[:60]}...")
            print(f"   Fiyat: ${product.get('price', 'N/A')}")
            print(f"   Skor: {product.get('advanced_score', 'N/A')}")
            print(f"   Satış: {product.get('sold_count', 'N/A')}")
            print()
            
        print("\nYÜKSEK POTANSİYELLİ İLK 10 ÜRÜN:")
        print("-" * 30)
        for i, product in enumerate(results['high_potential_products'], 1):
            print(f"{i}. {product.get('title', 'N/A')[:60]}...")
            print(f"   Fiyat: ${product.get('price', 'N/A')}")
            print(f"   Skor: {product.get('advanced_score', 'N/A')}")
            print(f"   Satış: {product.get('sold_count', 'N/A')}")
            print()
        
        print(f"\nDetaylı sonuçlar: {json_file}")
        print(f"CSV raporu (En Çok Satanlar): {csv_top_selling_file}")
        print(f"CSV raporu (Yüksek Potansiyelliler): {csv_high_potential_file}")
        
    except Exception as e:
        logger.error(f"Ana fonksiyon hatası: {e}")
        raise

if __name__ == "__main__":
    main()


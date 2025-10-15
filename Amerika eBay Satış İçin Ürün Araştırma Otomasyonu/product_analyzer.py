#!/usr/bin/env python3
"""
Ürün Analizi ve Skorlama Algoritması
Bu modül eBay ürünlerini analiz eder ve satış potansiyelini skorlar.
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ProductAnalyzer:
    def __init__(self):
        """Ürün analizörünü başlat"""
        self.category_weights = {
            "Clothing, Shoes & Accessories": 1.2,
            "Home & Garden": 1.1,
            "Health & Beauty": 1.3,
            "Electronics": 1.0,
            "Jewelry & Watches": 0.9,
            "Collectibles": 0.8,
            "Sporting Goods": 1.0,
            "Toys & Hobbies": 1.1,
            "Business & Industrial": 0.7,
            "Motors": 0.6
        }
        
        # Trend anahtar kelimeleri ve ağırlıkları
        self.trend_keywords = {
            "trending": 1.5,
            "hot selling": 1.4,
            "best seller": 1.3,
            "popular": 1.2,
            "top rated": 1.1,
            "most watched": 1.0,
            "fast shipping": 0.8,
            "new arrival": 1.0,
            "limited edition": 1.2
        }
        
        # Fiyat aralığı skorları
        self.price_ranges = [
            (0, 10, 0.5),      # Çok düşük fiyat
            (10, 25, 1.0),     # Düşük fiyat
            (25, 50, 1.3),     # Orta-düşük fiyat
            (50, 100, 1.5),    # Orta fiyat (en iyi)
            (100, 250, 1.2),   # Orta-yüksek fiyat
            (250, 500, 1.0),   # Yüksek fiyat
            (500, 1000, 0.8),  # Çok yüksek fiyat
            (1000, float('inf'), 0.5)  # Lüks fiyat
        ]
    
    def calculate_advanced_score(self, product: Dict[str, Any]) -> float:
        """Gelişmiş skorlama algoritması"""
        score = 0.0
        
        # 1. Fiyat skoru (30% ağırlık)
        price_score = self._calculate_price_score(product.get('price', 0))
        score += price_score * 0.30
        
        # 2. Satış performansı skoru (25% ağırlık)
        sales_score = self._calculate_sales_score(product.get('sold_count', 0))
        score += sales_score * 0.25
        
        # 3. İlgi skoru (15% ağırlık)
        interest_score = self._calculate_interest_score(product.get('watchers', 0))
        score += interest_score * 0.15
        
        # 4. Kategori skoru (10% ağırlık)
        category_score = self._calculate_category_score(product.get('search_keyword', ''))
        score += category_score * 0.10
        
        # 5. Trend skoru (10% ağırlık)
        trend_score = self._calculate_trend_score(product.get('title', ''), product.get('search_keyword', ''))
        score += trend_score * 0.10
        
        # 6. Kargo skoru (5% ağırlık)
        shipping_score = self._calculate_shipping_score(product.get('shipping', ''))
        score += shipping_score * 0.05
        
        # 7. Satıcı güvenilirlik skoru (5% ağırlık)
        seller_score = self._calculate_seller_score(product.get('seller', ''))
        score += seller_score * 0.05
        
        return round(score, 2)
    
    def _calculate_price_score(self, price: float) -> float:
        """Fiyat bazlı skor hesaplama"""
        if price <= 0:
            return 0.0
        
        for min_price, max_price, multiplier in self.price_ranges:
            if min_price <= price < max_price:
                return 100 * multiplier
        
        return 50  # Varsayılan skor
    
    def _calculate_sales_score(self, sold_count: int) -> float:
        """Satış sayısı bazlı skor hesaplama"""
        if sold_count <= 0:
            return 0
        elif sold_count >= 1000:
            return 100
        elif sold_count >= 500:
            return 90
        elif sold_count >= 100:
            return 80
        elif sold_count >= 50:
            return 70
        elif sold_count >= 20:
            return 60
        elif sold_count >= 10:
            return 50
        elif sold_count >= 5:
            return 40
        else:
            return 30
    
    def _calculate_interest_score(self, watchers: int) -> float:
        """İzleyici sayısı bazlı skor hesaplama"""
        if watchers <= 0:
            return 0
        elif watchers >= 100:
            return 100
        elif watchers >= 50:
            return 80
        elif watchers >= 20:
            return 60
        elif watchers >= 10:
            return 40
        elif watchers >= 5:
            return 30
        else:
            return 20
    
    def _calculate_category_score(self, search_keyword: str) -> float:
        """Kategori bazlı skor hesaplama"""
        for category, weight in self.category_weights.items():
            if category.lower() in search_keyword.lower():
                return 100 * weight
        return 50  # Varsayılan skor
    
    def _calculate_trend_score(self, title: str, search_keyword: str) -> float:
        """Trend anahtar kelimesi bazlı skor hesaplama"""
        title_lower = title.lower()
        keyword_lower = search_keyword.lower()
        
        max_score = 0
        for keyword, weight in self.trend_keywords.items():
            if keyword in title_lower or keyword in keyword_lower:
                score = 100 * weight
                max_score = max(max_score, score)
        
        return max_score if max_score > 0 else 50
    
    def _calculate_shipping_score(self, shipping: str) -> float:
        """Kargo bazlı skor hesaplama"""
        shipping_lower = shipping.lower()
        
        if 'free' in shipping_lower:
            return 100
        elif 'fast' in shipping_lower or 'express' in shipping_lower:
            return 80
        elif 'standard' in shipping_lower:
            return 60
        else:
            return 40
    
    def _calculate_seller_score(self, seller: str) -> float:
        """Satıcı güvenilirlik skoru hesaplama"""
        if not seller:
            return 50
        
        # Pozitif feedback yüzdesi çıkarma
        feedback_match = re.search(r'(\d+(?:\.\d+)?)%\s+positive', seller.lower())
        if feedback_match:
            feedback_percent = float(feedback_match.group(1))
            if feedback_percent >= 99:
                return 100
            elif feedback_percent >= 95:
                return 80
            elif feedback_percent >= 90:
                return 60
            elif feedback_percent >= 85:
                return 40
            else:
                return 20
        
        return 50  # Varsayılan skor
    
    def analyze_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ürün listesini analiz et ve skorla"""
        analyzed_products = []
        
        for product in products:
            # Gelişmiş skor hesapla
            advanced_score = self.calculate_advanced_score(product)
            
            # Ürün kopyasını oluştur ve skoru ekle
            analyzed_product = product.copy()
            analyzed_product['advanced_score'] = advanced_score
            analyzed_product['analysis_timestamp'] = datetime.now().isoformat()
            
            analyzed_products.append(analyzed_product)
        
        # Skorlara göre sırala
        analyzed_products.sort(key=lambda x: x.get('advanced_score', 0), reverse=True)
        
        return analyzed_products
    
    def categorize_products(self, products: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Ürünleri kategorilere ayır"""
        categories = {
            'high_potential': [],      # Skor >= 80
            'medium_potential': [],    # Skor 60-79
            'low_potential': [],       # Skor 40-59
            'poor_potential': []       # Skor < 40
        }
        
        for product in products:
            score = product.get('advanced_score', 0)
            
            if score >= 80:
                categories['high_potential'].append(product)
            elif score >= 60:
                categories['medium_potential'].append(product)
            elif score >= 40:
                categories['low_potential'].append(product)
            else:
                categories['poor_potential'].append(product)
        
        return categories
    
    def generate_insights(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ürün analizi için içgörüler üret"""
        if not products:
            return {}
        
        df = pd.DataFrame(products)
        
        insights = {
            'total_products': len(products),
            'average_score': df['advanced_score'].mean() if 'advanced_score' in df.columns else 0,
            'score_distribution': {},
            'price_analysis': {},
            'category_performance': {},
            'top_trends': []
        }
        
        # Skor dağılımı
        if 'advanced_score' in df.columns:
            insights['score_distribution'] = {
                'high_potential': len(df[df['advanced_score'] >= 80]),
                'medium_potential': len(df[(df['advanced_score'] >= 60) & (df['advanced_score'] < 80)]),
                'low_potential': len(df[(df['advanced_score'] >= 40) & (df['advanced_score'] < 60)]),
                'poor_potential': len(df[df['advanced_score'] < 40])
            }
        
        # Fiyat analizi
        if 'price' in df.columns:
            price_data = df['price'].dropna()
            if len(price_data) > 0:
                insights['price_analysis'] = {
                    'average_price': float(price_data.mean()),
                    'median_price': float(price_data.median()),
                    'min_price': float(price_data.min()),
                    'max_price': float(price_data.max()),
                    'price_ranges': self._analyze_price_ranges(price_data)
                }
        
        # Kategori performansı
        if 'search_keyword' in df.columns:
            category_scores = df.groupby('search_keyword')['advanced_score'].mean().to_dict()
            insights['category_performance'] = {k: float(v) for k, v in category_scores.items()}
        
        # En iyi trendler
        if 'title' in df.columns:
            insights['top_trends'] = self._extract_trending_keywords(df['title'].tolist())
        
        return insights
    
    def _analyze_price_ranges(self, prices: pd.Series) -> Dict[str, int]:
        """Fiyat aralığı analizi"""
        ranges = {
            '$0-$25': 0,
            '$25-$50': 0,
            '$50-$100': 0,
            '$100-$250': 0,
            '$250-$500': 0,
            '$500+': 0
        }
        
        for price in prices:
            if price < 25:
                ranges['$0-$25'] += 1
            elif price < 50:
                ranges['$25-$50'] += 1
            elif price < 100:
                ranges['$50-$100'] += 1
            elif price < 250:
                ranges['$100-$250'] += 1
            elif price < 500:
                ranges['$250-$500'] += 1
            else:
                ranges['$500+'] += 1
        
        return ranges
    
    def _extract_trending_keywords(self, titles: List[str]) -> List[Dict[str, Any]]:
        """Başlıklardan trend anahtar kelimeleri çıkar"""
        word_counts = {}
        
        # Yaygın kelimeleri filtrele
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        
        for title in titles:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
            for word in words:
                if word not in stop_words:
                    word_counts[word] = word_counts.get(word, 0) + 1
        
        # En çok kullanılan 10 kelimeyi al
        trending = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [{'keyword': word, 'frequency': count} for word, count in trending]

def main():
    """Test fonksiyonu"""
    # Test verisi
    test_products = [
        {
            'title': 'Best Selling iPhone Case',
            'price': 25.99,
            'sold_count': 150,
            'watchers': 25,
            'shipping': 'Free shipping',
            'seller': 'seller123 99.5% positive (1.2K)',
            'search_keyword': 'Electronics'
        },
        {
            'title': 'Trending Fashion T-Shirt',
            'price': 15.50,
            'sold_count': 75,
            'watchers': 12,
            'shipping': 'Standard shipping',
            'seller': 'fashionstore 98% positive (500)',
            'search_keyword': 'Clothing, Shoes & Accessories'
        }
    ]
    
    analyzer = ProductAnalyzer()
    
    # Ürünleri analiz et
    analyzed = analyzer.analyze_products(test_products)
    
    # Kategorilere ayır
    categories = analyzer.categorize_products(analyzed)
    
    # İçgörüler üret
    insights = analyzer.generate_insights(analyzed)
    
    print("Analiz Sonuçları:")
    print(json.dumps(insights, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()


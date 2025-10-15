# eBay Piyasa Araştırması Otomasyonu

Bu proje, eBay Amerika pazarı için otomatik piyasa araştırması yaparak en çok satan ve satış potansiyeli yüksek ürünleri tespit etmek üzere tasarlanmıştır.

## Özellikler

- Belirlenen kategorilerde ve trend anahtar kelimelerde ürün arama.
- Ürün verilerini (başlık, fiyat, URL, satıcı, satış sayısı vb.) toplama.
- Toplanan ürünleri analiz etme ve potansiyel skorları atama.
- En çok satan ve yüksek potansiyelli ilk 10 ürünü listeleme.
- Sonuçları JSON ve CSV formatlarında kaydetme.

## Dosya Yapısı

- `ebay_scraper.py`: eBay'den veri çeken ve ürünleri analiz eden ana script.
- `product_analyzer.py`: Ürün analizi ve skorlama mantığını içeren modül.
- `README.md`: Bu proje hakkında bilgi.

## Kullanım

`ebay_scraper.py` scriptini çalıştırarak piyasa araştırmasını başlatabilirsiniz:

```bash
python3.11 ebay_scraper.py
```

Script çalıştıktan sonra, aşağıdaki dosyalar oluşturulacaktır:

- `ebay_market_research_YYYYMMDD_HHMMSS.json`: Tüm toplanan ve analiz edilen ürün verilerini içeren JSON dosyası.
- `ebay_market_research_top_selling_YYYYMMDD_HHMMSS.csv`: En çok satan ürünlerin listesini içeren CSV dosyası.
- `ebay_market_research_high_potential_YYYYMMDD_HHMMSS.csv`: Yüksek potansiyelli ürünlerin listesini içeren CSV dosyası.

Konsolda ayrıca bir özet rapor görüntülenecektir.

## Rapor Çıktısı Örneği

```
==================================================
eBay PIYASA ARAŞTIRMASI RAPORU
==================================================
Tarih: [Tarih ve Saat]
Analiz edilen toplam ürün sayısı: [Sayı]
En çok satan ürün sayısı: [Sayı]
Yüksek potansiyelli ürün sayısı: [Sayı]

EN ÇOK SATAN İLK 10 ÜRÜN:
------------------------------
1. [Ürün Başlığı]...
   Fiyat: $[Fiyat]
   Skor: [Skor]
   Satış: [Satış Sayısı]

...

YÜKSEK POTANSİYELLİ İLK 10 ÜRÜN:
------------------------------
1. [Ürün Başlığı]...
   Fiyat: $[Fiyat]
   Skor: [Skor]
   Satış: [Satış Sayısı]

...

Detaylı sonuçlar: [JSON Dosya Adı]
CSV raporu (En Çok Satanlar): [CSV Dosya Adı]
CSV raporu (Yüksek Potansiyelliler): [CSV Dosya Adı]
```

## Sonraki Adımlar

Bu raporlar, eBay'de satış yaparken hangi ürünlere odaklanmanız gerektiği konusunda size değerli bilgiler sağlayacaktır. Otomasyonun günde iki kez çalışacak şekilde zamanlanması için sonraki adımlar planlanacaktır.



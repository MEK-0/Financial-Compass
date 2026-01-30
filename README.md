# 🏗️ Görev Dağılımı ve İş Paketleri
## 📦 Paket 1: Enterprise Backend 

* Teknoloji: Java 17, Spring Boot 3.x, PostgreSQL, Spring Cloud OpenFeign.

* Veri Yönetimi: User ve Transaction tablolarının tasarlanması; harcamaların kategorize edilmesi.

* Orkestrasyon: AI servisine analiz talebi göndermek için FeignClient entegrasyonu.

* Trigger Mekanizması: Kullanıcı sisteme girdiğinde veya periyodik olarak AI analizini tetikleyen servislerin yazılması.

* API: Mobil arayüz (veya frontend) için analiz sonuçlarını dönen endpoint'lerin (GET /status) hazırlanması.

## 🤖 Paket 2: Multi-Agent AI Engine 

* Teknoloji: Python 3.9+, FastAPI, LangGraph/LangChain, Pandas.

* Ajan 1 (Accountant): Gelen harcama listesinden düzenli giderleri (kira, fatura) bulup gelecek ayın yükümlülüğünü tahmin eder.

* Ajan 2 (Detective): MCC kodları üzerinden mükerrer abonelikleri ve fiyat artışlarını (Price Hike) tespit eder.

* Ajan 3 (Reasoner/Advisor): Diğer ajanların verilerini birleştirerek Safe_to_Spend (Serbest Bakiye) hesaplar ve aksiyon önerileri üretir.

* API: Spring Boot'tan gelen JSON verisini karşılayan yüksek performanslı bir FastAPI endpoint'i.
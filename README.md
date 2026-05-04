# CampusPulse
### **Anomali Tespiti ve 3D Modelleme Tabanlı Kampüs Enerji Verimliliği ve Yönetim Platformu**

**CampusPulse**, üniversite kampüslerindeki "hayalet yükleri" ve enerji israfını ortadan kaldırmak için geliştirilmiş, **Yapay Zeka** ve **3D Modelleme** tabanlı bir enerji yönetim ekosistemidir.

> **🏆 Hackathon Başarısı:** Bu proje, 30 takımın katıldığı hackathon kapsamında **2.lik Ödülü** kazanmıştır.

---

## 📸 Uygulama Arayüzü

| 3D Dijital İkiz Görünümü | Anomali Analiz Paneli |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/25c96f3b-b9fa-4146-a774-1d6cee2d5cd1" width="100%"> | <img src="https://github.com/user-attachments/assets/32994731-a84f-466c-9892-da8c0a02dee5" width="100%"> |
| *Three.js ile hazırlanan interaktif kampüs haritası.* | *Tespit edilen israfların finansal ve ekolojik dökümü[cite: 1].* |
| **Oda Durum Takibi** | **Detaylı Raporlar ve Analiz** |
| <img src="<img width="1600" height="757" alt="3d3" src="https://github.com/user-attachments/assets/8bf2c099-0cdf-40aa-ad64-14b3508ae0bd" />
" width="100%"> | <img src="<img width="1600" height="757" alt="3d4" src="https://github.com/user-attachments/assets/a17a123c-31f4-4060-8d56-d0364184bea3" />
" width="100%"> |
| *Odaların anlık doluluk ve enerji tüketim verileri[cite: 1].* | *Periyodik enerji verimliliği ve tasarruf raporları[cite: 1].* |

## Problemin Tanımı
Ortalama bir kampüs yılda milyonlarca kWh enerji tüketmektedir; ancak asıl sorun sistemlerin "kör" olmasıdır. 
*   Binaların anlık doluluk oranları izlenememektedir.
*   Boş amfiler ve laboratuvarlar 7/24 enerji tüketmeye devam etmektedir.
*   Yalnızca ana kampüs bütçesinde yıllık yaklaşık **16.7 Milyon TL** tutarında bir fatura yükü oluşmaktadır.

---

## CampusPulse Çözümü
CampusPulse, bu finansal yükü dijital bir denetim mekanizmasına dönüştürür:
*   **Yapay Zeka Denetim Katmanı:** Enerji tüketimini ders programlarıyla senkronize analiz eden hibrit bir yapı sunar.
*   **Isolation Forest Algoritması:** Veri setindeki gizli enerji israflarını ve uç değerleri milisaniyeler içinde teşhis eder[cite: 1].
*   **3D Dijital İkiz:** Tespit edilen anomalileri doğrudan Three.js tabanlı arayüz üzerinde "Nokta Atışı Müdahale Planı" olarak görselleştirir[cite: 1].

---

## Teknik Mimari ve Akış Şeması
```mermaid
graph LR
  A[IoT & Mock Veri] --> B[Yapay Zeka Motoru]
  B --> C[Backend & API]
  C --> D[3D Dijital İkiz]

Drive Linki: https://drive.google.com/drive/folders/10g2qQrcajHxdFh7CzZzixgROO4KasuMx?usp=sharing

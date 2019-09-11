# Mackolik (TR)
İstenilen tarihe/tarihlere göre futbol maçlarının bilgilerini ve **iddaa** oranlarını mackolik.com'dan alıp csv dosyasına yazar.

**mackolik.csv** dosyasında, 01/01/2013 ile 16/08/2019 tarihleri arasında oynanmış iddaa oranına sahip tüm futbol maçları vardır. Toplam 148120 maç.

**Canlı Bahis sistemine geçildiği için Iddaa, maç kodlarını ve yapılarını değiştirmiştir. Bu yüzden, şuan program sadece Canlı Bahis sistemi öncesi tarihler için çalışmaktadır. İlerleyen zamanlarda program yeni sisteme entegre edilecektir.**

# Mackolik (EN)
Gets the betting odds of football matches based on Turkey's Official Betting Game (IDDAA).

**mackolik.csv** have 148120 matches which played between 01/01/2013 and 16/08/2019

# Nasıl Çalışır? (TR)
  **Örnek gün 01/01/2018' e göre anlatım:**
  * 01/01/2018 tarihinde bahis oranı açılmış tüm futbol maçlarının ID'lerini ve tarih, saat, lig gibi maç detaylarını alır.
    ```
      http://goapi.mackolik.com/livedata?date=01/01/2018
    ```
  * Alınmış olan her id'e giderek maç oranları alır.
    ```
      arsiv.mackolik.com/Match/Default.aspx?id=2816096
    ```
   * Her maçın oranlarını .csv dosyasının yapısına uyarlar ve yazar.

  **Terminal görüntüsü**
  
   ![terminal görünütüsü](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/console.jpg)

# CSV Format
```
Date, Season, Time, Code, League, Home, Away, HT, FT, MS1, MSX, MS2,
H, H1, HX, H2, H, IY1.5A, IY1.5U, 1.5A, 1.5U, 2.5A, 2.5U, 3.5A, 3.5U,
KGV, KGY, IY1, IY0, IY2, 1-X, 1-2, X-2, TG01, TG23, TG46, TG7,
1/1, 1/X, 1/2, X/1, X/X, X/2, 2/1, 2/X, 2/2
```

# Requirements (tested versions)
**pip install -r requirements.txt**
  ```
Python 3.6.5
Requests 2.20.0
Beautifulsoup4 4.6.0
  ```
  
# Bazı İstatistikler
Bu istatistikler 01/01/2013 ile 27/12/2018 tarihleri arasında oynanan maçlardan çıkarılmıştır.

    MS1 tablosu için; 
        'Maç Sonucu 1' bahisi tutan/kazanan maçların yaklaşık olarak 3500'ü ms1 - 1.85 oranına sahipmiş.

**Bahis veya yatırım tavsiyesi değildir.**

![ms1](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/ms1.png)

![ms0](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/ms0.png)

![ms2](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/ms2.png)

![iy1](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/iy1.png)

![iy0](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/iy0.png)

![iy2](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/iy2.png)

![25a](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/2,5a.png)

![25u](https://raw.githubusercontent.com/boardsofcanada/mackolik/master/images/2,5u.png)

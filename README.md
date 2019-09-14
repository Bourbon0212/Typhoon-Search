# Typhoon-Search: 西北太平洋颱風路徑比對
## 分析方法
本研究颱風路徑比對之演算法主要基於「**最短距離**」、「**時間加權**」與「**基數排序（radix sort）**」。首先，(1) 使用者從各國氣象單位匯入颱風點資料，或由 (2) 使用者輸入欲搜尋的颱風路徑點與其相對應的搜尋半徑，若歷史颱風路徑點與使用者輸入點之間的最短距離小於搜尋半徑，則賦予時間加權。其次，針對每一筆歷史颱風路徑，總合計算加權總分。最後，依總分、時間加權、通過點個數與時間進行基數排序，統整出路徑相似程度較高的歷史颱風資料。

## 使用語言與套件
* Python 3.7.0    
* flask 1.0.3
* gunicorn 19.9.0 (Optional for local test, Must for online)
* honcho 1.0.1 (Optional)
* BeautifulSoup

## 程式碼    
### app.py    
* `@app.route('/')`: 使用者介面首頁   
* `@app.route('/typhoon_forecast')`: 從各國氣象局取得現有(或最後一筆)颱風路徑資料    
* `@app.route("/route_sorting")`: 歷史颱風路徑相似度分析排序結果     
* `@app.route("/typhoon_history")`: 及時擷取 JMA 歷史颱風路徑資料   

### data_process.py   
* 自日本気象庁公開 API 接收 1951 年至今，所有気象庁管轄範圍內熱帶氣旋之資料    
* 每一筆颱風資料皆具備 header line 與 data lines
  + header line: 該颱風的國際編號與英文名稱等
  + data lines: 每六小時，該颱風所在位置的經緯度與風速資料   
* 每一行資料不同位置皆有獨特意義，透過程式逐行擷取、進行字串處理，將其整理成 JSON 格式
* 經統整後，總計約有 1,700 筆熱帶氣旋資料，並包含約 65,000 筆點資料

### get_function.py   
* **history_point_data(history)**:    
  + 將 data_process.py 的結果整理成:  `颱風編號:[(經緯1), (經緯2), ...]` 的格式
* **getDistance(latA, lonA, latB, lonB)**:    
  + 輸入任意兩點之經緯度，回傳兩點之間距離（公尺）   
* **get_yymm(history)**:    
  + 將 data_process.py 的結果取出每筆颱風資料最後一筆點資料的時間，作為颱風發生時間    
  + `颱風編號:[年, 月]` 的格式   
* **compute_weight(k)**:
  + 尋找對應不同使用者輸入點個數（M），能使時間加權最大化的時間權重臨界值（w-hat）    
  
### radix_sort.py   
* **min_distance(history, point_data, U)**:
  + 找尋每筆（i）颱風資料與使用者輸入之第 k 個點之間最短距離: `dik = min(Dijk)`   
* **weight_of_all(history, point_data, U)**:    
  + 計算落於搜尋半徑內的每筆歷史颱風路徑排序總分    
    + `<Route Score> sigma(k = 1, M) [1 + kw, k, 1] | for all Dik < radius`   
  + 並從 `get_yymm()` 找到颱風發生時間   
    + `<Time  Score> [year, month]`   
* **radix_sort(history, point_data, U)**:   
  + 取得 `weight_of_all()` 的分數
  + 再依照 `總分`、`時間加權`、`通過點個數`、`與現在月分之差`、`與現在年份之差`排序

### module: center    
#### parser.py
* **parse_forecast(text)**: 
  + Typhoon2000 網站爬蟲：取得每個時間點各個氣象單位的颱風點資料
#### api.py
* **get_typhoons()**:
  + 整理 `parser` 資料為所有颱風的 `['<en>', '<zh-tw>', '<year>', '<key>']`    
  + 回傳 List 越前面的颱風為越新的颱風
* **get_typhoon_track(key, member = "CWB")**:
  + 給定特定颱風的 key 與氣象單位，回傳該單位的颱風路徑點資料
  + 以 List 回傳該颱風資料: `(Lon, Lat), (Lont, Lat)...`
#### meta.py
* 臺灣 CWB 資料各歷史颱風連結資料庫

DormFlowAlert
----
快速的宿舍網路總是讓人一用上癮，但是每天8GB的流量限制實在是讓人無奈，尤其是一旦超流就得被斷線，更是讓人生氣又無奈，所以本程式結合[csie.io的Line通知功能](https://csie.io/linefaq)，定期檢查您宿網使用的流量，並且在使用流量到達50%、70%、90%以及100%時，自動發出Line通知至您的裝置，讓您可以預先做出處置（如：遠端回去關機或是打電話給室友拔線等等），省去被斷線的痛苦經驗！使用本程式需要符合下列條件：

- 你必須是[csie.io](https://csie.io)的使用者
- 你住在[中正大學](http://www.ccu.edu.tw/)學生宿舍

安裝說明
----------
本程式使用Python的Requests library，經過實測可以直接在系上`linux.cs`以及`mcore8.cs`主機上面執行，如果您要在自己的機器上運行，請先執行`pip install requests`。

步驟如下：

- 登入系上`linux.cs`或`mcore8.cs`主機
- git clone https://github.com/clyang/DormFlowAlert
- 編輯檔案： `cd DormFlowAlert && vim DormFlowAlert.py`
  - 將`MYIP`改為您宿網的IP
  - 將`LINE_TOKEN`改為您的專屬token，（[您可在此取得](https://csie.io/linefaq)）
  - 存檔
- 最後設定每三分鐘檢查一次，使用下列指令`crontab -e`，在檔案最後新增下列這行
  - `*/3 * * * * ~/DormFlowAlert/DormFlowAlert.py >> ~/DormFlowAlert/flow.log`
  - 存檔
- 使用`crontab -l`檢查是否設定成功
- 搞定收工，祝您永遠不會收到超流的通知，[csie.io](https://csie.io)關心您

有圖有真相
----------
![alt_tag](https://i.imgur.com/SEUw67i.png)


# TOC Project 2020

共有9個state請參照show-fsm.png
State介紹
	user: 顯示出第一頁的功能選單
	state1: 告訴你台鐵火車的訂票網址
	state2: 告訴你高鐵的訂票網址
	state3-state4: 利用網路爬蟲去科技紫微網上將今天各星座的運勢抓下來並告訴你
	state5: 顯示出第二頁的功能選單
	state6: print出此linebot的FSM圖
	state7-state8: 利用網路爬蟲去weather.com上將今天各縣市的天氣預報抓下來並告訴你
操作流程:
	一開始先傳送任意訊息給小助手-KU，他會回傳一個功能選單給使用者，使用者再依所需的功能去點選或是打字輸入即可。
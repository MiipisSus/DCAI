# DCAI
> :point_right:  **IMPORTANT**:point_left:
> 
> 由於當時撰寫該版本時功力不足，架構十分凌亂，因此已經在著手重構 DCAI_v2，敬請期待！

DCAI 是一款針對 Character ai 的多項聊天功能，整理並串接到 Discord 機器人上的專案。
目前僅有繁體中文(zh-tw)的版本。

不包含 GUI 的版本在[這裡](https://github.com/MiipisSus/DCAI-Run-only-.ver)。
## How to set-up
> 請先在 [Discord.dev](https://ptb.discord.com/developers/applications) 創建一個 Discord bot，並記下其 token
1. 執行 bot.py
2. 在管理機器人的視窗中，填寫必須資訊並儲存

![圖片](https://github.com/user-attachments/assets/be1f1fee-ea9b-40a4-8fbe-626696c56c32)

## How to use
1. 將 Discord Bot 邀入伺服器
2. @ Discord Bot 並輸入聊天內容，它就會回覆你了！

![圖片](https://github.com/user-attachments/assets/67910aa8-e090-456f-b9df-e7718348285c)

## Feature
### 多人聊天室設計
同個頻道上的機器人，將會記錄所有與他對話的人的名稱，因此它能夠在 C-ai LLM model 的有限記憶中辨識所有人。
另外也可以使用 /改變暱稱 改變機器人對自己的稱呼。
### 機器人間可以互相聊天
當你創建的機器人為複數以上時，可以對一位 Bot 使用 /角色一對一聊天 ，並選擇另一名 Bot，讓他們在頻道進行對話！
除了一般的對話，還可以針對想要的情境撰寫故事設定。

![圖片](https://github.com/user-attachments/assets/0e2dd649-5168-45c8-ab3a-4442dd006913)

### 報時
針對單一伺服器，可以對一位 Bot 使用 /定時訊息啟用 ，設定單一頻道為「報時頻道」。
該機器人會在早上9 點以及晚上9 點時，在該頻道進行報時任務。

![圖片](https://github.com/user-attachments/assets/ee81473e-2c40-4d42-abdc-09db65765787)


### 歡迎新成員
針對單一伺服器，可以對一位 Bot 使用 /定時訊息啟用 ，設定單一頻道為「歡迎新成員頻道」。
當有新成員加入伺服器時，該機器人會給予新成員歡迎訊息

![圖片](https://github.com/user-attachments/assets/2ab33e13-6a9d-4962-9a37-b63d6f428f26)


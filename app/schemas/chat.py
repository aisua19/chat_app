# チャットアプリにおける送受信データ構造を定義する
# WebSocket通信で扱うJSONメッセージの妥当性や構造の明示に使用

from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    #サーバーに送信するメッセージ構造
    #必須項目は username と message のみ
    username: str
    message: str

class ChatMessageResponse(BaseModel):
    #サーバーがユーザーに返すレスポンス構造
    #IDと送信時刻を含む
    id: int
    username: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True  # ORMモデルからの自動変換を許可（SQLAlchemy用）
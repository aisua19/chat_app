#チャットアプリで使用するモデルを定義
#ORM機能でPythonクラスとDBテーブルを対応させる

from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.db.base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    message = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

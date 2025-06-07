#WebSocketリアルタイム通信を行うルーティング機能を定義
#APIRouterでチャット処理を分離し、接続、受信、保存、ブロードキャスト

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_session
from app.db.models import ChatMessage
from datetime import datetime
import json 

router = APIRouter()

#接続中のソケットをリストで保持
#ユーザーが切断時にリストから除外（リソース管理）
active_connections: List[WebSocket] = []


#新しい接続時にWebSocket受け入れ
#一時的な接続リストに追加（ブロードキャスト対象）
async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@router.websocket("/ws")
#WebSocketエンドポイント
#メッセージ受信後DBに保存しすべての接続にブロードキャスト
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    await connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            #フォーマットが正しくない場合は無視して待機
            try:
                parsed = json.loads(data)
                username = parsed["username"]
                message = parsed["message"]
            except (json.JSONDecodeError, KeyError):
                continue

            #メッセージ内容をDBに非同期で保存、コミット後の timestamp を取得
            new_msg = ChatMessage(username=username, message=message)
            session.add(new_msg)
            await session.commit()

            # [timestamp] username: message の形で全接続中クライアントへ送信
            timestamp = new_msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            await broadcast(f"[{timestamp}] {username}: {message}")
    except WebSocketDisconnect:
        disconnect(websocket)

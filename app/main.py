#起点となるファイル
#ルーティング・ログ初期化などの中心処理を記述

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router as chat_router
from app.core.logging_config import init_logging

#アプリ起動時にログ設定を読み込み、障害時の追跡を可能に
init_logging()

app = FastAPI()

#CORS設定（開発環境ではフロントエンド連携のため全許可）
#今は全オリジン許可だが、本番ではセキュリティのため制限予定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)

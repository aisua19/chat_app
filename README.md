# Chat App (FastAPI + WebSocket + MariaDB)
このアプリケーションは、インフラエンジニア志望として以下のような実運用を意識した構成で設計、構築しています。  
Dockerによるコンテナ化と環境依存の排除。  
MariaDB を用いたデータ永続化と構造的な設計。  
ログ出力設定（ローテーション含む） による運用監視基盤の整備。  
.envによる環境変数管理でセキュリティと可搬性の確保。  
AWSへの展開や運用監視（CloudWatch）も視野に入れた設計となっており、本番運用を想定したログ基盤やセキュリティ構成にも配慮しています。  
また、このアプリケーションは将来的なゲーム内チャット機能の実装を見据えたプロトタイプでもあり、FastAPIによる非同期WebSocket通信を通じてリアルタイムチャットを実現し、MariaDBに履歴を保存する構成となっています。  

## 使用ライブラリと選定理由  

ライブラリ理由  

**FastAPI** 軽量で高性能な非同期Webフレームワーク。自動APIドキュメント生成にも対応。  
**Uvicorn[standard]** 非同期対応サーバ。FastAPIとの親和性が高く、開発時にリロード等が便利。  
**SQLAlchemy** ORMによりDB構造とPythonコードの整合性を維持しやすい。  
**Aiomysql** MariaDBとの非同期接続をサポート。FastAPIとの整合性。  
**python-dotenv** .env　による設定管理で、環境に応じた切り替えが容易。  

##  起動方法（ローカル開発）  
　
bash  
cp .env.example .env  
docker-compose up --build  

## WebSocket通信仕様  

エンドポイント：`ws://localhost:8000/ws`  
送信形式（JSON）:  
json  
{
  "username": "your_name",  
  "message": "masseage"  
}  

## データベース構成（MariaDB）  

DB名：`chat_db`  
テーブル：`chat_messages`（履歴自動保存）  
接続情報は `.env` 管理  
　
## ログ出力  

出力先：`logs/app.log`  
出力レベル：`.env` で `DEBUG`, `INFO` 等を指定可能  
最大2MB、最大5世代でローテート保存  

## ディレクトリ構成  

app/  
├── main.py  
├── db/  
│   ├── models.py  
│   ├── session.py  
│   └── base.py  
├── schemas/  
│   └── chat.py  
├── routers/  
│   └── chat.py  
└── core/　　
    └── logging_setting.py  

import logging
from logging.handlers import RotatingFileHandler
import os

# .envからLOG_LEVELを取得して出力レベルを制御
#開発ならDEBUG、本番ならWARNING/ERROR に切り替える想定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def init_logging():
    logger = logging.getLogger("chat_logger")
    # 既に出力先があれば二重登録を防いでそのまま返す
    if logger.hasHandlers():
        return logger

    #logs/ が存在しない場合に備えて生成
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    #app.log に最大2MBでローテート、最大5世代分
    log_file = os.path.join(log_dir, "app.log")
    handler = RotatingFileHandler(log_file, maxBytes=2 * 1024 * 1024, backupCount=5)

    #日時、ログレベル、メッセージを標準化
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    #ロガー初期化
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    logger.addHandler(handler)
    logger.propagate = False

    # コンソールへの出力
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # CloudWatch 想定ログ出力は watchtower などのライブラリで出力先追加可能（未実装）
    return logger

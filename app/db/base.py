#基底クラス Base を定義するファイル
#モデルファイルが複数に分かれても、共通のBaseでテーブル定義が統一される構成

from sqlalchemy.orm import declarative_base

Base = declarative_base()

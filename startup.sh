#!/bin/bash
# 仮想環境を作成（または再利用）し、明示的に有効化する
python -m venv antenv
source antenv/bin/activate
# 依存パッケージを確実にインストールする
pip install -r requirements.txt
# 仮想環境内のPythonを使ってStreamlitを起動する
python -m streamlit run src/backend/main.py --server.port 8000 --server.address 0.0.0.0

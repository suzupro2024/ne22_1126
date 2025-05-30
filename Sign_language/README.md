# 手話認識システム（MediaPipe + LSTM）

このプロジェクトは、MediaPipeとLSTMモデルを用いて、日本語の基本的な挨拶手話（「おはようございます」「こんにちは」「こんばんは」）を認識するシステムです。

---

## プロジェクト構成

| ファイル名 | 説明 |
|------------|------|
| `main.py` | 動画（手話の学習用動画）から手のランドマークを抽出し、30フレーム単位でデータを保存します。このデータは学習データの生成に使用します。 |
| `learning.py` | main.pyで生成した手のランドマークデータをファイルから読み込み、学習用データセット（訓練/テスト）を作成します。 |
| `LSTM.py` | LSTMモデルを定義し、learning.pyで作成した学習用データセットを用いて、手話分類モデルを訓練します。|
| `real_time_interface.py` | 学習済みモデルを使ってWebカメラ映像からリアルタイムに手話を認識・表示（認識結果と確信度）します。 |

---

## ⚙️ 動作環境・必要なライブラリ

- Python 3.6
- TensorFlow
- OpenCV
- MediaPipe
- scikit-learn
- numpy

ライブラリのインストール（例）:

```bash
pip install tensorflow opencv-python mediapipe scikit-learn numpy
```

from learning import X_train, y_train, X_test, y_test # X_train, y_train, X_test, y_test をインポート
from main import SEQUENCE_LENGTH, LABELS  # SEQUENCE_LENGTH と LABELS をインポート

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# モデル定義
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(SEQUENCE_LENGTH, 63)),  # 63 は x, y, z の座標数
    LSTM(64),
    Dense(32, activation='relu'),
    Dense(len(LABELS), activation='softmax')  # 出力クラス数は LABELS の長さ
])

# モデルコンパイル
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# モデルの学習
model.fit(X_train, y_train, epochs=30, validation_data=(X_test, y_test))

# モデルの保存
model.save('sign_language_model.h5') 
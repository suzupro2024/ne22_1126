import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from main import SEQUENCE_LENGTH, LABELS

model = load_model('your_language_model')

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

cap = cv2.VideoCapture(0)

sequence = []
predictions = []
threshold = 0.3  # ← 信頼度の閾値

# 予測結果の安定性を見るための変数
last_label = ""
display_label = ""
display_counter = 0
repeat_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        landmarks = [coord for lm in hand.landmark for coord in (lm.x, lm.y, lm.z)]
        sequence.append(landmarks)

        if len(sequence) > SEQUENCE_LENGTH:
            sequence.pop(0)

        if len(sequence) == SEQUENCE_LENGTH:
            sequence_array = np.array(sequence).reshape(1, SEQUENCE_LENGTH, 63)
            prediction = model.predict(sequence_array)[0]
            max_prob = np.max(prediction)
            predicted_index = np.argmax(prediction)
            predicted_label = LABELS[predicted_index]

            if max_prob > threshold:
                if predicted_label == last_label:
                    repeat_count += 1
                else:
                    repeat_count = 0
                    last_label = predicted_label

                # 同じ予測が3回連続で出たときのみ表示
                if repeat_count == 3:
                    display_label = predicted_label
                    display_counter = 30  # 1秒程度表示
                    repeat_count = 0
                    sequence = []  # リセット（新しい動作を待つ）

    if display_counter > 0:
        cv2.putText(frame, f'Prediction: {display_label}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        display_counter -= 1

    cv2.imshow("Sign Language Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

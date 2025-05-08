import glob
import cv2
import mediapipe as mp
import os
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

DATA_DIR = 'landmark_data'
SOURCE_DIR = 'dat'

# ラベルとフォルダ名の対応
LABEL_MAP = {
    'GoodMorning': 'おはようございます',
    'GoodAfternoon': 'こんにちは',
    'GoodEvening': 'こんばんは'
}

LABELS = list(LABEL_MAP.keys())

SEQUENCE_LENGTH = 30
os.makedirs(DATA_DIR, exist_ok=True)

def process_video(video_path, label):
    """動画を処理してランドマークデータを保存する"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    sequence = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(image)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                landmarks = [coord for lm in hand.landmark for coord in (lm.x, lm.y, lm.z)]
                sequence.append(landmarks)

                if len(sequence) == SEQUENCE_LENGTH:
                    save_name = f"{label}_{os.path.basename(video_path)}_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.npy"
                    save_path = os.path.join(DATA_DIR, save_name)
                    try:
                        np.save(save_path, np.array(sequence))
                        print(f"Saved: {save_path}")
                    except Exception as e:
                        print(f"Error saving file {save_path}: {e}")
                    sequence = []
    finally:
        cap.release()

def main():
    """メイン処理"""
    for label, folder_name in LABEL_MAP.items():
        video_files = glob.glob(os.path.join(SOURCE_DIR, folder_name, '*.mp4'))
        for video_path in video_files:
            process_video(video_path, label)

if __name__ == '__main__':
    main()
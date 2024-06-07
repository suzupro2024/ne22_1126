# 必要なパッケージをインポート
import azure.cognitiveservices.speech as azure_speech
import time

# 音声認識を行うための関数を作成
def speech_recognize_continuous():
    # AzureのSpeech Serviceの資格情報を設定
    subscription_key = "21c98d58d2d348fba76ca7dcbd24746e"
    region = "japaneast"
    
    # 設定した資格情報を使ってSpeechConfigとAudioConfigを作成
    speech_config = azure_speech.SpeechConfig(subscription=subscription_key, region=region, speech_recognition_language="ja-JP")
    audio_config = azure_speech.AudioConfig(use_default_microphone=True)
    speech_recognizer = azure_speech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    # 音声認識の開始を表示(音声認識をコード内部で開始するよりも前に実行することで、表示的に音声認識開始と同時に表示できる)
    # 音声認識を内部的に開始してから表示すると、音声を受信中の文言が表示されるまでにラグが生じる
    print("音声を受信中...")  

    # 音声認識を開始
    speech_recognizer.start_continuous_recognition()

    # 音声認識の結果を表示
    speech_recognizer.recognized.connect(lambda evt: print(f"認識結果: {evt.result.text}"))
    # 音声認識がキャンセルされた時にエラーの詳細を表示
    speech_recognizer.canceled.connect(lambda evt: print(f"音声認識がキャンセルされました: {evt.reason} - {evt.error_details}"))

    # 音声認識の終了を検知するためのフラグ
    done = False

    # 音声認識が終了するまで待機
    while not done:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("処理を中断します。")
            speech_recognizer.stop_continuous_recognition()
            break         

# 音声認識を実行
if __name__ == "__main__":
    speech_recognize_continuous()
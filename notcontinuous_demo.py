import azure.cognitiveservices.speech as azure_speech

def speech_recognize_once():
    subscription_key = "21c98d58d2d348fba76ca7dcbd24746e"
    region = "japaneast"

    speech_config = azure_speech.SpeechConfig(subscription=subscription_key, region=region, speech_recognition_language="ja-JP")
    audio_config = azure_speech.AudioConfig(use_default_microphone=True)

    speech_recognizer = azure_speech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("音声を受信中...")
    result = speech_recognizer.recognize_once()

    if result.reason == azure_speech.ResultReason.RecognizedSpeech:
        print("認識結果: {}".format(result.text))
    elif result.reason == azure_speech.ResultReason.NoMatch:
        print("音声を認識できませんでした。")
    elif result.reason == azure_speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("音声認識がキャンセルされました。: {}".format(cancellation_details.reason))
        if cancellation_details.reason == azure_speech.CancellationReason.Error:
            print("エラー詳細: {}".format(cancellation_details.error_details))

# 関数呼び出し
speech_recognize_once()

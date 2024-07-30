import azure.cognitiveservices.speech as azure_speech
import yaml

# YAMLファイルからAzureの資格情報を読み込む関数
def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def speech_recognize_continuous():
    
    # YAMLファイルから資格情報を読み込む
    config = load_config("config.yml")
    subscription_key = config["azure"]["subscription_key"]
    region = config["azure"]["region"]

    speech_config = azure_speech.SpeechConfig(subscription=subscription_key, region=region, speech_recognition_language="ja-JP")
    speech_recognizer = azure_speech.SpeechRecognizer(speech_config=speech_config)

    print("音声を受信中...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == azure_speech.ResultReason.RecognizedSpeech:
        print("認識されました: {}".format(result.text))
    elif result.reason == azure_speech.ResultReason.NoMatch:
        print("音声が認識されませんでした")
    elif result.reason == azure_speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("音声認識がキャンセルされました: {}".format(cancellation_details.reason))
        if cancellation_details.reason == azure_speech.CancellationReason.Error:
            print("エラーの詳細: {}".format(cancellation_details.error_details))

if __name__ == "__main__":
    speech_recognize_continuous()

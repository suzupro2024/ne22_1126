#include <M5Stack.h>
#include <WiFi.h>
#include <WiFiUDP.h>
#include "efont.h"
#include "efontESP32.h"
#include "efontEnableJa.h"

// WiFi設定
const char* ssid = "TP-Link_IoT_B4F4";  // WiFiのSSIDを指定
const char* password = "46008213";  // WiFiのパスワードを指定

// サーバーとクライアントの設定
const char* serverAddress = "192.168.0.65";  // サーバーのアドレスを指定
const int serverPort = 10024;
const int clientPort = 10025;

WiFiUDP udp;
char buf[1024];
int textX = 350; // X座標
int textY = 145; // Y座標
int textsize = 6; // テキストサイズ
int scrollSpeed = 50; // スクロール速度（遅いほど速い）
bool textFinished = true; // テキストのスクロールが終了したかどうかを示すフラグ

void scrollText(char* text) {
  // 必要な部分のみクリア
  int textWidth = strlen(text) * textsize * 12; // テキストの幅を計算

  // 画面外に出たテキスト部分をクリア
  if (textX + textWidth < M5.Lcd.width()) {
    int clearWidth = min(15, M5.Lcd.width() - textX - textWidth);
    M5.Lcd.fillRect(textX + textWidth, textY, clearWidth, textsize * 24, TFT_BLACK);
  }

  printEfont(text, textX, textY, textsize); // 日本語表示

  // スクロールの更新
  textX -= 15; // テキストを左にスクロール
  delay(scrollSpeed);

  // テキストが画面外に完全に出たら
  if (textX < -textWidth) {
    textFinished = true;  // スクロール終了フラグを設定
  }
}

void setup() {
  M5.begin();
  M5.Power.begin();
  M5.Lcd.setTextSize(2); // テキストサイズを設定
  M5.Lcd.setTextColor(TFT_WHITE, TFT_BLACK);

  // 左上に表示
  M5.Lcd.setCursor(10, 10); // 左上の位置にカーソルを設定
  M5.Lcd.print("Speed Up");
  M5.Lcd.setCursor(35, 30);
  M5.Lcd.println("[A]");

  // 右上に表示
  M5.Lcd.setCursor(190, 10); // 右上の位置にカーソルを設定
  M5.Lcd.print("Speed Down");
  M5.Lcd.setCursor(230, 30);
  M5.Lcd.println("[C]");

  // WiFi接続
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // UDP待受開始
  udp.begin(clientPort);

  // サーバーに接続メッセージを送信
  const char* connectMessage = "接続しました";
  udp.beginPacket(serverAddress, serverPort);
  udp.write(reinterpret_cast<const uint8_t*>(connectMessage), strlen(connectMessage));
  udp.endPacket();
}

void loop() {
  // 左ボタンでスクロール速度を速くする
  if (M5.BtnA.wasPressed()) {
    scrollSpeed = max(scrollSpeed - 10, 10);  // スクロール速度を速くする
  }

  // 右ボタンでスクロール速度を遅くする
  if (M5.BtnC.wasPressed()) {
    scrollSpeed = min(scrollSpeed + 10, 100);  // スクロール速度を遅くする
  }

  // ボタンの状態を更新
  M5.update();

  if (textFinished) {  // 前のテキストのスクロールが完了した場合のみ、新しいテキストを読み込む
    int packetSize = udp.parsePacket();
    if (packetSize) {
      int len = udp.read(buf, packetSize);
      if (len >= 0) {
        buf[len] = '\0'; // バッファをnull終端
        textX = M5.Lcd.width(); // 新しいテキストが届いたときにスクロール位置をリセット
        textFinished = false; // スクロール開始フラグを設定
      }
    }
  }

  if (!textFinished) {  // スクロールが完了するまでscrollTextを呼び出す
    scrollText(buf);
  }
}
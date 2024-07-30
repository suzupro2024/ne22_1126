#include <M5Stack.h>
#include <WiFi.h>
#include <WiFiUDP.h>
#include "efont.h"
#include "efontESP32.h"
#include "efontEnableJa.h"

// WiFi設定
const char* ssid = "yourssid";  // WiFiのSSIDを指定
const char* password = "yourpassword";  // WiFiのパスワードを指定

// サーバーとクライアントの設定
const char* serverAddress = "youripaddress";  // サーバーのアドレスを指定
const int serverPort = 10024;
const int clientPort = 10025;

WiFiUDP udp;
char buf[1024];
int textX = 320; // スクロールのためのX位置
String displayedText = ""; // 現在表示中の全テキスト

void setup() {
  M5.begin();
  M5.Power.begin();
  M5.Lcd.setTextSize(2); // テキストサイズを大きく設定
  M5.Lcd.setTextColor(WHITE, BLACK);

  // WiFi接続
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    M5.Lcd.print(".");
  }

  M5.Lcd.printf("IP address: %s\n", WiFi.localIP().toString().c_str());

  // UDP待受開始
  udp.begin(clientPort);

  // サーバーに接続メッセージを送信
  const char* connectMessage = "接続しました";
  udp.beginPacket(serverAddress, serverPort);
  udp.write(reinterpret_cast<const uint8_t*>(connectMessage), strlen(connectMessage));
  udp.endPacket();
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(buf, packetSize);
    if (len > 0) {
      buf[len] = '\0'; // バッファをnull終端
      displayedText += String(buf) + " "; // 新しいメッセージを蓄積
      textX = 320; // 新しいメッセージを右端から始める
    }
  }

  // テキスト表示
  M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 40, BLACK); // 前回のテキストの部分だけクリア
  printEfont(buf, textX, 40, 2); // 日本語表示、フォントサイズを大きく設定

  // スクロールの更新
  textX -= 2; // テキストを左にスクロール
  int textWidth = displayedText.length() * 16 * 2; // 全テキストの幅を計算
  if (textX + textWidth < 0) { // 全テキストが左に移動したらリセット
    textX = 320;
  }

  delay(50); // スクロール速度調整
}

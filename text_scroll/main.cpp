#include <M5Stack.h>
#include "efontEnableJa.h"  // 日本語表示用フォントライブラリ
#include "efont.h"
#include "efontESP32.h"  // Unicode表示用ライブラリ

const int max_chars = 40;  // 一度に表示する最大文字数
const int display_width = 450;  // 画面の幅
const int char_height = 16;  // 文字の高さ
const int scroll_speed = 2;  // スクロール速度（ピクセル）

void setup() {
  M5.begin();
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(WHITE, BLACK);  // 前景色を白、背景色を黒に設定
  M5.Lcd.setCursor(0, 0);
  Serial.begin(115200);  // シリアル通信の初期化
}

void loop() {
  static char buf[max_chars + 1];  // 受信バッファ（最大文字数 + 終端文字）
  static int buf_index = 0;
  static int y = 0;  // 初期表示位置
  static int x = display_width;  // 初期X位置（右端から開始）
  static bool displayed = false;  // 表示済みフラグ

  if (Serial.available() > 0) {
    char c = Serial.read();  // 1バイト読み込み
    buf[buf_index++] = c;
    buf[buf_index] = '\0';  // 文字列の終端を設定

    // 一定の文字数に達したら表示
    if (buf_index >= max_chars) {
      buf_index = 0;  // バッファインデックスをリセット
      memset(buf, 0, sizeof(buf));  // バッファをクリア
      displayed = false;  // 新しい文字列の表示を許可
      x = display_width;  // 文字列のX位置をリセット
    }
  }

  if (!displayed) {
    // 前の文字列をスクロールしてフェードアウト
    if (x <= -display_width) {  // 完全に画面外に出たら表示済みに設定
      displayed = true;
    } else {
      // 前の位置をクリア
      M5.Lcd.fillRect(x + scroll_speed, y, max_chars * 16, char_height, BLACK);

      // 文字列を描画
      printEfont(buf, x, y, 1);

      // スクロール位置を更新
      x -= scroll_speed;
    }
  }

  // 更新間隔を調整
  delay(500);  // スクロール速度を調整（値を変えて調整）
}

/******************************************************************************************
 * FileName     : SmartFeeder_Basic_40_mission.ino
 * Description  : 이티보드 스마트 급식기 코딩 키트(Basic)
 * Author       : PEJ
 * Created Date : 2024.10.25
 * Reference    : 
******************************************************************************************/


//==========================================================================================
// 서보 모터 사용하기
//==========================================================================================.
#include <Servo.h>
Servo servo;                                             // 서보 모터 객체 생성
const int servo_pin = D6;                                // 서보 모터 핀 : D8


//==========================================================================================
// OLED 사용하기
//==========================================================================================.
#include "oled_u8g2.h"
OLED_U8G2 oled;


//==========================================================================================
// 전역 변수 선언
//==========================================================================================
const int motor_pin1 = D2;                               // 모터 제어 핀: D2
const int motor_pin2 = D3;                               // 모터 제어 핀: D3

const int motor_button = D7;                             // 먹이 공급 버튼 : D7(노랑)

const int echo_pin = D8;                                 // 초음파 수신 핀: D8
const int trig_pin = D9;                                 // 초음파 송신 핀: D9

int count;                                               // 먹이 공급 횟수
float distance;                                          // 거리
String motor_state = "off";                              // 모터 상태

unsigned long timer = 1 * 60  * 120  * 1000UL;           // 먹이 공급 타이머의 시간
unsigned long now = 0;                                   // 현재 시간
unsigned long last_feeding = 0;                          // 마지막 먹이 공급 시간
String time_remaining = "00:00:00";                      // 남은 타이머 시간

unsigned long short_previous_time = 0;
unsigned long long_previous_time = 0;


//==========================================================================================
void setup()                                             // 설정
//==========================================================================================
{
  Serial.begin(115200);                                  // 시리얼 통신 준비

  oled.setup();                                          // OLED 셋업

  pinMode(motor_pin1, OUTPUT);                           // 모터 제어 핀 1: 출력 모드
  pinMode(motor_pin2, OUTPUT);                           // 모터 제어 핀 2: 출력 모드

  pinMode(motor_button, INPUT);                          // 모터 제어 버튼: 입력 모드

  pinMode(trig_pin, OUTPUT);                             // 초음파 송신부: 출력 모드
  pinMode(echo_pin, INPUT);                              // 초음파 수신부: 입력 모드

  servo.attach(servo_pin);                               // 서보모터 핀 지정

  motor_off();                                           // 모터 중지
}


//==========================================================================================
void loop()                                              // 사용자 반복 처리
//==========================================================================================
{
  do_sensing_process();                                  // 센싱 처리

  do_automatic_process();                                // 자동화 처리

  et_short_periodic_process();                           // 짧은 주기 처리

  et_long_periodic_process();                            // 긴 주기 처리
}


//==========================================================================================
void do_sensing_process()                                // 센싱 처리
//==========================================================================================
{
  now = millis();                                        // 현재 시간 저장

  if (digitalRead(motor_button) == LOW) {                // 먹이 공급 버튼이 눌렸다면
    food_supply();                                       // 먹이 공급
  }

  // 초음파 송신
  digitalWrite(trig_pin, LOW);
  digitalWrite(echo_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);

  unsigned long duration  = pulseIn(echo_pin, HIGH);     // 초음파 수신까지의 시간 계산
  distance = duration * 17 / 1000;                       // 거리 계산

  delay(100);
}


//==========================================================================================
void food_supply()                                       // 먹이 공급
//==========================================================================================
{
  motor_control();                                       // 모터 제어

  last_feeding = now;                                    // 마지막 먹이 공급 시간 업데이트
  count += 1;                                            // 먹이 공급 횟수 증가
}


//==========================================================================================
void motor_control()                                     // 모터 제어
//==========================================================================================
{
  motor_on();                                            // 모터 작동
  delay(1000);

  motor_off();                                           // 모터 중지
}


//==========================================================================================
void motor_on()                                          // 모터 작동
//==========================================================================================
{
  motor_state = "on";                                    // 모터 상태 변경
  display_information();                                 // OLED 표시

  servo.write(50);                                       // 차단봉 열기

  digitalWrite(motor_pin1, HIGH);                        // DC 모터 작동
  digitalWrite(motor_pin2, HIGH);

  delay(1000);
}


//==========================================================================================
void motor_off()                                         // 모터 작동
//==========================================================================================
{
  motor_state = "off";                                   // 모터 상태 변경
  display_information();                                 // OLED 표시

  digitalWrite(motor_pin1, LOW);                         // DC 모터 중지
  digitalWrite(motor_pin2, LOW);

  delay(600);

  servo.write(180);                                       // 차단봉 열기
}


//==========================================================================================
void do_automatic_process()                              // 자동화 처리
//==========================================================================================
{
  if(now - last_feeding < timer && distance > 4) return;

  food_supply();                                         // 먹이 공급
}


//==========================================================================================
void et_short_periodic_process()                         // 사용자 주기적 처리 (예 : 1초마다)
//==========================================================================================
{   
  unsigned long interval = 1 * 1000UL;                   // 1초마다 정보 표시
  unsigned long now = millis();

  if (now - short_previous_time < interval) {            // 1초가 지나지 않았다면
    return;
  }
  short_previous_time = now;

  display_information();                                 // 표시 처리
}


//==========================================================================================
void display_information()                               // OLED 표시
//==========================================================================================
{
  String string_count = String(count);                   // 횟수 문자열 변환
  String string_distance = String(distance);             // 거리 문자열 변환

  time_remaining_calculate();

  oled.setLine(1, "* SmartFeeder *");                    // 1번째 줄에 펌웨어 버전
  oled.setLine(2, "count: " + string_count);             // 2번째 줄에 횟수
  oled.setLine(3, "distance: " + string_distance);      // 3번째 줄에 거리
  oled.setLine(4, "motor: " + motor_state);             // 4번째 줄에 모터 상태
  oled.setLine(5, "time: " + time_remaining);           // 5번째 줄에 타이머 남은 시간

  oled.display(5);                                       // OLED에 표시
}


//==========================================================================================
void time_remaining_calculate()                          // 남은 시간 계산
//==========================================================================================
{
  unsigned long time_cal = now - last_feeding;
  unsigned long timer_cal = timer - time_cal;

  int hour = timer_cal / (60 * 60 * 1000);
  timer_cal = timer_cal % (60 * 60 * 1000);

  int minute = timer_cal / (60 * 1000);
  timer_cal = timer_cal % (60 * 1000);

  int second = timer_cal / 1000;

  char buffer[9];  // "hh:mm:ss" 형식의 문자열을 저장할 버퍼
  sprintf(buffer, "%02d:%02d:%02d", hour, minute, second);

  time_remaining = String(buffer);
}


//==========================================================================================
void et_long_periodic_process()                          // 사용자 주기적 처리 (예 : 5초마다)
//==========================================================================================
{
  unsigned long interval = 5 * 1000UL;                   // 5초마다 정보 표시
  unsigned long now = millis();

  if (now - long_previous_time < interval) {             // 5초가 지나지 않았다면
    return;
  }
  long_previous_time = now;

  display_serial();                                      // 시리얼 모니터 정보 표시
}


//==========================================================================================
void display_serial()                                    // 메시지 송신
//==========================================================================================
{
  time_remaining_calculate();

  Serial.println("count: " + String(count));
  Serial.println("distance: " + String(distance) + " cm");
  Serial.println("time_remaining: " + String(time_remaining));
  Serial.println("-------------------------");
}


//==========================================================================================
//
// (주)한국공학기술연구원 http://et.ketri.re.kr
//
//==========================================================================================
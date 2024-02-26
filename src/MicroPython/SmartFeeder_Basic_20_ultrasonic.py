# ******************************************************************************************
# FileName     : SmartFeeder_Basic_20_ultrasonic.py
# Description  : 스마트 급식기 코딩 키트(기본)_초음파
# Author       : 박은정
# Created Date : 2024.02.26
# Reference    :
# Modified     : 
# ******************************************************************************************


#==========================================================================================
# import
#==========================================================================================
import time                                           # 시간 관련 모듈
from machine import Pin, time_pulse_us                # 핀 및 시간 관련 모듈
from ETboard.lib.pin_define import *                  # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                   # ETboard OLED 관련 모듈


#==========================================================================================
# global variable
#==========================================================================================
led_red = Pin(D2)                                     # 빨강 LED 핀 지정
led_blue = Pin(D3)                                    # 파랑 LED 핀 지정
led_green = Pin(D4)                                   # 초록 LED 핀 지정
led_yellow = Pin(D5)                                  # 노랑 LED 핀 지정

echo_pin = Pin(D8)                                    # 초음파 센서 수신부
trig_pin = Pin(D9)                                    # 초음파 센서 송신부

oled = oled_u8g2()                                    # oled 선언

count = 0                                             # 사료 공급 횟수 저장 변수


#==========================================================================================
# setup
#==========================================================================================
def setup() :
    led_red.init(Pin.OUT)                             # 빨강 LED 출력모드 설정
    led_blue.init(Pin.OUT)                            # 파랑 LED 출력모드 설정
    led_green.init(Pin.OUT)                           # 초록 LED 출력모드 설정
    led_yellow.init(Pin.OUT)                          # 노랑 LED 출력모드 설정

    trig_pin.init(Pin.OUT)                            # 초음파 센서 송신부 출력 모드 설정
    echo_pin.init(Pin.IN)                             # 초음파 센서 수신부 입력 모드 설정

    motor_off()                                       # 모터 중지


#==========================================================================================
# main loop                                           # 거리가 4cm 미만일 때 사료 공급
#==========================================================================================
def loop() :
    # 전역 변수 호출
    global count

    # 초음파 송신 후 수신부는 HIGH 상태로 대기
    trigPin.value(LOW)
    echoPin.value(LOW)
    time.sleep_ms(2)
    trigPin.value(HIGH)
    time.sleep_ms(10)
    trigPin.value(LOW)

    duration = time_pulse_us(echoPin, HIGH)           # echoPin이 HIGH를 유지한 시간 저장

    # HIGH 였을 때 시간(초음파 송수신 시간)을 기준으로 거리를 계산
    distance = 17 * duration / 1000

    if distance < 4 and distance > 0:
        food_supply()                                 # 사료 공급 함수 호출
        count += 1                                    # count 1 증가

    print("거리:", distance)
    print("횟수:", count)
    print("-----------------------------------");

    oled.clear()                                      # OLED 초기화

    count_line = "Count: %d" %(count)                 # count 값 표시 문자열 생성

    oled.setLine(1, "* Smart Fedding *")              # OLED 첫 번째 줄: 시스템 이름
    oled.setLine(2, count_line)                       # OLED 두 번째 줄: count 값
    oled.display()

    time.sleep(0.07)                                  # 초음파 측정 시 최소 시간 간격 0.07초


#==========================================================================================
# food_supply                                         # OLED 표시 및 모터 제어
#==========================================================================================
def food_supply():
    oled.setLine(3, "Motor On")                       # OLED 세 번째 줄: Motor on
    oled.display()                                    # OLED 출력
    motor_on()                                        # motor_on 함수 호출

    time.sleep(3)                                     # 3초간 대기

    oled.setLine(3, "Motor Off")                      # OLED 세 번째 줄: Motor Off
    oled.display()                                    # OLED 출력
    motor_off()                                       # motor_off 함수 호출


#==========================================================================================
# motor_on                                            # DC 모터, 진동 모터 켜기
#==========================================================================================
def motor_on():                   
    led_red.value(HIGH)                               # DC 모터 켜기
    led_blue.value(HIGH)

    led_green.value(HIGH)                             # 진동 모터 켜기
    led_yellow.value(HIGH)


#==========================================================================================
# motor_off                                           # DC 모터, 진동 모터 끄기
#==========================================================================================
def motor_off():
    led_red.value(LOW)                                # DC 모터 끄기
    led_blue.value(LOW)

    led_green.value(LOW)                              # 진동 모터 끄기
    led_yellow.value(LOW)


#==========================================================================================
# start point
#==========================================================================================
if __name__ == "__main__" :
    setup()
    while True :
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
# ******************************************************************************************
# FileName     : SmartFeeder_Basic_30_timer.py
# Description  : 스마트 급식기 코딩 키트(기본)_타이머
# Author       : 박은정
# Created Date : 2024.02.26
# Reference    :
# Modified     : 2024.04.05 : PEJ : 진동 모터 제외, 서보 모터 추가
# Modified     : 2024.08.05 : PEJ : 함수 추가 및 수정, 시간 초 변경
# ******************************************************************************************


#===========================================================================================
# import
#===========================================================================================
import time                                           # 시간 관련 모듈
from machine import Pin                               # 핀 관련 모듈
from ETboard.lib.pin_define import *                  # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                   # ETboard OLED 관련 모듈
from ETboard.lib.servo import Servo                   # ETboard Servo Motor 관련 모듈


#===========================================================================================
# global variable
#===========================================================================================
led_red = Pin(D2)                                     # 빨강 LED 핀 지정
led_blue = Pin(D3)                                    # 파랑 LED 핀 지정

oled = oled_u8g2()                                    # oled 선언

servo = Servo(Pin(D6))                                # 서보모터 핀 지정

count = 0                                             # 사료 공급 횟수 저장 변수
motor_state = "Off"                                   # 모터 상태를 "Off"로 초기화
timer_line = ""                                       # 남은 시간을 공백으로 초기화

timer = 10                                            # 사료가 공급될 시간
pre_time = 0                                          # 마지막 사료 공급 시간
now = 0                                               # 현재 시간 저장


#===========================================================================================
# setup
#===========================================================================================
def setup() :
    led_red.init(Pin.OUT)                             # 빨강 LED 출력 모드 설정
    led_blue.init(Pin.OUT)                            # 파랑 LED 출력 모드 설정

    motor_off()                                       # 모터 중지


#==========================================================================================
# main loop
#==========================================================================================
def loop() :
    global now, pre_time, count                       # 전역 변수 호출

    now = int(round(time.time()))                     # 현재 시간을 저장
    if now - pre_time >= timer:                       # 타이머가 완료되었을 시
        food_supply()                                 # 사료 공급 함수 호출
        count += 1                                    # count 1 증가
        pre_time = now                                # 마지막 사료 공급 시간 저장

    print("남은 시간:", timer - (now - pre_time), "초")
    print("횟수:", count)
    print("-----------------------------------");

    oled_print()                                      # OLED 출력 함수 호출

    time.sleep(0.1)


#===========================================================================================
# food_supply
#===========================================================================================
def food_supply():
    global motor_state                                # 전역 변수 호출

    motor_state = "On"                                # 모터 상태 변경
    oled_print()                                      # OLED 출력
    motor_on()                                        # motor_on 함수 호출

    motor_state = "OFF"                               # 모터 상태 변경
    oled_print()                                      # OLED 출력
    motor_off()                                       # motor_off 함수 호출


#===========================================================================================
# motor_on
#===========================================================================================
def motor_on():
    servo.begin()
    servo.write_angle(50)                             # 차단봉 열기
    servo.end()   

    led_red.value(HIGH)                               # DC 모터 켜기
    led_blue.value(HIGH)

    time.sleep(1)                                     # 1초간 대기


#===========================================================================================
# motor_off
#===========================================================================================
def motor_off():
    led_red.value(LOW)                                # DC 모터 끄기
    led_blue.value(LOW)

    time.sleep(0.6)                                   #  0.6초간 대기

    servo.begin()
    servo.write_angle(180)                            # 차단봉 닫기
    servo.end()


#===========================================================================================
# oled_print
#===========================================================================================
def oled_print():
    global last_feeding_time, now, timer_line         # 전역 변수 호출


    count_line = "Count: %d" %(count)                 # count 값 표시 문자열 저장
    motor_line = "Motor: " + motor_state              # 모터 상태 표시 문자열 저장
    time_calculate()                                  # 남은 타이머 시간 문자열 저장

    oled.clear()                                      # OLED 초기화

    oled.setLine(1, "* Smart Feeder *")               # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, count_line)                       # OLED 두 번째 줄: 사료 공급 횟수
    oled.setLine(3, timer_line)                       # OLED 세 번째 줄: 남은 시간
    oled.setLine(4, motor_line)                       # OLED 네 번째 줄: 모터 상태

    oled.display()


#===========================================================================================
# time_calculate
#===========================================================================================
def time_calculate():
    global now, pre_time, timer_line

    cal_time = now - pre_time
    minute, sec = divmod(timer - cal_time, 60)
    hour = 0
    if minute > 60:
        hour = int(minute / 60)
        minute = minute % 60
    timer_line = "Timer: " + '{:0>2}'.format(hour) + ':' + '{:0>2}'.format(minute) + ':' + \
                 '{:0>2}'.format(sec)


#===========================================================================================
# start point
#===========================================================================================
if __name__ == "__main__" :
    setup()
    while True :
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
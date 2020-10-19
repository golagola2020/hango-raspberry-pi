# 외장모듈
import os
import sys                     # 시스템 모듈
from gtts import gTTS          # TTS 모듈
from pygame import mixer, time

# 내장모듈
from Http import Http
from config import *

class Gspeak:

    def __init__(self, speed):
        # 음성 파일명 변수
        self.sound_msgs = {
            'basic': {},
            'position': {},
            'sold': {},
            'sold_out': {}
        }

        mixer.init(speed)

    def get_sound_msgs(self):
        '''
            sound_msgs 반환 함수
        '''

        return self.sound_msgs

    def save_sound(self, file_path, file_name, message):
        '''
            사운드 저장 함수
        '''

        # 파일 경로, 파일명과 메세지 출력
        print(f'File Path : {file_path}, File Name : {file_name}, Message : {message}')

        # mp3 변환 및 출력, 한국어
        tts = gTTS(text=message, lang='ko')
        tts.save(f'{RPI_FILE_PATH}/sounds/{file_path}/{file_name}.mp3')

    def refresh_message(self, drinks):
        '''
            사운드 메세지 제작 함수 
        '''

        # 자판기의 모든 음료 정보를 하나의 문자열로 병합
        names = ""
        for i, name in enumerate(drinks["name"]):
            names += f"{str(i+1)}번 {name}, "

        # 센싱되고 있지 않은 기본 상태 메세지
        self.sound_msgs["basic"]["basic"] = f"안녕하세요. 말하는 음료수 자판기입니다. 지금부터 음료수 위치와 이름을 말씀드리겠습니다. {names} 감사합니다. 저는 행고입니다. 웃음 웃음 "

        # 음료수 이름을 파일명으로 하고 메세지 만들기
        for idx in range(len(drinks["name"])):
            # 손이 음료를 향해 위치한 상태 메세지
            self.sound_msgs["position"][drinks["name"][idx]] = f"{drinks['name'][idx]}. {str(drinks['price'][idx])}원입니다아 ."
            # 음료수가 팔린 상태
            self.sound_msgs["sold"][drinks["name"][idx]] = f"{drinks['name'][idx]} 선택. 맛있게 드시고 즐거운 하루 되십시오 ."
            # 음료수 품절 상태
            self.sound_msgs["sold_out"][drinks["name"][idx]] = f"{drinks['name'][idx]}, 품절입니다아 ."

    def update_message(self, drinks):
        '''
            자판기 음료수 중 수정된 것이 있는지, 없는지 반환하는 함수
        '''
        # 서버로부터 전달된 음료수 이름들 순회
        for idx, drink_name in enumerate(drinks["name"]):
            # 사운드로 만들어지지 않은 음료수가 있다면 실행
            if drink_name not in self.sound_msgs["position"]:
                # 자판기의 모든 음료 정보를 하나의 문자열로 병합
                print(f'추가된 음료 : {drink_name}\n{drink_name} 음성 파일을 생성합니다...')
                names = ""
                for i, name in enumerate(drinks["name"]):
                    names += f"{str(i+1)}번 {name} "

                # 센싱되고 있지 않은 기본 상태 메세지
                self.sound_msgs["basic"]["basic"] = f"안녕하세요. 말하는 음료수 자판기입니다. 지금부터 음료수 위치와 이름을 말씀드리겠습니다. {names}"
                self.save_sound('basic', 'basic', self.sound_msgs["basic"]["basic"])
                # 손이 음료를 향해 위치한 상태 메세지
                self.sound_msgs["position"][drinks["name"][idx]] = f"{drinks['name'][idx]} {str(drinks['price'][idx])}원. "
                self.save_sound('position', drinks["name"][idx], self.sound_msgs["position"][drinks["name"][idx]])
                # 음료수가 팔린 상태
                self.sound_msgs["sold"][drinks["name"][idx]] = f"{drinks['name'][idx]} 선택. 맛있게 드시고 즐거운 하루 되십시오. "
                self.save_sound('sold', drinks["name"][idx], self.sound_msgs["sold"][drinks["name"][idx]])
                # 음료수 품절 상태
                self.sound_msgs["sold_out"][drinks["name"][idx]] = f"{drinks['name'][idx]} 품.절. "
                self.save_sound('sold_out', drinks["name"][idx], self.sound_msgs["sold_out"][drinks["name"][idx]])

    def say(self, folder_name, sound_name='basic'):
        '''
            pygame으로 말하는 함수

            각 상태에 따라 출력 메세지가 달라진다.
                
                1. basic : 센싱되고 있지 않은 기본 상태
                2. position : 손이 음료를 향해 위치한 상태
                3. sold : 음료수가 팔린 상태
                4. sold_out : 음료수 품절 상태
        '''

        # 폴더명과 사운드명 출력
        print(f'Folder Name : {folder_name}, Sound Name : {sound_name}')

        mixer.music.load(f'{RPI_FILE_PATH}/sounds/{folder_name}/{sound_name}.mp3')
        mixer.music.play()

        # 'basic' 상태가 아니면 실행 중인 음성 파일이 종료될 때까지 대기시킨다.
        if folder_name != 'basic':
            clock = time.Clock()
            while mixer.music.get_busy():
                print("음성 출력 중...")
                clock.tick(1000)    # 재생 시간 연장
    
    def stop(self):
        '''
            pygame 음성 종료 함수
        '''
        if mixer.music.get_busy():
            mixer.music.stop()

    def is_available(self):

        if mixer.music.get_busy():
            return False
        return True
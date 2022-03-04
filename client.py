from datetime import datetime
import os
import socket
import threading

import cv2
import pyaudio

import warnings
warnings.filterwarnings("ignore")


class Client:

    def __init__(self):
        name_client = input('What is your name? ')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                self.target_ip = input('Enter IP address of server --> ')
                self.target_port = 9090
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")


        # _init_ params
        FONT = cv2.FONT_HERSHEY_PLAIN
        self.chunk_size = 1024  # 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000


        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                          output=True, frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                             input=True, frames_per_buffer=self.chunk_size)

        self.record_on = True
        self.aux = []

        print("Connected to Server")
        self.s.send(name_client.encode("utf-8"))
        print("Server > " + self.s.recv(1024).decode("utf-8"))

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()

        while True:
            img = cv2.imread("bb.png")
            title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if self.record_on:
                img = cv2.flip(img, 1)
                cv2.putText(img, "REC", (40, 40), FONT, 3, (0, 0, 255), 3)
                cv2.putText(img, title, (40, 450), FONT, 3, (255, 255, 255), 2)
                cv2.imshow('Audio chat :)', img)
                try:
                    data = self.recording_stream.read(1024)
                    self.aux.append(data)
                    self.s.sendall(self.aux[-1])
                except:
                    pass
            else:
                img = cv2.flip(img, 1)
                cv2.putText(img, "MUTE", (40, 40), FONT, 3, (255, 0, 0), 3)
                cv2.putText(img, "The chat room ", (40, 400), FONT, 3, (255, 255, 255), 2)
                cv2.putText(img, "can't hear you!", (200, 450), FONT, 3, (255, 255, 255), 2)
                cv2.imshow('Audio chat :)', img)

                del self.aux[:]
                self.recording_stream.stop_stream()

            q = cv2.waitKey(1)
            if q == ord('p'):
                self.record_on = False
            if q == ord('c'):
                self.record_on = True
                self.recording_stream.start_stream()
            if q == ord('q'):
                print("Thanks for testing!")
                self.s.send(b"disconnect")
                os._exit(0)

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


client = Client()

#!/usr/bin/python3

#
#        Guardian of mall chatbot
#
#        Copyright (C) 2022 - All Rights Reserved
#
#        Group:
#            Mariniello Alessandro  0622702106   a.mariniello15@studenti.unisa.it
#            Pepe       Paolo   0622702005   p.pepe17@studenti.unisa.it
#            Rabasca    Dario   0622702003   d.rabasca@studenti.unisa.it
#            Vicidomini Luigi   0622701949  l.vicidomini11@studenti.unisa.it
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import rospy
from std_msgs.msg import Int16MultiArray, Bool
import numpy as np
import sounddevice
import speech_recognition as sr


def is_pepper_speaking_callback(is_speaking):
    """
    Callback function, it is called when Pepper speaks to turn off and on the microphone
    so that Pepper does not hear its own voice
    """
    global stop_listening
    global is_person_engaged

    # if is_person_engaged:
    # if person is engaged it deactivate the microphone
    if is_speaking.data:
        print('Pepper is speaking, stop listening...')
    
        # stopping background listening
        stop_listening()
        
    else:
        print('Pepper has done speaking, start listening...')
        # starting again background listening
        stop_listening = r.listen_in_background(m, callback)
        


def detection_callback(is_person_detected):
    """
    Callback function, it is called the instant when a person is considered to be in the scene or out of the scene,
    if the person is in the scene, Pepper starts listening otherwise it deactivates the microphone
    """
    global stop_listening
    global is_person_engaged

    if is_person_detected.data:
        is_person_engaged = True
        print('Person detected, start listening...')
        try:
            # starting again background listening
            stop_listening = r.listen_in_background(m, callback)
        except:
            pass
    else:
        is_person_engaged = False
        print('Person not detected, stop listening...')
        try:
            # stopping background listening
            stop_listening()
        except:
            pass


def callback(recognizer, audio):
    """
    Callback function, it is called whenever a piece of audio gets detected by the recognizer, it publishes in
    the "mic_data" topic
    """
    data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    data_to_send = Int16MultiArray()
    data_to_send.data = data

    pub.publish(data_to_send)


# initializing node and all the topics it will use
rospy.init_node('voice_detection_node', anonymous=True)

pub = rospy.Publisher('mic_data', Int16MultiArray, queue_size=10)

rospy.Subscriber('is_pepper_speaking', Bool, is_pepper_speaking_callback)
# rospy.Subscriber('detection', Bool, detection_callback)

# setting the engagement of the person initially to False
is_person_engaged = False

# Initialize a Recognizer
r = sr.Recognizer()

# Audio source
m = sr.Microphone(device_index=None,
                  sample_rate=16000,
                  chunk_size=1024)

# Calibration within the environment
# we only need to calibrate once, before we start listening
print("Calibrating...")
with m as source:
    r.adjust_for_ambient_noise(source, duration=3)
    # r.energy_threshold = 150
print("Calibration finished")

# start listening in the background
# `stop_listening` is now a function that, when called, stops background listening
stop_listening = r.listen_in_background(m, callback)

rospy.spin()

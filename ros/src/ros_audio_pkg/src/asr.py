#!/usr/bin/env python3

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
from std_msgs.msg import Int16MultiArray, String
import numpy as np

from speech_recognition import AudioData
import speech_recognition as sr

# Initialize a Recognizer
r = sr.Recognizer()

# Init node
rospy.init_node('speech_recognition', anonymous=True)
pub1 = rospy.Publisher('voice_txt', String, queue_size=10)


def callback(audio):
    """
    This callback takes as input the audio track and sends it to google recognizer to
    extract the sentence.
    """
    data = np.array(audio.data, dtype=np.int16)
    audio_data = AudioData(data.tobytes(), 16000, 2)
    try:
        spoken_text = r.recognize_google(audio_data, language='en-GB')
        print("Here's what google understood, I'm posting it: " + spoken_text)
        pub1.publish(spoken_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition cannot understand from this audio file")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def listener():
    """
    This function when 'mic_data' topic publish something, the callback is activated passing as input the
    Int16MultiArray which represent the audio track
    """
    rospy.Subscriber("mic_data", Int16MultiArray, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

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
from std_msgs.msg import String, Bool
from pepper_nodes.srv import Text2Speech
from std_msgs.msg import Bool
import time

def main():
    print('Starting tts client...')

    rospy.init_node('speaking_node')
    rospy.wait_for_service('/tts')
    tts_service = rospy.ServiceProxy('/tts', Text2Speech)
    synchronize_speech = rospy.Publisher('is_pepper_speaking', Bool, queue_size=10)

    while not rospy.is_shutdown():
        txt = rospy.wait_for_message("bot_answer", String)

        # pepper starts to talk, stop speech recognition
        synchronize_speech.publish(True)
        
        msg: str = txt.data
        msg = msg.replace(",", "\\pau=100\\")
        msg = msg.replace(".", "\\pau=200\\")

        tts_service(msg)
        time.sleep(1)

        # pepper finishes to talk, starting again speech recognition
        synchronize_speech.publish(False)


if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass
    
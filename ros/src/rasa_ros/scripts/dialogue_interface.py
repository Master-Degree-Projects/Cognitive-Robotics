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
from std_msgs.msg import String, Bool
from rasa_ros.srv import Dialogue
from pepper_nodes.srv import LoadUrl, ExecuteJS, LoadUrlRequest


class TerminalInterface:
    """
    Class implementing a terminal i/o interface.

    Methods
    - get_text(self): return a string read from the terminal
    - set_text(self, text): prints the text on the terminal

    """

    def __init__(self):
        self.pub_answer = rospy.Publisher('bot_answer', String, queue_size=10)  # Publisher of the RASA answer
        self.sub_det = rospy.Subscriber('detection', Bool, queue_size=1)

    def get_text(self):
        print("Waiting the speech...")
        txt = None
        while txt is None:
            try:
                txt = rospy.wait_for_message("voice_txt", String)
            except:
                pass

        # prints on terminal the input message
        print("[IN]:", txt.data)

        return str(txt.data)

    def set_text(self, text):
        # prepares the text in input for publication, then it publishes it
        data_to_send = String()
        data_to_send.data = text
        self.pub_answer.publish(data_to_send)

        # prints on terminal the received output message 
        print("[OUT]:", text)


def main():
    # initializing node and topic it will use
    rospy.init_node('writing')

    rospy.wait_for_service('dialogue_server')
    dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)

    terminal = TerminalInterface()

    while not rospy.is_shutdown():
        # getting message from terminal, that is what user says
        message = terminal.get_text()

        if message == 'exit':
            break

        try:
            # getting bot answer and posting it in the topic
            bot_answer = dialogue_service(message)
            terminal.set_text(bot_answer.answer)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

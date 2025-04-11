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

from rasa_ros.srv import Dialogue, DialogueResponse
import rospy
import requests


def handle_service(req):
    input_text = req.input_text
    print('INPUT', input_text)
    # Get answer
    ip = "10.0.1.224"  # NOTE: change ip to you IP!!!
    get_answer_url = f"http://{ip}:5002/webhooks/rest/webhook"
    message = {
        "sender": 'bot',
        "message": input_text
    }

    r = requests.post(get_answer_url, json=message)
    response = DialogueResponse()
    response.answer = ""
    for i in r.json():
        response.answer += i['text'] + ' ' if 'text' in i else ''
    print('RESPONSE', response.answer)
    return response


def main():
    # Server Initialization
    rospy.init_node('dialogue_service')

    s = rospy.Service('dialogue_server',
                      Dialogue, handle_service)

    rospy.logdebug('Dialogue server READY.')
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        pass

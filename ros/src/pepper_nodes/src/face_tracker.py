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

from utils import Session
from optparse import OptionParser
import rospy
from pepper_nodes.srv import WakeUp, Rest
import qi
import argparse
import sys


class TrackerNode:
    """
    This class implements a ROS node used to control the Pepper posture
    """

    def __init__(self, ip, port, faceSize):
        """
        The constructor creates a session to Pepper and initializes the services
        """
        self.ip = ip
        self.port = port
        self.session = Session(ip, port)
        self.faceSize = faceSize
        self.motion_proxy = self.session.get_service("ALMotion")
        self.posture_proxy = self.session.get_service("ALRobotPosture")
        self.tracker_service = self.session.get_service("ALTracker")
        self.animation_player_service = self.session.get_service("ALAnimationPlayer")

    def stop(self, *args):
        """
        This method calls the ALMotion service and sets the robot to rest position
        """
        try:
            self.motion_proxy.rest()
            self.tracker_service.stopTracker()
        except:
            self.tracker_service = self.session.get_service("ALTracker")
            self.tracker_service.stopTracker()
        return "ACK"

    def start(self):
        """
        Starts the detection of the face
        """
        rospy.init_node("tracker_node")
        self.trackernode()
        rospy.Service("tracker", WakeUp, self.trackernode)
        rospy.spin()

    def trackernode(self, *args):
        """
        This method calls the ALMotion and ALRobotPosture services and it sets motors on and then it sets the robot posture to initial position
        """
        try:
            # Add target to track.
            targetName = "Face"
            faceWidth = self.faceSize
            self.tracker_service.registerTarget(targetName, faceWidth)
            # Then, start tracker.
            self.tracker_service.track(targetName)
        except:
            self.motion_proxy = self.session.get_service("ALMotion")
            self.posture_proxy = self.session.get_service("ALRobotPosture")
            self.tracker_service = self.session.get_service("ALTracker")
            self.animation_player_service = self.session.get_service("ALAnimationPlayer")

        return "ACK"


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.230")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = TrackerNode(options.ip, int(options.port), 0.1)
        node.start()
    except rospy.ROSInterruptException:
        node.stop()

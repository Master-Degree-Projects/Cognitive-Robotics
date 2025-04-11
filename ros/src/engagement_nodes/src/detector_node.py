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

import os

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String, Bool
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
import ros_numpy # pip3 install git+https://github.com/eric-wieser/ros_numpy
import cv2
from cv_bridge import CvBridge
import tensorflow as tf
assert(int(tf.__version__.split('.')[0]) >= 2)
import numpy as np


class Detector:
    """
    Detector class, uses the model defined in the initialization method for detection
    """
    def __init__(self, mode="face"):
        """
        Constructor of the Detector class, it takes in input the mode (it can be either "face" or "person")
        """
        self.mode = mode

        if mode != "face" and mode != "person":
            raise Exception("Detector mode must be either 'face' or 'person'.")
        if mode == "face":
            faceProto = "/home/luigi/Desktop/group3_ws/group3_ws/src/engagement_nodes/src/opencv_face_detector.pbtxt"
            faceModel = "/home/luigi/Desktop/group3_ws/group3_ws/src/engagement_nodes/src/opencv_face_detector_uint8.pb"
            self.faceNet = cv2.dnn.readNet(faceModel, faceProto)
            self.br = CvBridge()
        else:
            detector_path = os.path.join(os.path.dirname(__file__), "efficientdet_d1_coco17_tpu-32")
            self.detect_fn = tf.saved_model.load(detector_path)

    def __call__(self, img, threshold=0.8):
        """
        Call function of the Detector class, it takes in input the image to use for detection and
        a threshold value used to filter all the detections. It uses the mode set during the initialization
        of the Detector object.
        """
        if self.mode == "face":
            # using face detector
            frame = self.br.imgmsg_to_cv2(img)
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)
            self.faceNet.setInput(blob)
            detections = self.faceNet.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > threshold and detections[0, 0, i, 5] < 1 and detections[0, 0, i, 6] < 1:
                    return True

            return False
        else:
            # using object detector, filtering the results by person class
            img = ros_numpy.numpify(img)
            img = img[:, :, ::-1]

            # convert the received image in tensor
            input_tensor = tf.convert_to_tensor(img)
            input_tensor = input_tensor[tf.newaxis, ...]

            # using the model to detect the objects
            detections = self.detect_fn(input_tensor)

            num_above_thresh = np.sum(detections['detection_scores'] > threshold)

            detections.pop('num_detections')
            detections = {key: value[0, :num_above_thresh].numpy() for key, value in detections.items()}
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

            for detection_label in detections['detection_classes']:
                if detection_label == person_id:
                    # a person has been detected
                    return True

            return False

def rcv_image(msg):
    """
    Callback functions
    """
    global number_of_presence_frames
    global number_of_absence_frames
    global first_detection

    person_detected = my_detector(msg)

    rospy.loginfo(str(person_detected))

    # if a person has been detected it updates the number_of_presence_frames and resets the
    # number_of_absence_frames variable
    if person_detected:
        number_of_presence_frames += 1
        number_of_absence_frames = 0
    else:  # otherwise it updates the number_of_absence_frames and resets the number_of_presence_frames variable
        number_of_presence_frames = 0

    if first_detection and not person_detected:
        number_of_absence_frames += 1

    # if the person stays for threshold consecutive frames it is considered "present"
    if number_of_presence_frames == presence_threshold:
        first_detection = True
        pub.publish(True)
        rospy.loginfo("Person detected: publishing to topic...")

    elif number_of_absence_frames == absence_threshold:
        pub.publish(False)
        rospy.loginfo("Person gone: publishing to topic...")


# initializing detector
my_detector = Detector("person")

# detector id for person class
person_id = 1

# auxiliary variables for counting the number of frames a person stays in or out of the scene
number_of_presence_frames = 0
number_of_absence_frames = 0
# variable used to check whether at least an initial detection has occurred
first_detection = False

# number of frames after which the person is considered present in the scene or absent
presence_threshold = 3
absence_threshold = 5


if __name__ == "__main__":
    try:
        # initializing node with the topic it will use
        rospy.init_node('detector_node')
        pub = rospy.Publisher('detection', Bool, queue_size=2)
        sub_img = rospy.Subscriber("in_rgb", Image, rcv_image)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass

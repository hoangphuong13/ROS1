#!/usr/bin/env python3
import rospy
import random
from geometry_msgs.msg import Twist

def random_velocity():
    rospy.init_node('random_turtle_controller', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz 

    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = random.uniform(-2.0, 2.0)  # toc do ngau nhien -2 den 2 
        msg.angular.z = random.uniform(-2.0, 2.0)  # doc quay ngau nhien -2 den 2 
        rospy.loginfo(f" vi tri cua rua theo truc x = {msg.linear.x}, vi tri cua rua theo truc z = {msg.angular.z}")
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        random_velocity()
    except rospy.ROSInterruptException:
        pass

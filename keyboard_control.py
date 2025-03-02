#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Điều khiển rùa:
W/S: Tăng/Giảm tốc độ
A/D: Quay trái/phải
Q: Dừng lại
CTRL+C để thoát
"""

def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
    return key

def keyboard_control():
    rospy.init_node('keyboard_control', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    speed = 0.0
    turn = 0.0
    twist = Twist()

    print(msg)
    while not rospy.is_shutdown():
        key = get_key()
        if key == 'w':
            speed += 0.5
        elif key == 's':
            speed -= 0.5
        elif key == 'a':
            turn += 0.5
        elif key == 'd':
            turn -= 0.5
        elif key == 'q':
            speed = 0.0
            turn = 0.0

        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)

if __name__ == '__main__':
    try:
        keyboard_control()
    except rospy.ROSInterruptException:
        pass

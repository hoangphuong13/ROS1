#!/usr/bin/env python3
import rospy
import random
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

# Kích thước bản đồ (11x11)
MAP_SIZE = 11.0
ESCAPE_DISTANCE = 1.0  # Khoảng cách rời xa tường sau khi quay

cmd_pub = None  # Publisher để điều khiển rùa

def pose_callback(msg):
    global cmd_pub

    x, y = msg.x, msg.y  # Lấy tọa độ hiện tại của rùa
    twist = Twist()

    # Kiểm tra nếu rùa chạm tường
    if x <= 0.5 or x >= (MAP_SIZE - 0.5) or y <= 0.5 or y >= (MAP_SIZE - 0.5):
        rospy.logwarn(f"⚠️ Rùa chạm tường tại (x={x:.2f}, y={y:.2f}) - Đổi hướng!")
        
        # Dừng ngay lập tức
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        cmd_pub.publish(twist)
        rospy.sleep(0.5)

        # Quay một góc ngẫu nhiên từ 90° đến 180°
        twist.angular.z = random.choice([-1, 1]) * random.uniform(1.5, 3.0)
        cmd_pub.publish(twist)
        rospy.sleep(1)  # Chờ quay hoàn tất

        # Di chuyển ra xa tường
        twist.linear.x = ESCAPE_DISTANCE
        twist.angular.z = 0.0
        cmd_pub.publish(twist)
        rospy.sleep(1.5)  # Chờ di chuyển

    else:
        # Nếu rùa ở vùng an toàn, hiển thị thông báo
        rospy.loginfo(f"✅ Rùa ở vị trí an toàn (x={x:.2f}, y={y:.2f})")

    # Tiếp tục đi thẳng sau khi tránh tường
    twist.linear.x = 2.0
    twist.angular.z = 0.0
    cmd_pub.publish(twist)

def main():
    global cmd_pub
    rospy.init_node('turtle_pose_monitor', anonymous=True)

    cmd_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

    rospy.spin()  # Chạy liên tục

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

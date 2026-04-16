#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix, NavSatStatus
import math

# Arbitrary origin in degrees
LAT0 = 22.4623967
LON0 = 114.0318546
ALT0 = 34.51


def odom_cb(msg):
    rospy.loginfo_throttle(1.0, "odom_cb called, publishing NavSatFix")
    # Get local coordinates in meters (odom frame)
    x = msg.pose.pose.position.x  # East (m)
    y = msg.pose.pose.position.y  # North (m)
    z = msg.pose.pose.position.z  # Up (m)

    # Approximate conversion meters -> degrees
    # 1 deg lat ~ 111,320 m
    dlat = y / 111320.0
    # 1 deg lon ~ 111,320 * cos(lat0)
    dlon = x / (111320.0 * math.cos(math.radians(LAT0)))

    lat = LAT0 + dlat
    lon = LON0 + dlon
    alt = ALT0 + z

    navsat = NavSatFix()
    navsat.header.stamp = msg.header.stamp
    navsat.header.frame_id = "base_link"  # or any frame you want

    navsat.status.status = NavSatStatus.STATUS_FIX
    navsat.status.service = NavSatStatus.SERVICE_GPS

    navsat.latitude = lat
    navsat.longitude = lon
    navsat.altitude = alt

    # Fake reasonable covariance (or set to 0)
    navsat.position_covariance = [0.109561, 0.0, 0.0,
                                  0.0, 0.109561, 0.0,
                                  0.0, 0.0, 0.272484]
    navsat.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

    pub.publish(navsat)

if __name__ == '__main__':
    rospy.init_node('fake_global_from_odom')

    pub = rospy.Publisher('/mavros/global_position/global1',
                          NavSatFix, queue_size=10)

    rospy.Subscriber('/mavros/global_position/local', Odometry, odom_cb)

    rospy.loginfo("Publishing fake /mavros/global_position/global1 from /mavros/global_position/local")
    rospy.spin()


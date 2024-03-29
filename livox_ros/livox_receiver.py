import time

import numpy as np
import cv2

import rospy
from sensor_msgs.msg import Image as Image_msg
from sensor_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import read_points_list,PointField

# path: /home/zhengxinyue/livox_ws/devel/lib/python2.7/dist-packages/livox_ros_driver/msg
from _CustomMsg import CustomMsg

from sensor_msgs import point_cloud2
from ros_numpy.point_cloud2 import get_xyz_points, pointcloud2_to_xyz_array
from ros_numpy.image import image_to_numpy, numpy_to_image

#from livox_ros.yolox_demo import get_predictor
import ros_numpy
#predictor = get_predictor()


def numpy_to_pointcloud2(points, stamp, frame_id):
    # 创建PointCloud2消息
    msg = PointCloud2()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id

    # 设置PointCloud2消息的字段
    msg.height = 1
    msg.width = points.shape[0]
    msg.fields.append(PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1))
    msg.fields.append(PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1))
    msg.fields.append(PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1))
    msg.fields.append(PointField(name="reflectivity", offset=16, datatype=PointField.FLOAT32, count=1))
    msg.is_bigendian = False
    msg.point_step = 16
    msg.row_step = msg.point_step * msg.width
    msg.is_dense = True

    # 将点云数据填充到PointCloud2消息中
    msg.data = points.tobytes()
    
    # msg.data = points.tostring()

    return msg


def livox_callback(msg):
    pass
    # p = msg.points
    # data = np.array([[i.x, i.y, i.z] for i in p])

    # data = msg.points

    # 尝试将已经通过numpy.buffer获得的点云numpy数据--->转化成pointcloud2格式的 然后将其发布出来 

    # 获取numpy数组
    points = msg.my_points
    # print(points)
    # 获取数据没问题


    print("Array dtype:", points.dtype)
    print("Array fields:", points.dtype.names)

    # # 假设已经获得时间戳和坐标系名称
    stamp = rospy.Time.now()
    frame_id = "map"

    # # 转换为PointCloud2消息
    pointcloud_msg = numpy_to_pointcloud2(points, stamp, frame_id)


    # 发布PointCloud2消息
    publisher.publish(pointcloud_msg)





def pc2_callback(msg):
    pass
    # points = read_points_list(msg)
    p = pointcloud2_to_xyz_array(msg)


# def image_callback(msg):
#     # print('image: ', msg.header.stamp.to_sec())
#     image = image_to_numpy(msg)
#     # object detect
#     outputs, img_info = predictor.inference(image)
#     result_image = predictor.visual(outputs[0], img_info, predictor.confthre)
#     image_publisher.publish(numpy_to_image(result_image, encoding='rgb8'))


if __name__ == '__main__':
    rospy.init_node('livox_convert_')
    livox_subscriber = rospy.Subscriber('/livox/lidar', CustomMsg, callback=livox_callback, queue_size=1)
    publisher = rospy.Publisher('/converted_pointcloud', PointCloud2, queue_size=1)
    # pc2_subscriber = rospy.Subscriber('/test_pointcloud', PointCloud2, callback=pc2_callback, queue_size=1)
    
    # 接收图像并解析
    #image_subscriber = rospy.Subscriber('/camera/color/image_raw', Image_msg, callback=image_callback, queue_size=1)
    #image_publisher = rospy.Publisher('/detect_image', Image_msg, queue_size=1)

    rospy.spin()

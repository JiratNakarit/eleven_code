#######################################################################################################################
'''
    Description
    ___________
    version: 1.2.1
    author: Jirat Nakarit
    Postscript: 1. This code for Real Sense D435.
                2. Now you cannot use record and read at the same time.
'''
#######################################################################################################################

import numpy as np
import cv2
import pyrealsense2 as rs


class MyCamera:

    def get_frame(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        return depth_frame, color_frame

    def get_image(self, depth_frame, color_frame):
        # Convert images to numpy arrays
        depth_img = np.asanyarray(depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())

        return depth_img, color_img

    def get_colormap(self, depth_img):
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        rescale_depth_img = cv2.convertScaleAbs(depth_img, alpha=0.0255)
        # dst[i] = saturate_cast(src[i] * alpha + beta)
        # In this case, use scale 0 - 255
        depth_colormap = cv2.applyColorMap(rescale_depth_img, cv2.COLORMAP_JET)

        return depth_colormap

    def release_camera(self):
        cv2.destroyAllWindows()
        self.pipeline.stop()

    def createRatio(self, X):
        dict = {
            424: 240,
            640: 480,
            1280: 720
        }
        return dict[X]


class Camera(MyCamera):

    def __init__(self, X=640, framerate=30):

        Y = self.createRatio(X)

        # Configure depth and color stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, X, Y, rs.format.z16, framerate)
        self.config.enable_stream(rs.stream.color, X, Y, rs.format.bgr8, framerate)

        # Start streaming
        self.pipeline.start(self.config)


class Record(MyCamera):

    def __init__(self, FILE, X=640, framerate=30):

        Y = self.createRatio(X)

        # Configure depth and color stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, X, Y, rs.format.z16, framerate)
        self.config.enable_stream(rs.stream.color, X, Y, rs.format.bgr8, framerate)

        self.config.enable_record_to_file(FILE)

        # Start streaming
        self.pipeline.start(self.config)

class Player(MyCamera):

    def __init__(self, FILE, X=640, framerate=30):

        Y = self.createRatio(X)

        # Configure depth and color stream
        self.pipeline = rs.pipeline()
        config = rs.config()

        rs.config.enable_device_from_file(config, FILE)

        config.enable_stream(rs.stream.depth, X, Y, rs.format.z16, framerate)
        config.enable_stream(rs.stream.color, X, Y, rs.format.bgr8, framerate)

        # Start streaming
        self.pipeline.start(config)

#######################################################################################################################
################################### \\ THESE IS AN EXAMPLE FOR USED THIS FUNCTION //###################################
#######################################################################################################################

if __name__ == "__main__":

    ''' This for open or use camera '''
    cam = Camera(640, 30)
    cam.release_camera()
    while True:
        depth_frame, color_frame = cam.get_frame()
        depth_img, color_img = cam.get_image(depth_frame, color_frame)
        depth_map = cam.get_colormap(depth_img)
        cv2.imshow('image', depth_map)
        cv2.imshow('depth', depth_map)
        cv2.imshow('color', color_img)
        if cv2.waitKey(1) == 27:
            cam.release_camera()
            break

    ''' Thia for record to .bag file '''
    # import time
    # rec = Record('test.bag', 424, 15)
    # t = time.time()
    # while True:
    #     depth_frame, color_frame = rec.get_frame()
    #     depth_img, color_img = rec.get_image(depth_frame, color_frame)
    #     depth_map = rec.get_colormap(depth_img)
    #     cv2.imshow('depth', depth_map)
    #     cv2.waitKey(1)
    #     if (time.time() - t) >= 5.00:
    #         rec.release_camera()
    #         break

    ''' This for read .bsag file '''
    # red = Player('test.bag', 424, 15)
    # while True:
    #     depth_frame, color_frame = red.get_frame()
    #     depth_img, color_img = red.get_image(depth_frame, color_frame)
    #     depth_map = red.get_colormap(depth_img)
    #     cv2.imshow('depth', depth_map)
    #     k = cv2.waitKey(1)
    #     if k == 27:
    #         break

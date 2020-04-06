# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import pickle
import cv2
import os

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

CWD = "/home/sviatoslav/Desktop/ParkSmart"
camera_data_path_global = CWD + '/data/pickle/camera_calibration_pickle.p' 
homography_data_path_global = CWD + '/data/pickle/perspective_transform_pickle.p' 

"""
LOAD_PICKLED_DATA:
Get pickled matrix data for distortion and perspective corrections
NOTE: with statement closes file automatically after statement ends
"""
with open( camera_data_path_global, mode = 'rb' ) as f: file = pickle.load( f )
roi = file[ 'roi' ]
mtx = file[ 'mtx' ]
dist = file[ 'dist' ]
new_cam_mat = file[ 'newCamMat' ]

with open( homography_data_path_global, mode = 'rb' ) as f: file = pickle.load( f )
m = file[ 'M' ]

def gstreamer_pipeline(
    capture_width=3264,
    capture_height=2464,
    display_width=3264,
    display_height=2464,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    folder_path = "/home/sviatoslav/Desktop/ParkSmart/data/calibration_images/"
    prefix = "img_"
    suffix = ".JPG"
    index = 0

    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()

            h, w = img.shape[ : 2 ]
            dsize = ( w, h )
            #img = cv2.undistort( img, mtx, dist, None, mtx )
            img = cv2.warpPerspective( img, m, dsize )
            cv2.imshow("CSI Camera", img)
            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            elif keyCode == 32:
                img_path = folder_path + prefix + str( index ) + suffix
                cv2.imwrite( img_path, img )  
                index = index + 1

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()

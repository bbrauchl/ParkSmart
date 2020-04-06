#===============================================================================
# IMPORT_LIBRARIES
#===============================================================================
import numpy as np
import cv2 as cv
import pickle
import glob
import os
import time
#===============================================================================
# VARIABLE_DECLARATIONS
#===============================================================================
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
#===============================================================================
# FUNCTIONS
#===============================================================================
"""
Create mask from vertices, then apply to input image
"""
def filter_region( img, vertices ):

    mask = np.zeros_like( img )

    # Condition for gray image (having only one channel )
    if( len( mask.shape ) == 2 ): cv.fillPoly( mask, vertices, 255 )

    # Condition for image with more than one channel
    else: cv.fillPoly( mask, vertices, ( 255, ) * mask.shape[2] )

    return( cv.bitwise_and( img, mask ) )
#-------------------------------------------------------------------------------
"""
Keep ROI surrounded by the vertices (i.e., polygon)
All other area is set to zero
"""
def select_region( img ):

    rows, cols = img.shape[ : 2 ]

    # Define polygon via vertices
    pnt_0 = [ cols * 0.30, rows * 0.90 ] # BL
    pnt_1 = [ cols * 0.30, rows * 0.08 ] # TL
    pnt_2 = [ cols * 0.90, rows * 0.08 ] # TR
    pnt_3 = [ cols * 0.90, rows * 0.90 ] # BR

    # Set vertices as array of point arrays
    vertices = np.array( [ [ pnt_0, pnt_1, pnt_2, pnt_3] ], dtype = np.int32 )
    #img = filter_region( img, vertices )
    #return( filter_region( img, vertices ) )
    y1 = int( rows * 0.07 ) 
    y2 = int( rows * 0.88 ) 

    x1 = int( cols * 0.31 ) 
    x2 = int( cols * 0.89 ) 

    img = img[  y1:y2, x1:x2]
    return( img )
#-------------------------------------------------------------------------------
"""
Create image pipeline to stream as video feed
"""
def camera_pipeline( img ):

    h, w = img.shape[ : 2 ]
    dsize = ( w, h )
    img = cv.warpPerspective( img, m, dsize )
    img = cv.undistort( img, mtx, dist, None, mtx )
    roi = select_region( img ) # Get cropped img

    return( roi )
#-------------------------------------------------------------------------------
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
    print(gstreamer_pipeline(flip_method=0))
    cap = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)

    folder_path = "/home/sviatoslav/Desktop/ParkSmart/data/training_data/tmp/"
    prefix = "img_"
    suffix = ".JPG"
    index = 0#21

    if cap.isOpened():

        cv.namedWindow( "CSI Camera", cv.WINDOW_NORMAL )

        while cv.getWindowProperty("CSI Camera", 0) >= 0:

            ret_val, frame = cap.read()
            output_img = camera_pipeline(frame)
            cv.resizeWindow( "CSI Camera", (1280, 720 ) )
            #cv.resizeWindow( "CSI Camera", output_img.shape[ : 2 ] )
            cv.imshow("CSI Camera", output_img)

            keyCode = cv.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27: break
            elif keyCode == 32:
                img_path = folder_path + prefix + str( index ) + suffix
                cv.imwrite( img_path, output_img )  
                index = index + 1

        cap.release()
        cv.destroyAllWindows()
    else: print("Unable to open camera")

if __name__ == "__main__": show_camera()

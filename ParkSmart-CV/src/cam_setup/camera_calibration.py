# IMPORT_LIBRARIES
import numpy as np 
import cv2 as cv
import pickle       
import glob
import os

#===================================================================================================
# PART_1 -- CAMERA CALIBRATION
#===================================================================================================

# CURRENT_WORKING_DIR
CWD = "/home/sviatoslav/Desktop/ParkSmart"
data_path = CWD + '/data/pickle/camera_calibration_pickle.p' 
imgs_path = CWD + '/data/calibration_images/*.JPG'
test_path = CWD + '/data/calibration_images/img_0.JPG' 
final_img = CWD + '/data/calibration_images/result.JPG'

# CHESSBOARD_VERTICES
points_per_row = 8 # horizontal_vertices
points_per_col = 6 # vertical_vertices

# OBJECT_POINTS -- E.g.: (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
object_points = np.zeros( ( points_per_col * points_per_row, 3 ), np.float32 )
object_points[ : , : 2 ] = np.mgrid[ 0 : 8, 0 : 6 ].T.reshape( -1, 2 )

# OBJECT_POINTS_&_IMAGE_POINTS_ARRAYS
obj_points_arr = [] # 3D points in the real world space
img_points_arr = [] # 2D points in the image plane

# CHESSBOARD FINDER TERMINATION CRITERIA, CHESSBOARD SIZE, & IMAGE SIZE
termination_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01)
pattern_size = ( points_per_row, points_per_col ) # 8,6
#image_size = ( 1280, 720 ) # w, h
image_size = ( 3264, 2464 ) # w, h

#FINDING CHESSBOARD

# LOAD_IMAGES
images = glob.glob( imgs_path )

# READ_IMAGE_FRAMES -- get object & image point arrays via chessboard corners finder 
for fname in images:
  
  # convert image to an opencv readable format
  original = cv.imread( fname )
  gray_img = cv.cvtColor( original, cv.COLOR_BGR2GRAY )
  
  # FindCheassboardCorners -- ret bool is true iff board is found
  ret, corners = cv.findChessboardCorners( gray_img, (8,6), None )
  
  if ret == True: 
    obj_points_arr.append( object_points ) # store object points
    corners2 = cv.cornerSubPix( gray_img, corners, ( 11, 11 ), ( -1, -1 ), termination_criteria )
    img_points_arr.append( corners2 )      # store image points
  
  else:
    print("Removing: ", fname)
    os.remove( fname )
    
print(gray_img.shape)

# CALIBRATION -- returns the camera matrix, distortion coefficents, rotation & translation vectors
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera( obj_points_arr, img_points_arr, gray_img.shape[ : : -1 ], None, None )

#===================================================================================================
# PART_2 -- UNDISTORTION TESTING
#===================================================================================================

img = cv.imread( test_path )
h, w = img.shape[ : 2 ]

# Refine img and return an img ROI that may be used for cropping img result
newCamMat, roi = cv.getOptimalNewCameraMatrix( mtx, dist, ( w, h ), 1, ( w, h ) )

#===================================================================================================
# PART_3 -- SAVING DATA
#===================================================================================================

dist_pickle = {}
dist_pickle[ 'roi' ] = roi 
dist_pickle[ 'mtx' ] = mtx
dist_pickle[ 'dist' ] = dist
dist_pickle[ 'newCamMat' ] = newCamMat
pickle.dump( dist_pickle, open( data_path, 'wb' ) )

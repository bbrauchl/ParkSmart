import numpy as np 
import cv2 as cv
import pickle       
import glob
import os

"""VARIABLE DECLARATIONS"""

# CURRENT_WORKING_DIR
CWD = "/home/sviatoslav/Desktop/ParkSmart"
img_warped = CWD + '/data/perspective_images/img_0.JPG'
img_target = CWD + '/data/perspective_images/img_1.JPG'
data_path = CWD + '/data/pickle/perspective_transform_pickle.p' 

# CHESSBOARD_VERTICES
points_per_row = 8 # horizontal_vertices
points_per_col = 6 # vertical_vertices

"""FINDING CHESSBOARD"""

# LOAD_IMAGES
src_img = cv.imread( img_warped )
dst_img = cv.imread( img_target )

ret1, corners1 = cv.findChessboardCorners( src_img, ( points_per_row, points_per_col ), None )
ret2, corners2 = cv.findChessboardCorners( dst_img, ( points_per_row, points_per_col ), None )

"""# Perspective Transform via homography matrix"""

# HOMOGRAPHY_ESTIMATION
M, homography_matrix = cv.findHomography( corners1, corners2 )

# STORE HOMOGRAPHY MATRIX M
dist_pickle = {}
dist_pickle[ 'M' ] = M 
pickle.dump( dist_pickle, open( data_path, 'wb' ) )

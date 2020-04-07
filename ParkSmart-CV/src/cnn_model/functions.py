import os
import pickle
import cv2 as cv
import numpy as np
from threading import Event, Thread, _after_fork

import sys
sys.path.insert(0, "/home/rory/Desktop/ParkSmart/web-dev/demos/")
import ParkSmart

CWD = "/home/rory/Desktop/ParkSmart"

predictions_file_path_global = CWD + '/predictions.p'
camera_data_path_global = CWD + '/data/pickle/camera_calibration_pickle.p'
homography_data_path_global = CWD + '/data/pickle/perspective_transform_pickle.p'
parking_space_dictionary_path_global = CWD + '/data/pickle/parking_spaces_pickle.p'

clean_lot_image_path_global = CWD + '/data/test_images/test_img_.0001.JPG'

g_streamer_string = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
#========================================================================================================
# THREADS
#========================================================================================================

def crop_spaces( cluster_img, cluster, buffer = 50 ):
	img_list = [ [] for i in range( len( cluster ) ) ]

	i = 0
	for spot in cluster:
		location = cluster.get( spot )
		x1, y1, x2, y2 = location
		y1 = y1 - buffer
		y2 = y2 + buffer
		if( y1 < 0 ): y1 = 0
		img_list[ i ] = cluster_img[ y1 : y2, x1 : x2 ]
		i += 1

	return( img_list )

# Get individual images with buffer included from crop fn
def parse_full_img( img, parking_space_dictionary, vertices ):

	dst_img_list = [ [] for i in range( len( parking_space_dictionary ) ) ]
	src_img_list = get_segmented_images( img, vertices )
	for i in range( 0, 4 ):
		cluster_str = 'Cluster_{}'.format( str( i ) )
		cluster = parking_space_dictionary.get( cluster_str )
		dst_img_list[ i ] = crop_spaces( src_img_list[ i ], cluster )

	return( dst_img_list )

def get_segmented_images( img, vertices ):

	img_list = [ [], [], [], [] ]
	for i in range( 3, -1, -1 ):

		x1 = vertices[ i ][ 0 ][ 0 ]
		x2 = vertices[ i ][ 2 ][ 0 ]
		y2 = vertices[ i ][ 0 ][ 1 ]
		y1 = vertices[ i ][ 1 ][ 1 ]
		h = abs( y1 - y2 )
		w = abs( x1 - x2 )

		segmented_img = img[ y1:y1+h, x1:x1+w ]

		# Rotate segmented image is it is the bottom cluster ( w/ handicap spaces )
		if( i == 3 ): segmented_img = cv.rotate( segmented_img, cv.ROTATE_90_COUNTERCLOCKWISE )
		img_list[ i ] = segmented_img

	return( img_list )

def load_clean_lot_cluster_images( vertices ):
	img_data = cv.imread( clean_lot_image_path_global )
	cluster_images = get_segmented_images( img_data, vertices )
	return( cluster_images )

def get_scaled_cluster_dimensions( cluster_images, scale_factor = 4 ):
	shapes = []
	for i in range( 0, 4 ):
		shape = cluster_images[ i ].shape[ : 2 ]
		if( i != 3 ): shapes.append( ( shape[ 1 ] // scale_factor, shape[ 0 ] // scale_factor, ) )
		else: shapes.append( ( shape[ 0 ] // scale_factor, shape[ 1 ] // scale_factor, ) )
	return( shapes )

#========================================================================================================
# LOAD PICKED FILES
#========================================================================================================
def load_camera_calibration_data():

    with open( camera_data_path_global, mode = 'rb' ) as f: 		# LOAD CAM CALIBRATION MATRICES
    	file = pickle.load( f )
    	mtx = file[ 'mtx' ]
    	dist = file[ 'dist' ]
    	f.close()

    return( mtx, dist )

def load_perspective_transformation_data():

    with open( homography_data_path_global, mode = 'rb' ) as f:		# LOAD PERSPECTIVE TRANSFORM MAT
    	file = pickle.load( f )
    	m = file[ 'M' ]
    	f.close()

    return( m )

def convert_dictionary( parking_space_dictionary ):

	return( new_dictionary )

def load_parking_space_dictionary():

    with open( parking_space_dictionary_path_global, mode = 'rb' ) as f: 	# LOAD PARKING SPACE DICTIONARY
    	file = pickle.load( f )
    	parking_space_dictionary = file[ 'parking_space_dictionary' ]
    	vertices = file[ 'vertices' ]
    	f.close()

    return( parking_space_dictionary, vertices )
#========================================================================================================
# PREDICTIONS FILE AND PREDCITIONS DICTIONARY
#========================================================================================================

# Create predictions dictionary ( containing key : value pairs )
def create_predictions_dictionary():

	predictions_dictionary = {}
	spot_count = [ 17, 28, 28, 11 ] # index 0 - 16, 0 - 13, 0 - 13, 0 - 15

	for i in range( len( spot_count ) ):
		spots = {}

		for x in range( spot_count[ i ] ):

			spots[ 'Spot_{}'.format( x ) ] = 0

		predictions_dictionary[ 'Cluster_{}'.format( i ) ] = spots

	#update_predictions_file( predictions_dictionary ) # Initialize empty predictions file every time
	pickle.dump( predictions_dictionary, open( predictions_file_path_global, 'wb' ) )

	return( predictions_dictionary )

def update_predictions_dictionary( predictions_dictionary, predictions_arr, cluster_index ):

	cluster_string = 'Cluster_{}'.format( cluster_index )
	for i in range( len( predictions_arr ) ):
		spot_string = 'Spot_{}'.format( i )
		predictions_dictionary[ cluster_string ][ spot_string ] = predictions_arr[ i ]

def update_predictions_server( predictions_arr, predictions_server_event, terminate_event ):

	lot_key = 'Lot'
	lot_item = 'Lot_D'
	space_key = 'Space'
	space_item = 0
	classification_key = 'IsOccupied'
	classification_item = True
	prediction_key = 'Confidence'
	prediction_item = 0.99
	type_key = 'Type'
	type_item_ev = 'electric_vehicle' 
	type_item_hc = 'handicap' 
	type_item_st = 'student'
	tmp_dict = { lot_key : lot_item, space_key : space_item, classification_key : classification_item, prediction_key : prediction_item, type_key : type_item_st } 
	
	update_item = []
	cluster_row_length = [ 17, 28, 28, 11 ] 
	map_middle_clusters = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,1,3,5,7,9,11,13,15,17,19,21,23,25,27]
	

	while( not terminate_event.isSet() ):

		space_count = 0
		update_item = []
		predictions_server_event.wait()                      

		print( "Updating server file..." )

		for i in range( len( cluster_row_length ) ):
			for j in range( cluster_row_length[ i ] ):

				if( i == 1 or i == 2 ): 
					mapped_index = map_middle_clusters[ j ]
					prediction = predictions_arr[ i ][ mapped_index ][ 0 ]
				elif( i == 3 ): prediction = predictions_arr[ i ][ - ( j + 1 ) ][ 0 ]
				else: prediction = predictions_arr[ i ][ j ][ 0 ]

				# If prediction is near zero -- classified as open / empty spot
				if( prediction > 0.5 ): classification = False	
				else: classification = True	

				update_item.append( {
				     'Lot': 'Lot_D',
				     'Space': int( space_count ),
				     'IsOccupied': bool( classification ),
				     'Confidence': float( prediction ), 
				     'Type': 'electric_vehicle' if space_count in range(0,4) else 'handicap' if space_count in range(73, 80) else 'student',
				} )
				space_count += int( 1 )

		ParkSmart.update_multi(update_item)
		predictions_server_event.clear()

def update_predictions_file( predictions_dictionary, file_update_event, terminate_event ):

	while( not terminate_event.isSet() ):

		file_update_event.wait()                      # wait (blocking)
		pickle.dump( predictions_dictionary, open( predictions_file_path_global, 'wb' ) )
		print( "\nTHREAD EVENT: Predictions file has been updated..." )
		file_update_event.clear()
#========================================================================================================
# CAMERA PIPELINES
#========================================================================================================
# Keep ROI surrounded by the vertices (i.e., polygon)
def select_region( img, rows, cols ):
	y1 = int( rows * 0.07 )
	y2 = int( rows * 0.88 )
	x1 = int( cols * 0.31 )
	x2 = int( cols * 0.89 )
	return( img[ y1 : y2, x1 : x2 ] )

# Create image pipeline to stream as video feed
def camera_pipeline( input_frame, mtx, dist, m ):
	h, w = input_frame.shape[ : 2 ]
	img  = cv.warpPerspective( input_frame, m, ( w, h ) )
	img  = cv.undistort( img, mtx, dist, None, mtx )
	roi  = select_region( img, h, w )
	return( roi )


#========================================================================================================
# PRIMARILY OPECN CV FUNCTIONS
#========================================================================================================
def init_windows( clean_cluster_images, scaled_cluster_shapes  ):

	window_display_handles = [ 'Cluster_0', 'Cluster_1', 'Cluster_2', 'Cluster_3' ]

	for i in range( 0, 4 ):
		cv.namedWindow( window_display_handles[ i ], cv.WINDOW_NORMAL )
		cv.resizeWindow( window_display_handles[ i ], scaled_cluster_shapes[ i ] )

		if( i != 3 ): cv.imshow( window_display_handles[ i ], clean_cluster_images[ i ] )
		else: cv.imshow( window_display_handles[ i ], np.rot90( clean_cluster_images[ i ], k = -1 ) )

	return( window_display_handles )

def update_cluster_window( window_image, window_display_handle, cluster_index, cluster_window_event, terminate_event ):

	while( not terminate_event.isSet() ):
		cluster_window_event.wait()                      
		if( cluster_index != 3 ): cv.imshow( window_display_handle, window_image )
		else: cv.imshow( window_display_handle, np.rot90( window_image, k = -1 ) )
		cluster_window_event.clear()

def update_windows( window_image, window_display_handles, window_index ):

	if( window_index != 3 ): cv.imshow( window_display_handles[ window_index ], window_image )
	else: cv.imshow( window_display_handles[ window_index ], np.rot90( window_image, k = -1 ) )

def bgr2rgb( img ):
	return( cv.cvtColor( img, cv.COLOR_BGR2RGB ) )

def terminate_camera( camera ):
	print( "Exiting Program..." )
	cv.destroyAllWindows()
	camera.release()

def init_camera():
	camera = cv.VideoCapture( gstreamer_pipeline(), cv.CAP_GSTREAMER )     
	return( camera )

#===============================================================================
# G STREAMER PIPELINE
#===============================================================================
def gstreamer_pipeline( capture_width=3264, capture_height=2464, display_width=3264, display_height=2464, framerate=21, flip_method=0 ):
	return( g_streamer_string % ( capture_width, capture_height, framerate, flip_method, display_width, display_height ) )

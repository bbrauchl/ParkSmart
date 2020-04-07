#========================================================================================================
# IMPORT_LIBRARIES
#========================================================================================================
import os
import time
import pickle
import warnings
import cv2 as cv
import numpy as np

#warnings.filterwarnings( 'ignore' )
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from threading import Event, Thread, _after_fork

from functions import load_parking_space_dictionary, load_clean_lot_cluster_images
from functions import load_camera_calibration_data, load_perspective_transformation_data
from functions import update_predictions_file, update_cluster_window, update_predictions_server
from functions import init_camera, init_windows, camera_pipeline, terminate_camera, update_windows
from functions import create_predictions_dictionary, parse_full_img, get_scaled_cluster_dimensions

#========================================================================================================
import tensorflow as tf

tf.keras.backend.clear_session()		# Clear any previous session
tf.keras.backend.set_learning_phase(0)
tf.compat.v1.disable_eager_execution()

from tensorflow.keras.models import load_model
from tensorflow.compat.v1.keras.backend import set_session

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction=0.5
session = tf.compat.v1.Session( config = config )
set_session( session )
#========================================================================================================
def load_trained_model():
	model = load_model( "/home/rory/Desktop/ParkSmart/data/model/model.h5" )
	return( model )

def update_cluster_predictions( model, cluster_images, predictions_dictionary, cluster_index ):

	index = 0
	confidence = []
	predictions = []
	cluster_image = cluster_images[ cluster_index ]
	cluster_string = 'Cluster_{}'.format( cluster_index )

	for spot in predictions_dictionary[ cluster_string ]:

		img_data = cv.resize( cluster_image[ index ], ( 64, 64 ) )
		prediction = model.predict( img_data[ None, :, :, : ] )[ 0 ]
		predictions.append( np.argmax( prediction ) )
		confidence.append( prediction )

		predictions_dictionary[ cluster_string ][ spot ] = predictions[ index ]
		index += 1

	return( predictions, confidence )

def update_animated_lot_image( segmented_lot_images, predictions_arr, parking_space_dictionary, cluster_index ):

	trim = 5
	red = [ 0, 0, 255 ]
	blue = [ 255, 0, 0 ]
	green = [ 0, 255, 0 ]
	cluster_string = 'Cluster_{}'.format( cluster_index )

	for i in range( len( predictions_arr ) ):

		rectangle = parking_space_dictionary[ cluster_string ][ 'ParkingSpace_ID_{}'.format( i ) ]
		prediction = predictions_arr[ i ]

		pt1 = ( rectangle[ 0 ] + trim, rectangle[ 1 ] + trim )
		pt2 = ( rectangle[ 2 ] - trim, rectangle[ 3 ] - trim )

		if( prediction == 0 ): color = green
		else: color = red
	
		cv.rectangle( segmented_lot_images[ cluster_index ], pt1 = pt1, pt2 = pt2, color = color, thickness = cv.FILLED )
		cv.rectangle( segmented_lot_images[ cluster_index ], pt1 = pt1, pt2 = pt2, color = blue, thickness = 10 )

def run_predictions_file_thread( threads, predictions_dictionary, terminate_event ):

	predictions_file_event = Event()
	threads.append( Thread( target = update_predictions_file, args = ( predictions_dictionary, predictions_file_event, terminate_event, ) ) )
	threads[ -1 ].start()

	print( "\nPredictions file thread is ready.")
	return( predictions_file_event )

def run_predictions_server_thread( threads, confidence_arr, terminate_event ):

	predictions_server_event = Event()
	threads.append( Thread( target = update_predictions_server, args = ( confidence_arr, predictions_server_event, terminate_event, ) ) )
	threads[ -1 ].start()

	print( "\nPredictions file thread is ready.")
	return( predictions_server_event )

def run_cluster_window_threads( threads, cluster_img, window_display_handle, terminate_event ):

	cluster_event_arr = []

	for i in range( 4 ):
		cluster_event = Event()
		threads.append( Thread( target = update_cluster_window, args = ( cluster_img[ i ], window_display_handle[ i ], i, cluster_event, terminate_event, ) ) )
		cluster_event_arr.append( cluster_event )
		threads[ -1 ].start()

	print( "\nCluster display window threads are ready.")
	return( cluster_event_arr )

def join_threads( threads, terminate_event ):

	terminate_event.set()

	print( "Joining threads..." )
	for thread in threads:
		thread.join( timeout = 0.01 )
		thread._delete()
	_after_fork()
	print( "Threads are joined." )

def init_shutdown( camera, threads, terminate_event ):

	print( "\nInitiating shutdown procedure..." )
	join_threads( threads, terminate_event )
	terminate_camera( camera )
	session.close()

#========================================================================================================
# MAIN FUNCTION 
#========================================================================================================

def cnn_pipeline():

	#-----------------------------------------------------------------------------------------------

	frame = []	
	threads = []
	confidences = [[],[],[],[]] #,,,
	frame_rate = 10
	initial_time = 0
	cluster_index = 0
	terminate_event = Event()						

	print( "\nInitializing CNN..." )
	model = load_trained_model()						# Load trained CNN model

	print( "\nInitializing camera matrices..." )
	m = load_perspective_transformation_data()				# Load perspective mat
	mtx, dist = load_camera_calibration_data()				# Load cam cal matrices
	parking_space_dictionary, vertices = load_parking_space_dictionary()	# Get parking space dict

	print( "\nInitializing predictions dictionary and file..." )
	predictions_dictionary = create_predictions_dictionary()           	# Empty predictions dict

	print( "\nInitializing clean cluster images of parkinglot..." )
	clean_cluster_images = load_clean_lot_cluster_images( vertices )	
	scaled_cluster_shapes = get_scaled_cluster_dimensions( clean_cluster_images )  

	print( "\nInitializing windows to display parking lot clusters..." )
	window_display_handles = init_windows( clean_cluster_images, scaled_cluster_shapes )	

	print( "\nInitializing worker threads to manage display windows and file udpates..." )
	predictions_file_event = run_predictions_file_thread( threads, predictions_dictionary, terminate_event )
	predictions_server_event = run_predictions_server_thread( threads, confidences, terminate_event )

	cluster_event_arr = run_cluster_window_threads( threads, clean_cluster_images, window_display_handles, terminate_event )

	camera = init_camera()
	if camera.isOpened():

	#-----------------------------------------------------------------------------------------------

		print( "\nProgram is ready, press 'r' to execute." )
		while( ( cv.waitKey( 30 ) & 0xFF ) != ord( 'r' ) ): None 	# Busy waiting

		print( "\nProgram is now executing..." )
		while( True ):

			cluster_index = np.mod( cluster_index, 5 )
			#-------------------------------------------------------------------------------
			ret_val, frame = camera.read()
			output_frame = camera_pipeline( frame, mtx, dist, m )
			cluster_images = parse_full_img( output_frame, parking_space_dictionary, vertices ) 	
			#-------------------------------------------------------------------------------
			if( cluster_index < 4 ):
				predictions_arr, confidences[ cluster_index ] = update_cluster_predictions( model, cluster_images, predictions_dictionary, cluster_index )      
				update_animated_lot_image( clean_cluster_images, predictions_arr, parking_space_dictionary, cluster_index )
				cluster_event_arr[ cluster_index ].set()
				print( 'Updating cluster: {}'.format( cluster_index ) )
			#-------------------------------------------------------------------------------
			if( cluster_index == 4 ): 
				#predictions_file_event.set() 	# Update prediction file 
				predictions_server_event.set()
			if( (  cv.waitKey( 1 ) & 0xFF ) == 27 ): break  	# ESC key to stop
			cluster_index += 1

	#-----------------------------------------------------------------------------------------------

	else: print("Unable to open camera")
	init_shutdown( camera, threads, terminate_event )
#========================================================================================================
if __name__ == "__main__": cnn_pipeline()
#========================================================================================================

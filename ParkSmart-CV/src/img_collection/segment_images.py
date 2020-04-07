#===============================================================================
# IMPORT_LIBRARIES
#===============================================================================
#import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import operator
import pickle
import glob
import time
import os

#from skimage.transform  import resize

#===============================================================================
# VARIABLE_DECLARATIONS
#===============================================================================
CWD = "/home/sviatoslav/Desktop/ParkSmart"
parking_space_pickle_path_global = CWD + '/data/pickle/parking_spaces_pickle.p' 
src_images_path_global = CWD + '/data/training_data/tmp'  
dst_images_path_global = CWD + '/data/training_data'  

"""
LOAD_PICKLED_DATA
"""
with open( parking_space_pickle_path_global, mode = 'rb' ) as f: 

    file = pickle.load( f )

    parking_space_dictionary = file[ 'parking_space_dictionary' ]
    vertices = file[ 'vertices' ] 
#===============================================================================
# FUNCTIONS
#===============================================================================
def rotate( img, ccw = False ):
    if( ccw == True ): return( cv.rotate( img, cv.ROTATE_90_COUNTERCLOCKWISE ) )
    else: return( cv.rotate( img, cv.ROTATE_90_CLOCKWISE ) )

def get_segmented_images( img, vertices, cluster_count = 4 ):

    img_list = [ img, img, img, img ]
    for i in range( 3, -1, -1 ):

        x1 = vertices[ i ][ 0 ][ 0 ]
        x2 = vertices[ i ][ 2 ][ 0 ]
        y2 = vertices[ i ][ 0 ][ 1 ]
        y1 = vertices[ i ][ 1 ][ 1 ]
        h = abs( y1 - y2 )
        w = abs( x1 - x2 )

        segmented_img = img[ y1:y1+h, x1:x1+w ] 

        # Rotate segmented image is it is the bottom cluster ( w/ handicap spaces )
        if( i == 3 ): segmented_img = rotate( segmented_img, True )
        img_list[ i ] = segmented_img

    return( img_list )
#-------------------------------------------------------------------------------
def crop_spaces( cluster_img, cluster, buffer = 50 ):
    img_list = [ [] for i in range( len( cluster ) ) ]

    i = 0
    for spot in cluster:
        location = cluster.get( spot )
        x1, y1, x2, y2 = location
        y1 = y1 - buffer
        if( y1 < 0 ): y1 = 0
        y2 = y2 + buffer
        img_list[ i ] = cluster_img[ y1 : y2, x1 : x2 ]
        i += 1

    return( img_list )
#-------------------------------------------------------------------------------
def save_imgs( imgs, dir_path, cluster3 = False ):

    dir_path_handicap = dir_path + '/handicap/'
    dir_path_regular = dir_path + '/regular/'

    i = 0
    if( cluster3 == False ):
        """
        if( os.path.isdir( dir_path_regular ) == True ): 

            sorted_list = os.listdir( dir_path_regular )
            sorted_list.sort()
            count = len( sorted_list )
            images = len( imgs )
            #print( count )
            #print( images )

            for i in range( images ):

                num = str( i + count ).zfill( 4 ) # CHANGE EVERY TIME !!!!!!!!!!


                filename = dir_path_regular + 'img_' + num + '.JPG'

                img = cv.resize( imgs[ i ], ( 200, 200 ) )
                #img = resize( imgs[ i ], ( 200, 200 ) )
                print( "Image #{:3}:".format( str( i ) ), filename, '\t shape: ', img.shape )
                cv.imwrite( filename, img )
                #plt.imsave( filename, img )"""
    
    # Otherwise seperate handicap spaces and place in seperate folder
    else:
        imgs_regular =  [ imgs[i] for i in range( 0, 4 ) ]
        imgs_handicap =  [ imgs[i] for i in range( 4, 11 ) ]
        """
        if( os.path.isdir( dir_path_regular ) == True ): 

            sorted_list = os.listdir( dir_path_regular )
            sorted_list.sort()
            count = len( sorted_list )
            images = len( imgs_regular )
            #print( count )
            #print( images )

            for i in range( images ):

                num = str( i + count ).zfill( 4 ) # CHANGE EVERY TIME !!!!!!!!!!


                filename = dir_path_regular + 'img_' + num + '.JPG'

                img = cv.resize( imgs_regular[ i ], ( 200, 200 ) )
                #img = resize( imgs_regular[ i ], ( 200, 200 ) )
                print( "Image #{:3}:".format( str( i ) ), filename, '\t shape: ', img.shape )
                cv.imwrite( filename, img )
                #plt.imsave( filename, img )
        """
        if( os.path.isdir( dir_path_handicap ) == True ): 

            sorted_list = os.listdir( dir_path_handicap )
            sorted_list.sort()
            count = len( sorted_list )
            images = len( imgs_handicap )
            #print( count )
            #print( images )

            for i in range( images ):

                num = str( i + count ).zfill( 4 ) # CHANGE EVERY TIME !!!!!!!!!!


                filename = dir_path_handicap + 'img_' + num + '.JPG'

                img = cv.resize( imgs_handicap[ i ], ( 200, 200 ) )
                #img = resize( imgs_handicap[ i ], ( 200, 200 ) )
                print( "Image #{:3}:".format( str( i ) ), filename, '\t shape: ', img.shape )
                cv.imwrite( filename, img )
                #plt.imsave( filename, img )
#-------------------------------------------------------------------------------
def parse_full_img( img, vertices, parking_space_dictionary, dir_path ):

    img_list = get_segmented_images( img, vertices )
    cluster3 = False
    for i in range( 0, 4 ):
        cluster_str = 'Cluster_{}'.format( str( i ) )
        cluster = parking_space_dictionary.get( cluster_str )
        #print( cluster_str )
        imgs = crop_spaces( img_list[ i ], cluster )

        if( i == 3 ): cluster3 = True
        save_imgs( imgs, dir_path, cluster3 )
#===============================================================================
def parse_image_folder( src_folder, dst_folder, vertices, parking_space_dictionary ):
        if( os.path.isdir( src_folder ) == True ): 

            sorted_list = os.listdir( src_folder )
            sorted_list.sort()
            i = 0

            for( filename ) in sorted_list:
                src = src_folder + '/' + filename
                print( src )

                if( os.path.isfile( src ) == True ):

                    img = cv.imread( src, cv.COLOR_BGR2RGB )
                    #img = plt.imread( src )
                    parse_full_img( img, vertices, parking_space_dictionary, dst_folder )
                    print( 'File {} Completed.'.format( str( filename ) ) )
#===============================================================================
def main():

    parse_image_folder( src_images_path_global, dst_images_path_global, vertices, parking_space_dictionary )

if __name__ == "__main__": main()

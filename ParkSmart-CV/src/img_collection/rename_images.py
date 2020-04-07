#===============================================================================
# IMPORT_LIBRARIES
#===============================================================================
import os                          # dealing with directories
import cv2 as cv                   # dealing with images
import numpy as np                 # dealing with arrays
#===============================================================================
# VARIABLE_DECLARATIONS
#===============================================================================
CWD = "/home/sviatoslav/Desktop/ParkSmart"
#===============================================================================
# FUNCTION_DEFINITIONS
#===============================================================================
"""
Function to rename image files for easier parsing 
"""
def rename_img_files( img_dir, img_base_name ):

  list_dir_seg = np.array( os.listdir( img_dir ) )

  i = 0
  for filename in list_dir_seg:
    
    index_str = str( i ).zfill( 4 )
    dst = img_base_name + '.' + index_str + ".JPG"
    src = img_dir + "/" + filename
    dst = img_dir + "/" + dst
    
    os.rename( src, dst )
    i += 1
#===============================================================================
# RENAMING_FILES
#===============================================================================
test_img_path = CWD + '/data/test_images'
rename_img_files( test_img_path, 'test_img_' )

test_img_path = CWD + '/data/training_data/old_tmp'
rename_img_files( test_img_path, 'tmp_img_' )

test_img_path = CWD + '/data/training_data/handicap/vacant'
rename_img_files( test_img_path, 'vacant_handicap_' )

test_img_path = CWD + '/data/training_data/handicap/occupied'
rename_img_files( test_img_path, 'occupied_handicap_' )

test_img_path = CWD + '/data/training_data/regular/vacant'
rename_img_files( test_img_path, 'vacant_regular_' )

test_img_path = CWD + '/data/training_data/regular/occupied'
rename_img_files( test_img_path, 'occupied_regular_' )
#===============================================================================

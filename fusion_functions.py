import h5py
import numpy as np
from tifffile import imwrite, imread, tiffcomment, TiffFile
from ome_types import from_tiff
from glob import glob
import os
import affine_matrices as affine
from scipy.ndimage import affine_transform
from timeit import default_timer as timer
from npy2bdv import BdvWriter
from napari import Viewer
import lxml
from datetime import datetime
import pyimagej as imagej
import scyjava

def deskew_views_separately():
    """deskew views with pyimagej and bigstitcher"""

def get_imagej_instance(memory_gb=60):
    scyjava.config.add_option('-Xmx{memory_gb}g')
    ij = imagej.init('sc.fiji:fiji:2.14.0')
    return ij

def run_reslicing_view_macro():
    macro = """
    #@ String name
    #@ int age
    #@ String city
    #@output Object greeting
    greeting = "Hello " + name + ". You are " + age + " years old, and live in " + city + "."
    """
    args = {
        'name': 'Chuckles',
        'age': 13,
        'city': 'Nowhere'
    }
    result = ij.py.run_macro(macro, args)
    print(result.getOutput('greeting'))

    """
    run("Image Fusion", 
    "browse=A:/leo/micromanager/bone_marrow_2nd/aml/data/deskewed_20250119-160952/pos_p0000/dataset.xml 
    select=A:/leo/micromanager/bone_marrow_2nd/aml/data/deskewed_20250119-160952/pos_p0000//dataset.xml 
    process_angle=[All angles] 
    process_channel=[All channels] 
    process_illumination=[All illuminations] 
    process_tile=[All tiles] 
    process_timepoint=[All Timepoints] 
    bounding_box=[Currently Selected Views] 
    downsampling=1 
    interpolation=[Linear Interpolation] 
    fusion_type=[Avg, Blending] 
    pixel_type=[16-bit unsigned integer] 
    interest_points_for_non_rigid=[-= Disable Non-Rigid =-] 
    produce=[Each timepoint & channel] 
    fused_image=[Display using ImageJ] 
    define_input=[Auto-load from input data (values shown below)] 
    display=[precomputed (fast, complete copy in memory before display)] 
    min_intensity=0 
    max_intensity=255");

    run("Image Fusion", "select=A:/leo/micromanager/bone_marrow_2nd/aml/data/deskewed_20250122-174424/pos_p0000//dataset.xml process_angle=[All angles] process_channel=[All channels] process_illumination=[All illuminations] process_tile=[All tiles] process_timepoint=[All Timepoints] bounding_box=[Currently Selected Views] downsampling=4 interpolation=[Linear Interpolation] fusion_type=[Avg, Blending] pixel_type=[16-bit unsigned integer] interest_points_for_non_rigid=[-= Disable Non-Rigid =-] produce=[Each timepoint & channel] fused_image=[Save as (compressed) TIFF stacks] define_input=[Auto-load from input data (values shown below)] output_file_directory=A:/leo/micromanager/bone_marrow_2nd/aml/data/deskewed_20250122-174424/pos_p0000 filename_addition=[]");

    produce=[Each view]

    """
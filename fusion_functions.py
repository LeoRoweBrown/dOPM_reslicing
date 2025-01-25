import h5py
import numpy as np
from tifffile import imwrite, imread, tiffcomment, TiffFile
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
    pass

def get_imagej_instance(memory_gb=60, 
                        imagej_dir="A:/leo_imagej/fiji-win64/fiji-win64/Fiji.app", 
                        download_imagej=False,
                        imagej_mode='interactive',
                        imagej_download_options = ['sc.fiji:fiji:2.14.0', 
                                                   'net.preibisch:BigStitcher:2.2.1']):
    scyjava.config.add_option(f"-Xmx{memory_gb}g")

    if 'ij' not in globals():
        if download_imagej:
            print("Downloading ImageJ")
            ij = imagej.init(imagej_download_options, mode=imagej_mode)
        elif imagej_dir is not None:
            print(f"Opening ImageJ from {imagej_dir}")
            ij = imagej.init(imagej_dir, mode='interactive')
        else:
            raise FileNotFoundError("No imageJ dir given, use download ImageJ=True")
        print("Created ImageJ instance", ij.getVersion()) 
    else:
        print(f"ImageJ instance already exists ({ij.getVersion()})")
    return ij

def deskew_and_save_tiffs(bdv_dir, save_dir, pattern='pos_*', separate_dirs=False):
    ij = get_imagej_instance()
    bdv_dirs = glob.glob(os.path.join(bdv_dir, pattern))
    
    for bdv in bdv_dirs:
        dataset_xml_path = os.path.join(bdv, "dataset.xml")
        print(f"reslicing data in {dataset_xml_path}")
        filename_addition = os.path.basename(dataset_xml_path)
        save_path = save_dir
        if separate_dirs:
            save_path = os.path.join(save_dir, filename_addition)
        os.makedirs(save_path, exist_ok=True)
        run_image_fusion_macro(ij, dataset_xml_path, save_dir, filename_addition=filename_addition)
        
def run_image_fusion_macro(ij, in_dir, out_dir,
                           filename_addition="",
                           downscale=4,
                           save_fused=False,
                           fusion_type="[Avg, Blending]",
                           view='both'):
    # Define the parameters
    if not save_fused:
        produce = "[Each view]"
    else:
        produce = "[Each timepoint & channel]"

    if view == 'both':
        angles = "[All angles]"
    elif str(view) == '0':
        angles = "[angle 0]"
    elif str(view) == '90':
        angles = "[angle 90]"
        
    params = {
        "select": in_dir,
        "process_angle": angles,
        "process_channel": "[All channels]",
        "process_illumination": "[All illuminations]",
        "process_tile": "[All tiles]",
        "process_timepoint": "[All Timepoints]",
        "bounding_box": "[Currently Selected Views]",
        "downsampling": str(downscale),
        "interpolation": "[Linear Interpolation]",
        "fusion_type": fusion_type,
        "pixel_type": "[16-bit unsigned integer]",
        "interest_points_for_non_rigid": "[-= Disable Non-Rigid =-]",
        "produce": produce,
        "fused_image": "[Save as (compressed) TIFF stacks]",
        "define_input": "[Auto-load from input data (values shown below)]",
        "output_file_directory": out_dir,
        "filename_addition": f"[{filename_addition}_]"
    }
        
    # Run the Image Fusion command with the parameters
    result = ij.py.run_plugin("Image Fusion", params)

 
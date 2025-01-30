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
import subprocess

def deskew_views_separately():
    """deskew views with pyimagej and bigstitcher"""
    pass

def deskew_bdv_and_save_tiffs(bdv_dir, save_dir, pattern='pos_*',
                              separate_dirs=False,
                              imagej_dir="C:/Users/lnr19/fiji-win64/Fiji.app"):
    if imagej_instance is None:
        ij = get_imagej_instance(imagej_download_options)
    else:
        ij = imagej_instance
        
    bdv_dirs = glob(os.path.join(bdv_dir, pattern))
    
    for bdv in bdv_dirs:
        dataset_xml_path = os.path.join(bdv, "dataset.xml")
        print(f"reslicing data in {dataset_xml_path}")
        filename_addition = os.path.basename(dataset_xml_path)
        save_path = save_dir
        if separate_dirs:
            save_path = os.path.join(save_dir, filename_addition)
        os.makedirs(save_path, exist_ok=True)
        run_image_fusion_macro(ij, dataset_xml_path, save_dir, filename_addition=filename_addition)
        
def run_image_fusion_macro(in_dir, out_dir, imagej_dir,
                           filename_addition="",
                           downscale=4,
                           save_fused=False,
                           fusion_type="[Avg, Blending]",
                           view='both',
                           correct_voxel_dims=True):

    xml_path = os.path.join(in_dir, "dataset.xml")

    # Build (windows) command
    # first build param list
    params = "["+
            f"xml_path={xml_path} " +
            f"out_dir={out_dir} " +
            f"downscale={downscale} " +
            f"fusion_method={fusion_method} " +
            f"view={view} " +
            f"filename_addition={filename_addition}" +
            "]"

    imagej_exe = os.path.join(imagej_dir, "ImageJ-win64.exe")
    macro_path = "imagej_macros/image_fusion.ijm"
    command = imagej_exe + " " + macro_path + params

    print("Running command: " + command)
    subprocess.run(command)
 
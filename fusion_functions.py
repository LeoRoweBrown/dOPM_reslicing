import h5py
import numpy as np
from tifffile import imwrite, imread, tiffcomment, TiffFile
from glob import glob
import os
import affine_matrices as affine
from scipy.ndimage import affine_transform
from timeit import default_timer as timer
from npy2bdv import BdvWriter, BdvEditor
from napari import Viewer
import lxml
from datetime import datetime
import subprocess

def deskew_views_separately():
    """deskew views with pyimagej and bigstitcher"""
    pass

def deskew_bdv_and_save_tiffs(bdv_dir, save_dir, pattern='pos_*',
                              separate_dirs=False, opm_angle=45, 
                              imagej_dir="C:/Users/lnr19/fiji-win64/Fiji.app",
                              stop_at_index=np.inf, start_at_index=0,
                              **kwargs):
    
    bdv_dirs = glob(os.path.join(bdv_dir, pattern))
    print("found BDV dataset folders: \n", bdv_dirs)

    for n, bdv in enumerate(bdv_dirs):
        if n < start_at_index:
            continue
        if n >= stop_at_index:
            print("Stopping at", n);
            break
        dataset_xml_path = os.path.join(bdv, "dataset.xml")
        print(f"reslicing data in {dataset_xml_path}")
        filename_addition = os.path.basename(bdv)
        print(filename_addition)
        save_path = save_dir
        if separate_dirs:
            save_path = os.path.join(save_dir, filename_addition)
        os.makedirs(save_path, exist_ok=True)
        run_image_fusion_macro(dataset_xml_path, save_dir, imagej_dir, 
                               filename_addition=filename_addition, **kwargs)
        
def run_image_fusion_macro(xml_path, out_dir, imagej_dir,
                           filename_addition="",
                           downscale=4,
                           save_fused=False,
                           fusion_method="[Avg, Blending]",
                           view='both',
                           correct_voxel_dims=True,
                           headless=False,
                           opm_angle=45,
                           save_method="[Save as (compressed) TIFF stacks]",
                           legacy=True):

    if headless:  # headless currently is broken and macro doesnt close. gotta use gui
        headless_str = "--headless"
    else:
        headless_str = ""
    
    if legacy:
        save_fused = 'false'
    else:
        save_fused = 'true'

    # for the fused case where we run the command once, put these into 1 length lists
    filename_addition_views = [filename_addition]
    views = [view]
    
    if not save_fused:
        bdv_xml = BdvEditor(xml_path)

        ## if you choose to reslice both views but separately (NO FUSION) and there are indeed two views
        if view == 'both': 
            if bdv_xml.nangles == 1:  # this might fall apart if somehow there's a "view 2" only?
                filename_addition_views = [filename_addition+"view_1"]
                views = ['1']
            if bdv_xml.nangles == 2:
                filename_addition_views = [filename_addition+"view_1", filename_addition+"view_2"]
                views = ['1', '2']
        

    # if views is both and we're not fusing, run this twice
    # note that save_fused is true so we get fused tiff naming with channel

    for v_i in range(len(views)):
        # Build (windows) command
        # first build param list
        params = (f"\"xml_path='{xml_path}', out_dir='{out_dir}', downscale={downscale}," +
                f"fusion_method='{fusion_method}', view='{views[v_i]}'," +
                f"filename_addition='{filename_addition_views[v_i]}', save_method='{save_method}'," +
                f"opm_angle={opm_angle}, save_fused={save_fused}\"")

        imagej_exe = os.path.join(imagej_dir, "ImageJ-win64.exe")
        abs_root_path = os.path.dirname(__file__)
        macro_path = os.path.join(abs_root_path, "imagej_macros/image_fusion.ijm")
        # macro_path = "./imagej_macros/image_fusion.ijm"
        command = f"{imagej_exe} --ij2 {headless_str} --run {macro_path} {params}"

        print("Running command: " + command)
        subprocess.run(command)
        # result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
 
 


import numpy as np
import os
from tifffile import imread, TiffFile
from ome_types import from_tiff
from glob import glob
from timeit import default_timer as timer
import warnings

def get_dims_from_metadata(stack_dir):
    # get metadata using ome-types library, tifffile doesnt parse xml 
    # into a dict unlike mm metadata
    stacks = glob(os.path.join(stack_dir, "HamamatsuHam_DCAM-dopm/*.tif"))
    print("Stack dir", stack_dir, "stacks", stacks)
    omexml = from_tiff(stacks[0])
    iminfo = omexml.images[0]

    size_x = iminfo.pixels.size_x  # x dimension
    size_zp = iminfo.pixels.size_y  # z prime dimension
    size_scan = len(omexml.images)  # n frames (y for yscanning)
    vox_size_x_um = iminfo.pixels.physical_size_x
    vox_size_zp_um = iminfo.pixels.physical_size_y
    vox_size_scan_um = iminfo.pixels.physical_size_z

    vox_dims = np.array((vox_size_x_um, vox_size_zp_um, vox_size_scan_um))
    min_vox_dim = np.min(vox_dims)
    normalized_vox_dims = vox_dims/min_vox_dim  # otherwise x and zp are downscaled to 1px
    
    print("size_x", size_x)
    print("size_zp", size_zp)
    print("size_scan", size_scan)

    dims_info = {
        'size_x':size_x, 'size_zp':size_zp, 'size_scan':size_scan,
        'vox_size_x_um':vox_size_x_um, 
        'vox_size_zp_um':vox_size_zp_um,
        'vox_size_scan_um':vox_size_scan_um
    }

    return dims_info, stacks


def load_tiff(stack_dir, projection='mean'):
    # get ome metadata
    dims, stacks = get_dims_from_metadata(stack_dir)

    imstack = np.zeros((
        dims['size_scan'], dims['size_zp'], dims['size_x']), dtype=np.uint16)

    start_time = timer()

    # read the mm-split 4gb tiff stacks into one big stack (matrix),
    # think about memory concerns...
    
    offset = 0
    for i in range(len(stacks)):
        print("loading",  stacks[i])
        with TiffFile(stacks[i]) as tif:
            mm_metadata = tif.micromanager_metadata
            try:
                pos_label = mm_metadata['Summary']['UserData']['positionLabel']['scalar']
            except:
                warnings.warn("Unable to get position label from MM metadata")
                pos_label = "XX"
                
            for n, page in enumerate(tif.pages):
                # print("page", n)
                imstack[n+offset,:,:] = page.asarray() # expects zyx
        offset += n+1

    end_time = timer()
    print("Read time", (end_time-start_time), "ms")

    return imstack, pos_label

def load_mean_projection(stack_dir, sampling=4, threshold=97):
    # get ome metadata
    dims, stacks = get_dims_from_metadata(stack_dir)

    improject = np.zeros((
        dims['size_zp'], dims['size_x']), dtype=np.uint32)

    start_time = timer()

    # read the mm-split 4gb tiff stacks into one big stack (matrix),
    # think about memory concerns...
    
    for i in range(len(stacks)):
        print("loading",  stacks[i])
        with TiffFile(stacks[i]) as tif:
            mm_metadata = tif.micromanager_metadata
            try:
                pos_label = mm_metadata['Summary']['UserData']['positionLabel']['scalar']
            except:
                warnings.warn("Unable to get position label from MM metadata")
                pos_label = "XX"
            pages_to_loop=tif.pages[::sampling]
            for n, page in enumerate(pages_to_loop):
                # print("page", n)
                frame = page.asarray()
                if threshold is None:
                    frame = frame-np.min(threshold, np.min(frame))
                improject += page.asarray() # expects zyx

    end_time = timer()
    print("Read time", (end_time-start_time), "ms")

    # rescale to 16bit
    scale = np.max(improject)/(2**15)
    improject = improject/scale

    return np.uint16(improject), pos_label

def parse_tiff_dirs(tiff_data_dir, opm_angle=45):
    tiff_dirs = glob(os.path.join(tiff_data_dir, "dOPM*"))
    print("List of dirs:\n",tiff_dirs)

    grouped_details = {}
    details_list = []

    for tiff_dir in tiff_dirs:
        print(tiff_dir)
        view_details = os.path.basename(tiff_dir).split("_")
        angle = -opm_angle if "view1" in view_details[-1] else opm_angle
        position_key = view_details[2]
        position_str = position_key[1:]
        time_str = view_details[1][1:]
        z_str = view_details[3][1:]
        channel_str = view_details[4][1:]

        tiff_dir_dict = {}
        tiff_dir_dict["time"] = time_str
        tiff_dir_dict["z"] = z_str
        tiff_dir_dict["channel"] = channel_str
        tiff_dir_dict["dir"] = tiff_dir
        tiff_dir_dict["angle"] = angle

        if position_key in grouped_details:
            grouped_details[position_key].append(tiff_dir_dict)
        else:
            grouped_details[position_key] = [tiff_dir_dict]

        details_list.append(tiff_dir_dict)

    return grouped_details, details_list

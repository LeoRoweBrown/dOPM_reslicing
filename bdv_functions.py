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

def parse_tiff_dirs(tiff_data_dir, opm_angle=45):
    tiff_dirs = glob(os.path.join(tiff_data_dir, "dOPM*"))
    print("List of dirs:\n",tiff_dirs)

    grouped_details = {}

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

    return grouped_details

def create_bdv_datasets(tiff_data_dir, out_dir, opm_angle=45, stop_at_position=None, max_slices_per_tile=3000):
    """
    Create a BDV dataset from a directory of tiff stacks, with each directory containing
    a given view (angle), timepoint, z-stack, channel. Datasets are separated by position 
    with intention to stitch.

    Parameters
    ----------
    tiff_data_dir : str
        Path to directory containing tiff stacks from dOPM microscope
    out_dir : str
        Path to output directory for BDV dataset
    opm_angle : int, optional
        The angle of the OPM microscope, by default 45.
    stop_at_position : int, optional
        Position at which to stop processing, by default None.
    Raises
    ------
    FileExistsError
        If the output directory already exists.

    """


    # get the grouped details from the tiff dirs
    grouped_details = parse_tiff_dirs(tiff_data_dir, opm_angle)

    # get current date for file timestamp
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    print(date_time)

    if os.path.exists(out_dir):
        print("Output directory already exists, exiting")
        raise(FileExistsError)

    # loop over grouped details, specifically each position
    for position, details in grouped_details.items():
        if stop_at_position is not None and int(position[1:]) != stop_at_position:
            break
        dirs = [d["dir"] for d in details]
        channels_strs = [d["channel"] for d in details]
        time_strs = [d["time"] for d in details]
        z_strs = [d["z"] for d in details]
        angles = [d["angle"] + OPM_ANGLE for d in details]
        angle_idxc = [0 if a == 0 else 1 for a in angles]

        # print all those dimenisons e.g. time, z, channel in a single print statement
        print("channels", channels_strs, "time", time_strs, "z", z_strs, "angle", angles)

        # to get n channels etc. use set(channels) etc. to get unique values
        n_channels = len(set(channels_strs))
        n_times = len(set(time_str))
        n_z = len(set(z_str))
        n_angles = len(set(angles))

        # for BDV dataset attributes
        channel_attr = [None]*n_channels
        angle_attr = [None]*n_angles

        # create BDV dataset
        save_path = os.path.join(out_dir, "pos_"+position_str)
        os.makedirs(save_path, exist_ok=True)
        save_file = os.path.join(save_path, "dataset.h5")

        bdv_writer = BdvWriter(save_file, 
                            nchannels=n_channels, 
                            nilluminations=1, 
                            nangles=n_angles,
                            ntiles=n_z)

        for n, tiff_dir in enumerate(dirs):
            print(tiff_dir)
            view_details = os.path.basename(tiff_dir).split("_")
            angle = -OPM_ANGLE if "view1" in view_details[-1] else OPM_ANGLE
            angle_i = angle_idxc[n]
            position_str = position
            position_i = int(position_str[1:])
            time_str = time_strs[n]
            time_i = int(time_str)
            z_str = z_strs[n]
            z_i = int(z_str)
            channel_str = channels_strs[n]
            channel_i = int(channel_str)

            print("angle", angle)
            print("position", position_str)
            print("time", time_str)
            print("z", z_str)
            print("channel", channel_str)

            # print(stack_dir)
            print(os.path.join(tiff_dir, "HamamatsuHam_DCAM-dopm/*.tif"))
            stacks = glob(os.path.join(tiff_dir, "HamamatsuHam_DCAM-dopm/*.tif"))

            # get ome metadata using ome-types library, tifffile doesnt parse xml into a dict unlike mm metadata
            omexml = from_tiff(stacks[0])
            iminfo = omexml.images[0]

            size_x = iminfo.pixels.size_x  # x dimension
            size_zp = iminfo.pixels.size_y  # z prime dimension
            size_scan = len(omexml.images)
            vox_size_x_um = iminfo.pixels.physical_size_x
            vox_size_zp_um = iminfo.pixels.physical_size_zp
            vox_size_z_um = iminfo.pixels.physical_size_z
            
            # unused, in future split positions into pos0001_0001, pos0001_0002 etc. when there's limited memory
            n_tiles_scan = size_scan // max_slices_per_tile  # 
            
            print("size_x", size_x)
            print("size_zp", size_zp)
            print("size_scan", size_scan)

            imstack = np.zeros((size_scan, size_zp, size_x), dtype=np.uint16)

            start_time = timer()

            # read the mm-split 4gb tiff stacks into one big stack (matrix), think about memory concerns...
            
            offset = 0
            for i in range(len(stacks)):
                print("loading",  stacks[i])
                with TiffFile(stacks[i]) as tif:
                    mm_metadata = tif.micromanager_metadata
                    for n, page in enumerate(tif.pages):
                        # print("page", n)
                        imstack[n+offset,:,:] = page.asarray() # expects zyx
                offset += n+1

            end_time = timer()
            print("Read time", (end_time-start_time), "ms")

            laser_meta = mm_metadata['Summary']['UserData']['laser']
            filter_meta = mm_metadata['Summary']['UserData']['filter']
            
            channel_attr[channel_i] = f"{laser_meta}"
            angle_attr[angle_i] = f"{angle}"

            start_time = timer()  # start timer for saving h5 file

            angle_from_zero = angle+OPM_ANGLE
            bdv_writer.append_view(
                imstack, angle=angle_i, time=time_i, tile=z_i, channel=channel_i,
                calibration=(vox_size_x_um, vox_size_zp_um, vox_size_z_um),
                voxel_size_xyz=(vox_size_x_um, vox_size_zp_um, vox_size_z_um),
                voxel_units='micron')
            print(f"dataset in {save_file}")
            bdv_writer.write_xml()

        # loop again to append the affines... annoying to have to do this
        for n in range(len(dirs)):
            angle_i = angle_idxc[n]
            position_i = int(position_str[1:])
            time_i = int(time_strs[n])
            z_i = int(z_strs[n])
            channel_i = int(channels_strs[n])

            bdv_writer.append_affine(
                affine.rotation_matrix(theta=np.pi/2, axis='x', square=False),
                name_affine='90 deg rotation about x',
                angle=angle_i, time=time_i, tile=z_i, channel=channel_i)
            skew_angle = -np.pi*(angle)/180
            bdv_writer.append_affine(
                affine.scale_matrix(sz=np.sin(skew_angle), square=False),
                name_affine='scale before shear',
                angle=angle_i, time=time_i, tile=z_i, channel=channel_i)
            bdv_writer.append_affine(
                affine.skew_matrix(skew_angle, square=False),
                name_affine='shear to deskew',
                angle=angle_i, time=time_i, tile=z_i, channel=channel_i)
            if angle > 0:
                bdv_writer.append_affine(affine.identity_matrix(square=False),
                    name_affine='identity to debug second view',
                    angle=angle_i, time=time_i, tile=z_i, channel=channel_i)

            
        # 
        bdv_writer.set_attribute_labels('angle', angle_attr) 
        bdv_writer.set_attribute_labels('channel', channel_attr)

        bdv_writer.close()
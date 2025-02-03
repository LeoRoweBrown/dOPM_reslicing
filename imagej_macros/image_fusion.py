#@ String (label="XML file for BDV dataset", persist=true) xml_path
#@ String (label="Directory to save fused/deskewed data", persist=true) out_dir
#@ Integer (label="Downscaling factor", value=4, min=1) downscale
#@ Boolean (label="Fuse views", value=false) save_fused
#@ Integer (label="OPM angle", value=45) opm_angle
#@ String (label="Fusion method", value="[Avg, Blending]", style="listBox", choices={"[Avg]", "[Avg, Blending]", "[Avg, Content Based]", "[Avg, Blending & Content Based]", "[Max intensity]", "[First Tile Wins (lowest ViewSetupId)]"}) fusion_method
#@ String (label="View to load", description="the view (1, 2) or 'both'", value="both", choices={"1", "2", "both"}) view
#@ String (label="Save method (default is tiff)", value="[Save as (compressed) TIFF stacks]", choices="[Save as (compressed) TIFF stacks]") save_method
#@ String (label="Prefix to filename", value="") filename_addition


import os, sys
from ij import IJ

print("Inside macro, xml_path = " + xml_path)
print("Out path with be " + out_dir)

# Map inputs to ImageJ-compatible options
if (save_fused):
    produce = "[Each timepoint & channel]"
else:
    produce = "[Each view]"

if (view == "1"):
    angle_in_file =  "[angle 0]"
elif (view == "2"):
    angle_in_file = "[angle " + str(int(opm_angle * 2)) + "]"
elif (view == "both") :
    angles = "[All angles]"

# make directories to save fused volumes
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Construct ImageJ command
ij_params = (
    "\"select={xml_path} "
    "process_angle={angles} "
    "process_channel=[All channels] "
    "process_illumination=[All illuminations] "
    "process_tile=[All tiles] "
    "process_timepoint=[All Timepoints] "
    "bounding_box=[Currently Selected Views] "
    "downsampling={downscale} "
    "interpolation=[Linear Interpolation] "
    "fusion_type={fusion_method} "
    "pixel_type=[16-bit unsigned integer] "
    "interest_points_for_non_rigid=[-= Disable Non-Rigid =-] "
    "produce={produce} "
    "fused_image={save_method} "
    "define_input=[Auto-load from input data (values shown below)] "
    "output_file_directory={out_dir} "
    "filename_addition=[{filename_addition}]\");".format(
        xml_path=xml_path,
        angles=angles,
        downscale=downscale,
        fusion_method=fusion_method,
        produce=produce,
        save_method=save_method,
        out_dir=out_dir,
        filename_addition=filename_addition
    )
)

print(ij_params)

IJ.run("Image Fusion", ij_params)
	
print("Quitting...");

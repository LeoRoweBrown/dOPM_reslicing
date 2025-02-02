#@ String (label="XML file for BDV dataset", persist=false) xml_path
#@ String (label="Directory to save fused/deskewed data", persist=false) out_dir
#@ Integer (label="Downscaling factor", value=4, min=1) downscale
#@ Boolean (label="Fuse views", value=false) save_fused
#@ Integer (label="OPM angle", value=45) opm_angle
#@ String (label="Fusion method", value="[Avg, Blending]", style="listBox", choices={"[Avg]", "[Avg, Blending]", "[Avg, Content Based]", "[Avg, Blending & Content Based]", "[Max intensity]", "[First Tile Wins (lowest ViewSetupId)]"}) fusion_method
#@ String (label="View to load", description="the view (1, 2) or 'both'", value="both", choices={"1", "2", "both"}) view
#@ String (label="Save method (default is tiff)", value="[Save as (compressed) TIFF stacks]", choices="[Save as (compressed) TIFF stacks]") save_method
#@ String (label="Prefix to filename", value="") filename_addition
#@ String (label="testvar", value="test") testvar

// Image Fusion Macro Script

function makeDirectories(path){
	// make path recursively
	if (!File.exists(path)) {
	    parent = File.getParent(path);
	    if (parent != "" && !File.exists(parent)) {
	        makeDirectories(parent); // Recursively create parent directories
	    }
	    File.makeDirectory(path); // Create the final directory
	}
}

setBatchMode(true);

print("Inside macro, xml_path = " + xml_path);
print("Out path with be " + out_dir);
print("testvar is " + testvar);

// Map inputs to ImageJ-compatible options
if (save_fused) {
    produce = "[Each timepoint & channel]";
} else {
    produce = "[Each view]";
}

if (view == "1") {
    angle_in_file =  "[angle 0]";
} else if (view == "2") {
    angle_in_file = "[angle " + opm_angle * 2 + "]";
} else if (view == "both") {
    angles = "[All angles]";
}

// make directories to save fused volumes
makeDirectories(out_dir);

/* run("Image Fusion", 
    "select=" + xml_path + 
    " process_angle=" + angles + 
    " process_channel=[All channels]" + 
    " process_illumination=[All illuminations]" + 
    " process_tile=[All tiles]" + 
    " process_timepoint=[All Timepoints]" + 
    " bounding_box=[Currently Selected Views]" + 
    " downsampling=" + downscale + 
    " interpolation=[Linear Interpolation]" + 
    " fusion_type=" + fusion_method + 
    " pixel_type=[16-bit unsigned integer]" + 
    " interest_points_for_non_rigid=[-= Disable Non-Rigid =-]" + 
    " produce=" + produce + 
    " fused_image=" + save_method + 
    " define_input=[Auto-load from input data (values shown below)]" + 
    " output_file_directory=" + out_dir + 
    " filename_addition=[" + filename_addition + "]");
	*/
print("Quitting...");
System.exit(0);
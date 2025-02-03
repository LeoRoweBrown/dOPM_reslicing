#@ String (label="XML file for BDV dataset", persist=true) xml_path
#@ String (label="Directory to save fused/deskewed data", persist=true) out_dir
#@ Integer (label="Downscaling factor", value=4, min=1) downscale
#@ Boolean (label="Fuse views", value=false) save_fused
#@ Integer (label="OPM angle", value=45) opm_angle
#@ String (label="Fusion method", value="[Avg, Blending]", style="listBox", choices={"[Avg]", "[Avg, Blending]", "[Avg, Content Based]", "[Avg, Blending & Content Based]", "[Max intensity]", "[First Tile Wins (lowest ViewSetupId)]"}) fusion_method
#@ String (label="View to load", description="the view (1, 2) or 'both'", value="both", choices={"1", "2", "both"}) view
#@ String (label="Save method (default is tiff)", value="[Save as (compressed) TIFF stacks]", choices="[Save as (compressed) TIFF stacks]") save_method
#@ String (label="Prefix to filename", value="") filename_addition

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


print("Inside macro, xml_path = " + xml_path);
print("Out path with be " + out_dir);

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

newImage("Untitled", "16-bit white", 1000, 1000, 100);
run("Out [-]");
run("Out [-]");
run("Gradient (3D)", "use");
	
print("Quitting...");
close("*");
// setOption("Changes",false);
setKeyDown("Esc");
run("Quit");
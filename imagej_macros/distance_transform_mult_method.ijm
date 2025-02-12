loaddir = "A:/leo/micromanager/dan_2/d3/fused_tiffs/";
tiffname = "fused_tp_0_ch_1.tif";
results_save_dir = loaddir;

open(loaddir+tiffname);
selectImage("fused_tp_0_ch_1.tif");
run("Z Project...", "projection=[Max Intensity]");
rename("max");
run("Duplicate...", "title=mask");
setThreshold(0, 700, "raw");
run("Convert to Mask");
run("Distance Transform 3D");
imageCalculator("Multiply create 32-bit", "max","Distance");
run("Measure");
saveAs("Results", results_save_dir+"/Results.csv");
run("Clear Results");

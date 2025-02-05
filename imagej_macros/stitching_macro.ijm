run("BigStitcher", 
    "select=define " +
    "define_dataset=[Manual Loader (TIFF only, ImageJ Opener)] " +
    "project_filename=dataset.xml " +
    "multiple_timepoints=[NO (one time-point)] " +
    "multiple_channels=[YES (one file per channel)] " +
    "multiple_illumination_directions=[NO (one illumination direction)] " +
    "multiple_angles=[NO (one angle)] " +
    "multiple_tiles=[YES (one file per tile)] " +
    "image_file_directory=A:/leo/micromanager/dan_2/row_b_and_d_fromb3_pos2/deskewed_20250203-150527/fused_tiffs " +
    "image_file_pattern=pos_p{xxxx}_fused_tp_0_vs_{c}.tif " +
    "channels_=0,1 " +
    "tiles_=0,1,2,3,4 " +
    "calibration_type=[Same voxel-size for all views] " +
    "calibration_definition=[Load voxel-size(s) from file(s) and display for verification] " +
    "show_list " +
    "pos_p0000_fused_tp_0_vs_0.tif pos_p0001_fused_tp_0_vs_0.tif pos_p0002_fused_tp_0_vs_0.tif " +
    "pos_p0003_fused_tp_0_vs_0.tif pos_p0004_fused_tp_0_vs_0.tif " +
    "pos_p0000_fused_tp_0_vs_1.tif pos_p0001_fused_tp_0_vs_1.tif pos_p0002_fused_tp_0_vs_1.tif " +
    "pos_p0003_fused_tp_0_vs_1.tif pos_p0004_fused_tp_0_vs_1.tif " +
    "pixel_distance_x=0.86327 " +
    "pixel_distance_y=0.86327 " +
    "pixel_distance_z=0.86327 " +
    "pixel_unit=micron"
);

// run("BigStitcher", "select=define define_dataset=[Manual Loader (TIFF only, ImageJ Opener)] project_filename=dataset.xml multiple_timepoints=[NO (one time-point)] multiple_channels=[YES (one file per channel)] _____multiple_illumination_directions=[NO (one illumination direction)] multiple_angles=[NO (one angle)] multiple_tiles=[YES (one file per tile)] image_file_directory=A:/leo/micromanager/dan_2/row_b_and_d_fromb3_pos2/deskewed_20250203-150527/fused_tiffs image_file_pattern=pos_p{xxxx}_fused_tp_0_vs_{c}.tif channels_=0,1 tiles_=0,1,2,3,4,8 calibration_type=[Same voxel-size for all views] calibration_definition=[Load voxel-size(s) from file(s) and display for verification] show_list pos_p0000_fused_tp_0_vs_0.tif pos_p0001_fused_tp_0_vs_0.tif pos_p0002_fused_tp_0_vs_0.tif pos_p0003_fused_tp_0_vs_0.tif pos_p0004_fused_tp_0_vs_0.tif pos_p0008_fused_tp_0_vs_0.tif pos_p0000_fused_tp_0_vs_1.tif pos_p0001_fused_tp_0_vs_1.tif pos_p0002_fused_tp_0_vs_1.tif pos_p0003_fused_tp_0_vs_1.tif pos_p0004_fused_tp_0_vs_1.tif pos_p0008_fused_tp_0_vs_1.tif pixel_distance_x=0.86327 pixel_distance_y=0.86327 pixel_distance_z=0.86327 pixel_unit=micron");

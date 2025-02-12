/*run("Image Fusion","select=file:///A:/leo/micromanager/bone_marrow_2nd/control/1pos_2048_test/deskewed_20250206-121256/pos_p0000/dataset.xml "+
"process_angle=[Range of angles (Specify by Name)] process_channel=[All channels] process_illumination=[All illuminations] process_tile=[All tiles] "+
"process_timepoint=[All Timepoints] process_following_angles=0 bounding_box=[Currently Selected Views] downsampling=4 interpolation=[Linear Interpolation] "+
"fusion_type=[Avg, Blending] pixel_type=[16-bit unsigned integer] interest_points_for_non_rigid=[-= Disable Non-Rigid =-] produce=[Each timepoint & channel] "+
"fused_image=[Save as (compressed) TIFF stacks] define_input=[Auto-load from input data (values shown below)] "+
"output_file_directory='A:/leo/micromanager/bone_marrow_2nd/control/1pos_2048_test/deskewed_20250206-121256/fused_tiffs' filename_addition=[test_pos_p0000view_1]");*/

run("Image Fusion","select=file:///A:/leo/micromanager/bone_marrow_2nd/control/1pos_2048_test/deskewed_20250206-121256/pos_p0000/dataset.xml "+
"process_angle=[Range of angles (Specify by Name)] process_channel=[All channels] process_illumination=[All illuminations] process_tile=[All tiles] "+
"process_timepoint=[All Timepoints] process_following_angles=0 bounding_box=[Currently Selected Views] downsampling=4 interpolation=[Linear Interpolation] "+
"fusion_type=[Avg, Blending] pixel_type=[16-bit unsigned integer] interest_points_for_non_rigid=[-= Disable Non-Rigid =-] produce=[Each timepoint & channel] "+
"fused_image=[Save as (compressed) TIFF stacks] define_input=[Auto-load from input data (values shown below)] "+
"output_file_directory='A:/leo/micromanager/bone_marrow_2nd/control/1pos_2048_test/deskewed_20250206-121256/fused_tiffs_2' filename_addition=[pos_p0000view_1]");


// run(Image Fusion,select=file:///A:/leo/micromanager/bone_marrow_2nd/control/1pos_2048_test/deskewed_20250206-121256/pos_p0000/dataset.xml process_angle=[Range of angles (Specify by Name)] process_channel=[All channels] process_illumination=[All illuminations] process_tile=[All tiles] process_timepoint=[All Timepoints] process_following_angles=0 bounding_box=[Currently Selected Views] downsampling=4 interpolation=[Linear Interpolation] fusion_type=[Avg, Blending] pixel_type=[16-bit unsigned integer] interest_points_for_non_rigid=[-= Disable Non-Rigid =-] produce=[Each timepoint & channel] fused_image=[Save as (compressed) TIFF stacks] define_input=[Auto-load from input data (values shown below)] output_file_directory=A:\leo\micromanager\bone_marrow_2nd\control\1pos_2048_test\deskewed_20250206-121256\fused_tiffs_2 filename_addition=[pos_p0000view_1])
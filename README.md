# arsei_ffmpeg
# modified ffmpeg and ffplay
1. Check out the latest version of ffmpeg
2. Apply the "arsei_modifications.patch"
3. Build ffmpeg along with the patch by following the instructions from here, https://trac.ffmpeg.org/wiki/CompilationGuide
4. Note : Please make sure that dependent packages for ffplay (see configure -> ffplay_deps) have been installed. Otherwise, ffplay will not be built. 

# arsei_ffmpeg
1. Copy the SFU-HW-Tracks-v1 dataset from https://data.mendeley.com/datasets/d5cc83ks6c/1 into the "Annotated_labels" folder.
   It will look something like "Annotated_labels/SFU-HW-Tracks-v1/ClassE/FourPeople/<annotated_labels>"
2. Create the arsei_cfg folder like arsei_cfg/FourPeople
3. Copy the input video to the "input" folder. Some of the sample videos could be found here, https://media.xiph.org/video/derf/
4. There is already a pre-built binary for HM encoder in the bin folder. If required, re-build the HM encoder using the source from https://vcgit.hhi.fraunhofer.de/jvet/HM and replace the binary.
5. Change the directory to bin folder.
6. Execute the master script file (In debian, source anno_label_to_bitstream.sh)
7. This will first convert the SFU-HW-Tracks-v1 annotated labels to config files and then encode the video along with the annotated regions in the form of ARSEI.
8. Now the bit stream could be visualized using ffplay <bitsream.h265>. This will display both the frames as well as the annotated regions in the form of bounding boxes. 

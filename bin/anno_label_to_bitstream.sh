#!bin/bash
# Convert the annotated labels to arsei cfg files
python3 dataset_arsei.py -i ../Annotated_labels/SFU-HW-Tracks-v1/ClassE/FourPeople/ -t FourPeople_1280x720_60_seq -o ../arsei_cfg/FourPeople/ -s FourPeople_1280x720_60_seq -l FourPeople_1280x720_object -f 600
echo "#########################################"
echo "Converted annotation labels to arsei cfg files"
echo "#########################################"

#Encode the video with ARSEI data
./TAppEncoderStaticd -c encoder_lowdelay_P_main.cfg
echo "#########################################"
echo "Encoding done, Please use ffplay to view the bitstream"
echo "#########################################"

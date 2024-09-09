"""
 Annotation label to annotated regions SEI config generator
 Author : Palanivel Guruvareddiar (Palanivel.Guruvareddiar@gmail.com)
"""
# Import Necessary Modules
import os
import sys
import argparse

#returns the label of the matching
def return_class_label(iden, id_lab_pair):
    for entries in id_lab_pair:
        if entries[1] == str(iden):
            return entries[0]

#returns the label's word length (E.g.: Cell phone has more length than Cellphone)
def find_label_len(labels_fld):
    length = 0
    #Look for Class field
    for i in range(len(labels_fld)):
        length += 1
        if labels_fld[i][1:] == 'Class':
            break
    return length

# Main Function
if __name__ == '__main__':

    # Constructs Argument Parser for User Input
    parser = argparse.ArgumentParser(
        description='AR SEI CFG Creator Script.Requires input folder & token, output folder & token, and no of frames.')
    parser.add_argument('-i', "--input_folder", required=True, help="input folder")
    parser.add_argument('-t', "--input_token", required=True, help="input token")
    parser.add_argument('-o', "--output_folder", required=True, help="output folder")
    parser.add_argument('-s', "--output_token", required=True, help="output token")
    parser.add_argument('-l', "--label_list_token", required=True, help="label list")
    parser.add_argument('-f', "--num_frames", required=True, help="number of frames")
    args = vars(parser.parse_args())

    # Path to inputs
    in_folder = args["input_folder"]
    in_token = args["input_token"]
    out_folder = args["output_folder"]
    out_token = args["output_token"]
    lab_list_token = args["label_list_token"]
    num_fr = args["num_frames"]

    # Tries to return Video Name, Width, Height, and Frame rate from *.annotation labels
    try:
        input_vid = (os.path.basename(in_token)).split(".")[0]
        input_name = input_vid.split(" ")[0]
        width = int((input_vid.split("_")[1]).split("x")[0])
        height = int((input_vid.split("_")[1]).split("x")[1])

    # Otherwise, Raise Error
    except:
        print("Error: Unsupported Video File Name")
        sys.exit()

    in_label_list_path = in_folder + lab_list_token + ".list"
    # Label list file
    lab_f = open(in_label_list_path, 'r')

    # (Label, Object) list pair from .list file
    label_obj_pair = []

    # Object info
    obj_info = []

    # Input path
    for f in range(int(num_fr)):
        counter = str(f).zfill(3)
        input_path = in_folder + in_token + "_" + counter + ".txt"
        output_path = out_folder + out_token + "_" + str(f) + ".txt"

        # Read labels for this frame from the list file
        num_labels = 0
        lab_lines = []
        lab_line = 0
        while lab_line != '\n':
            lab_line = lab_f.readline()
            if lab_line != '\n':
                lab_lines.append(lab_line)

        label_id_pair = []
        label_cnt = 0
        for labels in lab_lines:
            if label_cnt != 0:
                labels_field = labels.split()
                lab_len = find_label_len(labels_field)
                if lab_len < 3:
                    pair = ((labels_field[0][1:]), labels_field[lab_len][3:-2])
                else :
                    pair = ((labels_field[0][1:] + labels_field[1][0:] ), labels_field[lab_len][3:-2])
                label_id_pair.append(pair)
            label_cnt += 1

        # Look for any new labels in the frame
        new_pairs = []
        for pairs in label_id_pair:
            if pairs not in label_obj_pair:
                num_labels += 1
                label_obj_pair.append(pairs)
                new_pairs.append(pairs)

        # Count the number of objects
        # Every line represents an object
        num_objs = 0
        lines = []
        with open(input_path, 'r') as in_f:
            for line in in_f:
                num_objs += 1
                unique_obj_id = int(line.split()[0]) + int(line.split()[1])
                line_values = [int(line.split()[0]), unique_obj_id, float(line.split()[2]),
                               float(line.split()[3]), float(line.split()[4]), float(line.split()[5])]
                lines.append(line_values)
            lines = sorted(lines, key=lambda z: (z[0], z[1]))

        # Generate the output file contents
        out_f = open(output_path, "w")
        out_f.write("SEIArCancelFlag: 0\n")
        out_f.write("SEIArNotOptForViewingFlag: 0\n")
        out_f.write("SEIArTrueMotionFlag: 0\n")
        out_f.write("SEIArOccludedObjsFlag: 0\n")
        out_f.write("SEIArPartialObjsFlagPresentFlag: 0\n")
        out_f.write("SEIArObjLabelPresentFlag: 1\n")
        out_f.write("SEIArObjConfInfoPresentFlag: 0\n")
        out_f.write("SEIArObjLabelLangPresentFlag: 1\n")
        out_f.write("SEIArLabelLanguage: ENGLISH\n")
        # Label related information
        out_f.write("SEIArNumLabelUpdates: ")
        out_f.write(str(num_labels))
        out_f.write("\n")
        for n in new_pairs:
            out_f.write("SEIArLabelIdc[c]: ")
            out_f.write(str(n[1]))
            out_f.write("\n")
            out_f.write("SEIArLabelCancelFlag[c]: 0\n")
            out_f.write("SEIArLabel[c]: ")
            out_f.write(str(n[0]))
            out_f.write("\n")

        # Object related information
        out_f.write("SEIArNumObjUpdates: ")
        out_f.write(str(max(num_objs, len(obj_info))))
        out_f.write("\n")

        # Check to see whether any object disappeared
        if num_objs < len(obj_info):
            obj_pool = []
            items_to_be_popped = []
            for n in range(int(num_objs)):
                obj_contents = lines[n]
                cls_id = (obj_contents[0])
                class_lab = return_class_label(cls_id, label_id_pair)
                obj_id = (int(obj_contents[1]))
                obj_pool.append([obj_id, class_lab])

            for n in range(len(obj_info)):
                list_search = [obj_info[n][0], obj_info[n][1]]
                if any(list == list_search for list in obj_pool) == False:
                    out_f.write("SEIArObjIdx[c]: ")
                    out_f.write(str(obj_info[n][0]))
                    out_f.write("\n")
                    out_f.write("SEIArObjCancelFlag[c]: 1\n")
                    items_to_be_popped.append(int(n))
            if len(items_to_be_popped) > 0:
                for n in range(len(items_to_be_popped)):
                    obj_info.pop(items_to_be_popped[n])

        # Object contents
        for n in range(int(num_objs)):
            obj_contents = lines[n]
            cls_id = (obj_contents[0])
            class_lab = return_class_label(cls_id, label_id_pair)
            obj_id = (int(obj_contents[1]))
            out_f.write("SEIArObjIdx[c]: ")
            out_f.write(str(obj_id))
            out_f.write("\n")
            out_f.write("SEIArObjCancelFlag[c]: 0\n")

            if len(obj_info) > 0:
                list_search = [obj_id, class_lab]
                if any(list == list_search for list in obj_info):
                    # Existing object
                    index = obj_info.index(list_search)
                    # Whether label changed
                    if class_lab != obj_info[index][1]:
                        out_f.write("SEIArObjLabelUpdateFlag[c]: 1\n")
                        out_f.write("SEIArObjectLabelIdc[c]: ")
                        for sublist in label_obj_pair:
                            if sublist[0] == class_lab:
                                class_id = sublist[1]
                                out_f.write(str(class_id))
                                out_f.write("\n")
                                break
                    else:
                        out_f.write("SEIArObjLabelUpdateFlag[c]: 0\n")
                else:
                    out_f.write("SEIArObjLabelUpdateFlag[c]: 1\n")
                    out_f.write("SEIArObjectLabelIdc[c]: ")
                    for sublist in label_obj_pair:
                        if sublist[0] == class_lab:
                            class_id = sublist[1]
                            out_f.write(str(class_id))
                            out_f.write("\n")
                            break
                    pair = [obj_id, class_lab]
                    obj_info.append(pair)
            else:
                out_f.write("SEIArObjLabelUpdateFlag[c]: 1\n")
                out_f.write("SEIArObjectLabelIdc[c]: ")
                for sublist in label_obj_pair:
                    if sublist[0] == class_lab:
                        class_id = sublist[1]
                        out_f.write(str(class_id))
                        out_f.write("\n")
                        break
                pair = [obj_id, class_lab]
                obj_info.append(pair)

            out_f.write("SEIArBoundBoxUpdateFlag[c]: 1\n")
            out_f.write("SEIArBoundBoxCancelFlag[c]: 0\n")
            # Annotation files has (x,y) as the object midpoint and not TL x,y
            x = int(float(obj_contents[2]) * width)
            y = int(float(obj_contents[3]) * height)
            w = int(float(obj_contents[4]) * width)
            h = int(float(obj_contents[5]) * height)

            y_tl = y - int(h / 2)
            out_f.write("SEIArObjTop[c]: ")
            out_f.write(str(y_tl))
            out_f.write("\n")

            x_tl = x - int(w / 2)
            out_f.write("SEIArObjLeft[c]: ")
            out_f.write(str(x_tl))
            out_f.write("\n")
            out_f.write("SEIArObjWidth[c]: ")
            out_f.write(str(w))
            out_f.write("\n")

            out_f.write("SEIArObjHeight[c]: ")
            out_f.write(str(h))
            out_f.write("\n")

        out_f.close()

# -*- coding: utf-8 -*-
"""V2_with_bridges.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r07nhGnDgMuLBT_O2jO9ZrBuN4CrEpwo
"""

# Commented out IPython magic to ensure Python compatibility.
# ****************************** Importing Labraries *****************************************
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import argparse
import cv2
from skimage.util import img_as_float

# %matplotlib inline

# ************************ reading the image and the templates *************
img = cv2.imread("/app/uploads/image", cv2.IMREAD_GRAYSCALE)
temp1 = cv2.imread("/app/controllers/templates/and.PNG", cv2.IMREAD_GRAYSCALE)
temp2 = cv2.imread("/app/controllers/templates/or.PNG", cv2.IMREAD_GRAYSCALE)
temp3 = cv2.imread("/app/controllers/templates/xor.PNG", cv2.IMREAD_GRAYSCALE)
temp4 = cv2.imread("/app/controllers/templates/not.PNG", cv2.IMREAD_GRAYSCALE)
# greimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# template = cv2.imread("messi_face.jpg", 0)
# w, h = template.shape[::-1]

# ************************ Gate Detection *********************************

# ******************************* getting height and width for each gate ***************
w_and, h_and = temp1.shape[::-1]
w_or, h_or = temp2.shape[::-1]
w_xor, h_xor = temp3.shape[::-1]
w_not, h_not = temp4.shape[::-1]

detected_gates = []

# **************************** Detecting and gates *************************
res = cv2.matchTemplate(img, temp1, cv2.TM_CCORR_NORMED)
threshold = 0.99;
loc = np.where(res >= threshold)
i = 0
for pt in zip(*loc[::-1]):
    if i == 0:
        detected_gates.append([pt[0], pt[1], pt[0] + w_and, pt[1] + h_and, 0])
        pt_prev = pt
        i += 1
    else:
        if not (pt[0] >= pt_prev[0] - 5 and pt[0] <= pt_prev[0] + 5 \
                and pt[1] >= pt_prev[1] - 5 and pt[1] <= pt_prev[1] + 5):
            detected_gates.append([pt[0], pt[1], pt[0] + w_and, pt[1] + h_and, 0])
            pt_prev = pt
            i += 1

# **************************** Detecting or gates *************************
res = cv2.matchTemplate(img, temp2, cv2.TM_CCORR_NORMED)
threshold = 0.99;
loc = np.where(res >= threshold)
i = 0
for pt in zip(*loc[::-1]):
    if i == 0:
        detected_gates.append([pt[0], pt[1], pt[0] + w_or, pt[1] + h_or, 1])
        pt_prev = pt
        i += 1
    else:
        if not (pt[0] >= pt_prev[0] - 5 and pt[0] <= pt_prev[0] + 5 \
                and pt[1] >= pt_prev[1] - 5 and pt[1] <= pt_prev[1] + 5):
            detected_gates.append([pt[0], pt[1], pt[0] + w_or, pt[1] + h_or, 1])
            pt_prev = pt
            i += 1

# **************************** Detecting xor gates *************************
res = cv2.matchTemplate(img, temp3, cv2.TM_CCORR_NORMED)
threshold = 0.99;
loc = np.where(res >= threshold)
i = 0
for pt in zip(*loc[::-1]):
    if i == 0:
        detected_gates.append([pt[0], pt[1], pt[0] + w_xor, pt[1] + h_xor, 2])
        pt_prev = pt
        i += 1
    else:
        if not (pt[0] >= pt_prev[0] - 5 and pt[0] <= pt_prev[0] + 5 \
                and pt[1] >= pt_prev[1] - 5 and pt[1] <= pt_prev[1] + 5):
            detected_gates.append([pt[0], pt[1], pt[0] + w_xor, pt[1] + h_xor, 2])
            pt_prev = pt
            i += 1

# **************************** Detecting not gates *************************
res = cv2.matchTemplate(img, temp4, cv2.TM_CCORR_NORMED)
threshold = 0.99;
loc = np.where(res >= threshold)
i = 0
for pt in zip(*loc[::-1]):
    if i == 0:
        detected_gates.append([pt[0], pt[1], pt[0] + w_not, pt[1] + h_not, 3])
        pt_prev = pt
        i += 1
    else:
        if not (pt[0] >= pt_prev[0] - 5 and pt[0] <= pt_prev[0] + 5 \
                and pt[1] >= pt_prev[1] - 5 and pt[1] <= pt_prev[1] + 5):
            detected_gates.append([pt[0], pt[1], pt[0] + w_not, pt[1] + h_not, 3])
            pt_prev = pt
            i += 1

imgcopy = img.copy()
for pt in detected_gates:
    cv2.rectangle(imgcopy, (pt[0], pt[1]), (pt[2], pt[3]), (0, 0, 0), 2)
# plt.imshow(imgcopy , cmap = "gray")

# ****************************** Thresholding the input image ******************************
_, thresh_img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
# plt.imshow(thresh_img , cmap = 'gray')

# ****************************** Binarizing the input image ******************************
thresh_img = thresh_img / 255
# plt.imshow(thresh_img , cmap = 'gray')

# **************** Getting the image dimensions **************************
cols = thresh_img.shape[1]
rows = thresh_img.shape[0]

# negating the image
thresh_img_neg = thresh_img.copy()
for i in range(rows):
    for j in range(cols):
        if thresh_img[i][j] == 0:
            thresh_img_neg[i][j] = 1
        else:
            thresh_img_neg[i][j] = 0
# plt.imshow(thresh_img_neg , cmap = 'gray')

# Getting large points only (el point elly bna5od mnha wasla)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
img_of_large_points = cv2.erode(thresh_img_neg, kernel, iterations=1)
# plt.imshow(img_of_large_points , cmap = 'gray')

# Getting the centroids of the large points

img_of_large_points = np.uint8(img_of_large_points)
# starting from here we will see which 2 gates are connected
# You need to choose 4 or 8 for connectivity type
connectivity = 4
# Perform the operation
output = cv2.connectedComponentsWithStats(img_of_large_points)
# Get the results

# The first cell is the number of labels
num_labels_large_points = output[0]
# The second cell is the label matrix
labels_large_points = output[1]
# The third cell is the stat matrix
stats_large_points = output[2]
# The fourth cell is the centroid matrix
centroids_large_points = output[3]

# ****************************Corner detection*********************************
# We do that in order to get the points of intersection

filename = 'circuit.png'
imgForConrnersDetection = cv2.imread(filename)

gray = cv2.cvtColor(imgForConrnersDetection, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)

dst = cv2.cornerHarris(gray, 2, 3, 0.04)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
imgForDrawing = imgForConrnersDetection.copy()
imgForDrawing[dst > 0.1 * dst.max()] = [255, 255, 255]
# Will convert it to gray scale in order to subtract it form the original one
imgForDrawing = cv2.cvtColor(imgForDrawing, cv2.COLOR_BGR2GRAY)

# plt.imshow(imgForDrawing , cmap = 'gray')

# ***************************** Getting image of points *****************************
image_of_points = imgForDrawing - img
# plt.imshow(image_of_points , cmap = 'gray')

# Will delete any corner in the area of any gate
copy_image_of_points = image_of_points.copy()
for x in range(len(detected_gates)):
    copy_image_of_points[detected_gates[x][1]: detected_gates[x][3] + 1,
    detected_gates[x][0]: detected_gates[x][2] + 1] = 0

# plt.imshow(copy_image_of_points , cmap = 'gray')

# In this step we are considering only the corners in the wires intersections
# Fisrt we will get the centres of the connected components in copy_image_of_points

copy_image_of_points = np.uint8(copy_image_of_points)
# starting from here we will see which 2 gates are connected
# You need to choose 4 or 8 for connectivity type
connectivity = 4
# Perform the operation
output = cv2.connectedComponentsWithStats(copy_image_of_points)
# Get the results

# The first cell is the number of labels
num_labels_intersection = output[0]
# The second cell is the label matrix
labels_intersection = output[1]
# The third cell is the stat matrix
stats_intersection = output[2]
# The fourth cell is the centroid matrix
centroids_intersection = output[3]

intersection_point_list = []
# We will loop over them and select the intersection points only
for point in centroids_intersection:
    y = int(point[1])
    x = int(point[0])
    # See wether the point is surrunded by lines fromall directions
    if thresh_img[y, x + 5] == 0 and \
            thresh_img[y, x - 5] == 0 and \
            thresh_img[y + 5, x] == 0 and \
            thresh_img[y - 5, x] == 0:
        intersection_point_list.append(point)

# print((intersection_point_list))

'''
We will use findcontours function , so there must be no gaps between the connected gates, but the 
xor gate has gap between the first and second arc , so we will connect the with a small line
'''

# print(detected_gates)

# connecting XOR gates
thresh_img_neg_with_closed_xor = thresh_img_neg.copy()
cols = thresh_img_neg_with_closed_xor.shape[1]
rows = thresh_img_neg_with_closed_xor.shape[0]
mask = np.zeros((rows, cols))
# plt.imshow(thresh_img_neg_with_closed_xor , cmap = 'gray')
thresh_img_neg_with_closed_xor /= 255
for gate in detected_gates:
    # print(gate)
    if gate[4] == 2:
        x = int((gate[0] + gate[2]) / 2)
        y = int((gate[1] + gate[3]) / 2)
        mask[y - 5: y + 5, x - 20: x - 5] = 1
        # print(mask[y : y+20 , x-20 : x-5 ])
        # print(x, y)
thresh_img_neg_with_closed_xor = cv2.bitwise_or(thresh_img_neg, mask)

# plt.imshow(thresh_img_neg_with_closed_xor , cmap = 'gray')

# We will create two images , at the first one we will cut vertically above and below the
# intersection point , at the second ont we will cut horizontally left and right to the point

# 1. Horizontally
cut_img_horizontally = thresh_img_neg_with_closed_xor.copy()
for point in range(len(intersection_point_list)):
    centre_x = int(intersection_point_list[point][0])
    left = centre_x - 5
    right = centre_x + 5

    centre_y = int(intersection_point_list[point][1])
    top = centre_y - 5
    bottom = centre_y + 5

    cut_img_horizontally[top: bottom, left - 5: left] = 0
    cut_img_horizontally[top: bottom, right: right + 5] = 0

# plt.imshow(cut_img_horizontally , cmap = 'gray')

# 1. Vertically
cut_img_vertically = thresh_img_neg_with_closed_xor.copy()
for point in range(len(intersection_point_list)):
    centre_x = int(intersection_point_list[point][0])
    left = centre_x - 5
    right = centre_x + 5

    centre_y = int(intersection_point_list[point][1])
    top = centre_y - 5
    bottom = centre_y + 5

    cut_img_vertically[top - 5: top, left: right] = 0
    cut_img_vertically[bottom: bottom + 5, left: right] = 0

# plt.imshow(cut_img_vertically , cmap = 'gray')

# Now , it is the final step to find the connected gates , we will test both vertical and horizontal
# images to see the connected gates

# 1. Horizontally

connected_gates = []
# Note : every element in connected_gates list is in this shape :
# [input_gate1 , input_gate2 ,output ,type]
# initializing connected_gates
for gate in range(len(detected_gates)):
    connected_gates.append([None, None, None, detected_gates[gate][4]])

# starting from here we are gonna see raltions betwee the gates
image_mat_horz = []

for first_obj in range(len(detected_gates) - 1):

    # Getting only 2 gates in an image
    for second_obj in range(first_obj + 1, len(detected_gates)):

        # ***************** Getting the coordinates of point 1,2 ****************
        x_first_object = (detected_gates[first_obj][2] + detected_gates[first_obj][0]) / 2
        x_second_object = (detected_gates[second_obj][2] + detected_gates[second_obj][0]) / 2
        y_first_object = (detected_gates[first_obj][3] + detected_gates[first_obj][1]) / 2
        y_second_object = (detected_gates[second_obj][3] + detected_gates[second_obj][1]) / 2

        point1 = (x_first_object, y_first_object)
        point2 = (x_second_object, y_second_object)

        mask = np.ones([rows, cols])

        # Will delete all gates except for our two gates
        for x in range(len(detected_gates)):
            if x != first_obj and x != second_obj:
                mask[detected_gates[x][1]: detected_gates[x][3] + 1, detected_gates[x][0]: detected_gates[x][2] + 1] = 0

        # E7na kda b2a m3ana image feeha only 2 gates
        edited_image_1 = cv2.bitwise_and(src1=np.array(cut_img_horizontally), src2=mask)

        # Will cut any large point left to both the gates
        for point in range(len(centroids_large_points)):
            if point == 0:
                continue
            point_x = int(centroids_large_points[point][0])
            point_y = int(centroids_large_points[point][1])
            if point_x < x_first_object and point_x < x_second_object:
                edited_image_1[point_y - 10: point_y + 10, point_x - 10: point_x + 10] = 0

        edited_image_1 = np.uint8(edited_image_1)
        # Append it to image_mat_horz
        image_mat_horz.append(edited_image_1)

        # =============We will see if these two objects are connected or not=====================

        # /////////**************************************************/////////////
        # Mn awel hna da mkan el connectedComponentsWithStats 34an lw 7abb arg3ha tany
        # /////////**************************************************/////////////

        # ************** Getting the contours ***********************
        # Read in the image
        image = edited_image_1.copy()

        binary = image.copy()

        # Find contours from thresholded, binary image
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw all contours on a copy of the original image
        # contours_image = cv2.drawContours(contours_image, contours, -1, (0,255,0), 3)

        # See if the two objects are contained within a connected component
        for label in range(len(contours)):

            if cv2.pointPolygonTest(contours[label], point1, False) == 1 and \
                    cv2.pointPolygonTest(contours[label], point2, False) == 1:

                # print(str(first_obj)+" " +str(second_obj)+" are connected")

                # Hena hn2ol anhy gate input w anhy output
                if x_first_object > x_second_object:
                    if connected_gates[first_obj][0] == None:
                        connected_gates[first_obj][0] = str(second_obj)
                    else:
                        if connected_gates[first_obj][1] == None:
                            connected_gates[first_obj][1] = str(second_obj)
                else:
                    if connected_gates[second_obj][0] == None:
                        connected_gates[second_obj][0] = str(first_obj)
                    else:
                        if connected_gates[second_obj][1] == None:
                            connected_gates[second_obj][1] = str(first_obj)
                # print(str(first_obj) +str(second_obj) + "are connected" )
                break

# print(connected_gates)

# plt.imshow(cut_img_horizontally , cmap = 'gray')

# plt.imshow(img , cmap = 'gray')

# 2. Vertically

for first_obj in range(len(detected_gates) - 1):

    # Getting only 2 gates in an image
    for second_obj in range(first_obj + 1, len(detected_gates)):

        # ***************** Getting the coordinates of point 1,2 ****************
        x_first_object = (detected_gates[first_obj][2] + detected_gates[first_obj][0]) / 2
        x_second_object = (detected_gates[second_obj][2] + detected_gates[second_obj][0]) / 2
        y_first_object = (detected_gates[first_obj][3] + detected_gates[first_obj][1]) / 2
        y_second_object = (detected_gates[second_obj][3] + detected_gates[second_obj][1]) / 2

        point1 = (x_first_object, y_first_object)
        point2 = (x_second_object, y_second_object)

        mask = np.ones([rows, cols])

        for x in range(len(detected_gates)):
            if x != first_obj and x != second_obj:
                mask[detected_gates[x][1]: detected_gates[x][3] + 1, detected_gates[x][0]: detected_gates[x][2] + 1] = 0

        # E7na kda b2a m3ana image feeha only 2 gates
        edited_image_1 = cv2.bitwise_and(src1=np.array(cut_img_vertically), src2=mask)

        # Will cut any large point left to both the gates
        for point in range(len(centroids_large_points)):
            if point == 0:
                continue
            point_x = int(centroids_large_points[point][0])
            point_y = int(centroids_large_points[point][1])
            if point_x < x_first_object and point_x < x_second_object:
                edited_image_1[point_y - 10: point_y + 10, point_x - 10: point_x + 10] = 0

        edited_image_1 = np.uint8(edited_image_1)
        # Append it to image_mat_horz
        image_mat_horz.append(edited_image_1)

        # =============We will see if these two objects are connected or not=====================

        # /////////**************************************************/////////////
        # Mn awel hna da mkan el connectedComponentsWithStats 34an lw 7abb arg3ha tany
        # /////////**************************************************/////////////

        # ************** Getting the contours ***********************
        # Read in the image
        image = edited_image_1.copy()

        binary = image.copy()

        # Find contours from thresholded, binary image
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw all contours on a copy of the original image
        # contours_image = cv2.drawContours(contours_image, contours, -1, (0,255,0), 3)

        # See if the two objects are contained within a connected component
        for label in range(len(contours)):

            if cv2.pointPolygonTest(contours[label], point1, False) == 1 and \
                    cv2.pointPolygonTest(contours[label], point2, False) == 1:

                # Bdam da5alt hena yb2a ana mota2aked enhom connected
                # print(str(first_obj)+" " +str(second_obj)+" are connected")

                # If one of the two gates is not gate , we can to check its first input , if it
                # is not non , then continue

                # Hena hn2ol anhy gate input w anhy output
                if x_first_object > x_second_object:
                    if connected_gates[first_obj][0] == None:
                        connected_gates[first_obj][0] = str(second_obj)
                    else:
                        if connected_gates[first_obj][3] != 3:
                            if connected_gates[first_obj][1] == None \
                                    and connected_gates[first_obj][0] != str(second_obj):
                                connected_gates[first_obj][1] = str(second_obj)
                else:
                    if connected_gates[second_obj][0] == None:
                        connected_gates[second_obj][0] = str(first_obj)
                    else:
                        if connected_gates[second_obj][3] != 3:
                            if connected_gates[second_obj][1] == None \
                                    and connected_gates[second_obj][0] != str(first_obj):
                                connected_gates[second_obj][1] = str(first_obj)
                # print(str(first_obj) +str(second_obj) + "are connected" )
                break

# print(connected_gates)

# plt.imshow(cut_img_vertically , cmap = 'gray')

# plt.imshow(cut_img_horizontally , cmap = 'gray')

# print(detected_gates)

# plt.imshow(img , cmap = 'gray')

# Now let's sort the gates so that the gates that takes inputs from user are listed
# from top to bottom
sorted_initial_gates = []
input_gates = []
for gate in range(len(connected_gates)):
    if connected_gates[gate][3] == 3 and connected_gates[gate][0] == None:
        input_gates.append(detected_gates[gate] + [gate])
    elif connected_gates[gate][3] != 3 and (connected_gates[gate][0] == None or connected_gates[gate][1] == None):
        input_gates.append(detected_gates[gate] + [gate])

# I sort them
detected_objects_sorted = input_gates.sort(key=lambda x: x[1])
for gate in input_gates:
    sorted_initial_gates.append(connected_gates[gate[5]])

'''
for gate in connected_gates :
     if gate not in sorted_connected_gates:
          sorted_connected_gates.append(gate)
'''

# print(sorted_initial_gates)

# plt.imshow(img , cmap='gray')


# ******************************************************************************************************************* #
# Starting from here , we are calculating the truth table
# ******************************************************************************************************************* #

from AND import AND
from OR import OR
from NOT import NOT
from XOR import XOR
import copy

'''
connected_gates = [ [None , None , None , 0] ,
                   [None , None , None , 1] ,
                   [str(0) , str(1) , None , 0],
                   [str(0) , str(1) , None , 1]]

connected_gates = [[None, None, None , 3],
                  [None , None , None , 0],
                  ["0", "1", None , 1]]
'''
connected_gates = [['2', '5', None, 0],
                   [None, None, None, 0],
                   ['1', '3', None, 1],
                   [None, None, None, 2],
                   ['1', None, None, 2],
                   ['4', None, None, 3]]

sorted_initial_connected_gates = [[None, None, None, 2], [None, None, None, 0], ['1', None, None, 2]]

input_indices = []

Gates = []
final_truth_table = []
input_counter = 0
starting_gates = []
inputs_table = []
Gates_original = []
Not_output_gates = set()
names_of_inputs = []
gate_type = ["and", "or", "xor", "not"]
inputGates = []

# Get the indices of the input gates in the Gates list
for gate in sorted_initial_connected_gates:
    input_indices.append(connected_gates.index(gate))

# E7na hena bn3ml objects mn el classes elly 3ndna
for i in range(len(connected_gates)):

    if connected_gates[i][3] == 0:
        Gates.append(AND(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
    elif connected_gates[i][3] == 1:
        Gates.append(OR(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
    elif connected_gates[i][3] == 2:
        Gates.append(XOR(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
    elif connected_gates[i][3] == 3:
        Gates.append(NOT(connected_gates[i][0], connected_gates[i][2], connected_gates[i][3]))

# Hena bn7dd 3ndna kam input
gate_index = 0

for index in input_indices:
    if Gates[index].gtype == 3:

        if Gates[index].input1 == None:
            input_counter += 1
            starting_gates.append(gate_index)
            names_of_inputs.append(gate_type[Gates[index].gtype] + " inp1")
    else:

        if (Gates[index].input1 == None) and (Gates[index].input2 == None):
            input_counter += 2
            starting_gates.append(gate_index)
            names_of_inputs.append(gate_type[Gates[index].gtype] + " inp1")
            names_of_inputs.append(gate_type[Gates[index].gtype] + " inp2")
        elif ((Gates[index].input1 == None) and (Gates[index].input2 != None)):
            input_counter += 1
            starting_gates.append(gate_index)
            names_of_inputs.append(gate_type[Gates[index].gtype] + " inp1")
        elif ((Gates[index].input1 != None) and (Gates[index].input2 == None)):
            input_counter += 1
            starting_gates.append(gate_index)
            names_of_inputs.append(gate_type[Gates[index].gtype] + " inp1")

# print(input_counter)

# Hena hn7dd anhy gates elly hzhar 3nha input

for myGate in Gates:
    if myGate.gtype == 3:
        Not_output_gates.add(myGate.input1)
    else:
        Not_output_gates.add(myGate.input1)
        Not_output_gates.add(myGate.input2)

# Hn3ml elinputs table
for inputNumber in range(2 ** input_counter):
    input_element = []
    for shift in range(input_counter):
        input_element.append((inputNumber >> (input_counter - shift - 1)) & 0x1)
    inputs_table.append(input_element)

'''
for element in inputs_table :
    print(element)
'''

# We will calculate the output for each input in tht truth table

for iteration in range(2 ** input_counter):
    inputNumber = 0
    Gates = []

    # Gates = copy.copy(Gates_original)

    for i in range(len(connected_gates)):

        if connected_gates[i][3] == 0:
            Gates.append(
                AND(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
        elif connected_gates[i][3] == 1:
            Gates.append(OR(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
        elif connected_gates[i][3] == 2:
            Gates.append(
                XOR(connected_gates[i][0], connected_gates[i][1], connected_gates[i][2], connected_gates[i][3]))
        elif connected_gates[i][3] == 3:
            Gates.append(NOT(connected_gates[i][0], connected_gates[i][2], connected_gates[i][3]))

    gates_with_output_eq_None = []
    gates_with_output_eq_None = copy.copy(Gates)  # Shallow copy

    # Assign the input values to the gates
    for index in input_indices:
        if (Gates[index].input1 == None):
            if Gates[index].gtype == 3:
                Gates[index].input1 = inputs_table[iteration][inputNumber]
                inputNumber += 1
            else:
                if (Gates[index].input2 == None):
                    Gates[index].input1 = inputs_table[iteration][inputNumber]
                    Gates[index].input2 = inputs_table[iteration][inputNumber + 1]
                    inputNumber += 2
                else:
                    Gates[index].input1 = inputs_table[iteration][inputNumber]
                    inputNumber += 1
        else:
            if Gates[index].gtype != 3:
                if Gates[index].input2 == None:
                    Gates[index].input2 = inputs_table[iteration][inputNumber]
                    inputNumber += 1

    gates_with_output_eq_None = []
    gates_with_output_eq_None = copy.copy(Gates)  # Shallow copy

    # print("=======================================================================")
    # print("len after for loop" + " " + str(len(gates_with_output_eq_None)))

    # print(len(gates_with_output_eq_None))

    # hena b2a hn7sb el output bta3 kol gate
    while len(gates_with_output_eq_None) != 0:
        # for test in range(2) :
        # print("Entered while loop")
        # print(len(gates_with_output_eq_None))
        for myGate in gates_with_output_eq_None:
            if myGate.gtype == 3:
                if myGate.output != None:
                    continue
                if myGate.input1 != 1 and myGate.input1 != 0:
                    if myGate.input1 != None:
                        index = int(myGate.input1)
                        if Gates[index].output != None:
                            myGate.input1 = Gates[index].output
                        if myGate.input1 == 1 or myGate.input1 == 0:
                            myGate.calc()
                            gates_with_output_eq_None.remove(myGate)
                elif myGate.input1 == 1 or myGate.input1 == 0:
                    myGate.calc()
                    gates_with_output_eq_None.remove(myGate)

            else:
                if myGate.output != None:
                    continue

                # if ((myGate.input1 != 1) and (myGate.input1 != 0)) or ((myGate.input2 != 1) and (myGate.input2 != 0)):
                if myGate.input1 != None and myGate.input1 != 1 and myGate.input1 != 0:
                    index1 = int(myGate.input1)
                    if Gates[index1].output != None:
                        myGate.input1 = Gates[index1].output

                if myGate.input2 != None and myGate.input2 != 1 and myGate.input2 != 0:
                    index2 = int((myGate.input2))
                    if Gates[index2].output != None:
                        myGate.input2 = Gates[index2].output

                if ((myGate.input1 == 1) or (myGate.input1 == 0)) and ((myGate.input2 == 1) or (myGate.input2 == 0)):
                    # print("input has a complete value")
                    myGate.calc()
                    gates_with_output_eq_None.remove(myGate)

                elif ((myGate.input1 == 1) or (myGate.input1 == 0)) and ((myGate.input2 == 1) or (myGate.input2 == 0)):
                    myGate.calc()
                    gates_with_output_eq_None.remove(myGate)

    '''
        print("The gate start")
        for i in range(len(Gates)):
            if Gates[i].gtype == 3:
                print(str(Gates[i].input1) + " " + str(Gates[i].output) + " " + str(Gates[i].gtype))
            else:
                print(str(Gates[i].input1) + " " + str(Gates[i].input2) + " " + str(Gates[i].output) + " " + str(Gates[i].gtype))
        print("The gate end")
    '''

    output_elements = []
    output_elements.append(inputs_table[iteration])
    for myGate in range(len(Gates)):
        if str(myGate) not in Not_output_gates:
            output_elements.append(Gates[myGate].output)
    final_truth_table.append(output_elements)

# print("finisheeeeeeeeeeed")

# print(Not_output_gates)
#print(len(final_truth_table))
#print(names_of_inputs)
#for element in final_truth_table:
#    print(element)

'''
    print("The gate start")
    for i in range(len(connected_gates)):
        if Gates[i].gtype == 3:
            print(str(Gates[i].input1) + " " + str(Gates[i].output) + " " + str(Gates[i].gtype))
        else:
            print(str(Gates[i].input1) + " " + str(Gates[i].input2) + " " + str(Gates[i].output) + " " + str(
                Gates[i].gtype))
    print("The gate end")
    '''

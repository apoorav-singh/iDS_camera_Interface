import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
import os 
import glob
import shutil



# -------------------------------------------------------------------------------------------------------------------------------------------------
# Capturing Date and time
# -------------------------------------------------------------------------------------------------------------------------------------------------

import time
date_v = time.strftime("%d_%m_%Y")
def time_v(): return time.strftime("%H_%M_%S")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Folder and Path Management
# -------------------------------------------------------------------------------------------------------------------------------------------------

def latest_file(path_aft):
    list_of_files = glob.glob(os.getcwd()+"/"+path_aft+"/*") # * means all 
    if (list_of_files == None):
        return []
    else:
        return max(list_of_files, key=os.path.getctime)

# ------------------------------------------------------
dir_list = os.listdir()

file_found = 0

for i in dir_list:
    if (i == "Reference"):
        file_found += 1
    
    elif (i == "Saved"):
        file_found += 2 
    
    else:
        print("Files were found")


if (file_found == 2):
    print('No Refrence Directory found')
    os.mkdir("Reference")
    print('Directory successfully created')

elif (file_found == 1):
    print('No Saved Directory found')
    os.mkdir("Saved")
    os.mkdir("Saved/Clicked")
    os.mkdir("Saved/Substracted")
    print('Directory successfully created')

elif (file_found == 0):
    print('Null Directory')
    os.mkdir("Reference")
    os.mkdir("Saved")
    os.mkdir("Saved/Clicked")
    os.mkdir("Saved/Substracted")
    print('Directory(ies) successfully created')

else:
    print("Inconsistent Files: May be multiple directories with the same name.")


# ------------------------------------------------------

file_found = 0

print(os.getcwd())
os.chdir("Saved/Clicked")
dir_list = os.listdir()

if (len(dir_list) == 0):
    os.mkdir(date_v)

for i in dir_list:
    if (i == date_v):
        file_found += 1
        break
        
    else:
        print("Directory not found")
        

if (file_found == 0):
    print("Files was not found")
    os.mkdir(date_v)
    print("Files were created")


# ------------------------------------------------------
file_found = 0

os.chdir("..")
os.chdir("..")
os.chdir("Saved/Subtracted")
dir_list = os.listdir()

if (len(dir_list) == 0):
    os.mkdir(date_v)

for i in dir_list:
    if (i == date_v):
        file_found += 1
        break
        
    else:
        print("Directory not found")
        

if (file_found == 0):
    print("Files was not found")
    os.mkdir(date_v)
    print("Files were created")

# ------------------------------------------------------

file_found = 0

os.chdir("..")
os.chdir("..")
os.chdir("Saved/Comparison")
dir_list = os.listdir()

if (len(dir_list) == 0):
    os.mkdir(date_v)

for i in dir_list:
    if (i == date_v):
        file_found += 1
        break
        
    else:
        print("Directory not found")
        

if (file_found == 0):
    print("Files was not found")
    os.mkdir(date_v)
    print("Files were created")

# ------------------------------------------------------
    
file_found = 0

os.chdir("..")
os.chdir("..")
os.chdir("Reference")
dir_list = os.listdir()

if (len(dir_list) == 0):
    os.mkdir(date_v)

for i in dir_list:
    if (i == date_v):
        file_found += 1
        break
        
    else:
        print("Directory not found")
        

if (file_found == 0):
    print("Files was not found")
    os.mkdir(date_v)
    shutil.copy2('pot.png', 'Reference/'+date_v+"/")
    print("Files were created")
    
file_found = 0

os.chdir("..")


print("Current Working Directory: ", os.getcwd())



# -------------------------------------------------------------------------------------------------------------------------------------------------
# Initial Parameters for GUI
# -------------------------------------------------------------------------------------------------------------------------------------------------


dpg.create_context()
dpg.create_viewport(title='Imaging System Application - CAQT', width=600, height=800)
dpg.setup_dearpygui()

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Image capture from Imaging System
# -------------------------------------------------------------------------------------------------------------------------------------------------


vid = cv.VideoCapture(0)
ret, frame = vid.read()

data = np.flip(frame, 2)  # because the camera data comes in as BGR and we need RGB
data = data.ravel()  # flatten camera data to a 1 d stricture
data = np.asfarray(data, dtype='f')  # change data type to 32bit floats
texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU

with dpg.texture_registry(show=True):
    dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag="Live", format=dpg.mvFormat_Float_rgb)

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Reference Image
# -------------------------------------------------------------------------------------------------------------------------------------------------

def func_ref():
    reference_img = cv.imread(latest_file("Reference/"+date_v))
    data_ref = np.flip(reference_img, 2)  # because the camera data comes in as BGR and we need RGB
    data_ref = data_ref.ravel()  # flatten camera data to a 1 d stricture
    data_ref = np.asfarray(data_ref, dtype='f')  # change data type to 32bit floats
    texture_data = np.true_divide(data_ref, 255.0)  # normalize image data to prepare for GPU
    return reference_img, texture_data

with dpg.texture_registry(show=True):
    reference_img, texture_data_1 = func_ref()
    dpg.add_raw_texture(reference_img.shape[1], reference_img.shape[0], texture_data_1, tag="Ref", format=dpg.mvFormat_Float_rgb)

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Subtracted  Image
# -------------------------------------------------------------------------------------------------------------------------------------------------

def click_function():
    dpg.save_image(file="Saved/Clicked/"+date_v+"/"+time_v()+".png", width=frame.shape[1], height=frame.shape[0], data=data, components=3)
    m1 = latest_file("Reference/"+date_v)
    m2 = latest_file("Saved/Clicked/"+date_v)
    im_1 = cv.imread(m1)
    im_2 = cv.imread(m2)
    # subtract the images
    sub = cv.subtract(im_1, im_2)
    # TO show the output
    cv.imwrite("Saved/Subtracted/"+date_v+"/"+time_v()+".png", sub)
# def sub_function():
#     reference_img = cv.imread(latest_file("Saved/Subtracted/"+date_v))
#     data_ref = np.flip(reference_img, 2)  # because the camera data comes in as BGR and we need RGB
#     data_ref = data_ref.ravel()  # flatten camera data to a 1 d stricture
#     data_ref = np.asfarray(data_ref, dtype='f')  # change data type to 32bit floats
#     texture_data = np.true_divide(data_ref, 255.0)  # normalize image data to prepare for GPU
#     return reference_img, texture_data

# with dpg.texture_registry(show=True):
#     reference_img_2, texture_data_2 = sub_function()
#     dpg.add_raw_texture(reference_img_2.shape[1], reference_img_2.shape[0], texture_data_2, tag="Sub", format=dpg.mvFormat_Float_rgb)   

# -------------------------------------------------------------------------------------------------------------------------------------------------
# GUI 
# -------------------------------------------------------------------------------------------------------------------------------------------------
    

with dpg.window(label="Live Preview"):
    dpg.add_text("Live Preview from iDS Camera")
    dpg.add_image("Live")
    dpg.add_button(label="CLICK", callback=click_function)
with dpg.window(label="Refrence Preview"):
    dpg.add_text("Reference Image")
    dpg.add_image("Ref")
    dpg.add_button(label="SWAP REF", callback=lambda:dpg.save_image(file="Reference/"+date_v+"/"+time_v()+".png", width=frame.shape[1], height=frame.shape[0], data=data, components=3))
# with dpg.window(label="Subtraction"):
#     dpg.add_text("Subtracted Image")
#     dpg.add_image("Sub")
    


# dpg.show_metrics()
dpg.show_viewport()

while dpg.is_dearpygui_running():

    # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
    # commenting out the "ret, frame = vid.read()" line will show the full speed that operations and updating a texture can run at
    
    ret, frame = vid.read()
    data = np.flip(frame, 2)
    data = data.ravel()
    data = np.asfarray(data, dtype='f')
    texture_data = np.true_divide(data, 255.0)
    dpg.set_value("Live", texture_data)
    reference_img_1, texture_data_1 = func_ref()
    dpg.set_value("Ref", texture_data_1)
    # reference_img_2, texture_data_2 = sub_function()
    # dpg.set_value("Sub", texture_data_2)

    # to compare to the base example in the open cv tutorials uncomment below
    # cv.imshow('reference_image', frame)
    dpg.render_dearpygui_frame()

vid.release()
# cv.destroyAllWindows() # when using upen cv window "imshow" call this also
dpg.destroy_context()
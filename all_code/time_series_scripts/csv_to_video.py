import os 
import cv2 
import pandas as pd 
import matplotlib.pyplot as plt 

# event point to pictures
''' 
Draw a group of pictures with 2,000 incident points,
and synthesize video with a standard of 15 frame rate 15 
'''

def create_folder_if_not_exists(folder_path):
    # use os.path.exist() to check whether the path exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        ...
    ...

def draw_and_save(x, y, pic_path):
    plt.figure(figsize=(10, 6), dpi=100)
    plt.xlim(0, 128)
    plt.ylim(128, 0)
    plt.axis('off')
    plt.scatter(x, y, s=1) 
    plt.savefig(pic_path)
    plt.close()
    ...

def event_to_pic(file_name, event_count = 2000):
    # create a folder of the same name 
    create_folder_if_not_exists(f'../../video/artificial/{file_name}/')
    df = pd.read_csv(f'../../event_csv/split_data/artificial/{file_name}.csv')
    start =  0
    end = event_count 
    count = 1 
    # explain that it has not been traveled yet 
    while end < df.shape[0]:
        # do not take time stamp 
        temp = df.iloc[start : end, 1 : 3]
        draw_and_save(temp['x'], temp['y'], f'../../video/artificial/{file_name}/{count}.jpg')
        start = end 
        end = end + event_count 
        count = count + 1 

    temp = df.iloc[start:, 1:3]
    draw_and_save(temp['x'], temp['y'], f'../../video/artificial/{file_name}/{count}.jpg')

# picture transfer video 

def sort_key(item):
    return int(item[:-4])

def pic_to_video(images_folder, output_video):
    # get all the picture files in the folder 
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg')]
    image_files = sorted(image_files,key=sort_key)
    # Get the size of the first picture, as the size of the video frame
    first_image = cv2.imread(os.path.join(images_folder, image_files[0]))
    frame_size = (first_image.shape[1], first_image.shape[0])

    # Set video parameters
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 15

    # Create video writing objects
    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    # Traversen the picture file, write each picture to the video
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)
    # Release resources
    out.release()
    cv2.destroyAllWindows()
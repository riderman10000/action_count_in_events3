import cv2 
import time 
import numpy as np 
import pandas as pd 

import tools as tl 



def save_event_as_video(events, name,
    event_points = None, width = 128, height = 128,
    threshold = 0.9, decay = 0.005, image_scale = 2,
    frame_per_second = 1/60 ): # frame per second 
    # create image 
    image = np.zeros((height, width, 3), dtype=np.uint16)
    
    if event_points:
        events = events[:event_points]
    
    prev_x, prev_y, prev_time = 0, 0, 0 
    
    peak, spike = 255, 255 
    
    video_writer = cv2.VideoWriter(
        name,
        # apiPreference=cv2.CAP_FFMPEG,
        cv2.VideoWriter_fourcc (*'MJPG'), # (*'H264'), # (*'XVID'), #
        60, (width, height)
    )
    
    for event_idx, event in enumerate(events):
        time_stamp, x, y = event[0], int(event[1]), int(event[2])
        
        if not tl.is_with_in_manhattan_distance(prev_x, prev_y, x, y):
            prev_x, prev_y = x, y 
            continue
        prev_x, prev_y = x, y 
        
        # spike of the neuron 
        image[y, x] = spike 
        
        # decay of the neuron
        image = image - (decay * image ) #* (time_stamp - prev_time))
        image[image < 0] = 0 
        
        print(event_idx, image.max())
        image_display = image.astype(np.uint8)
        
        cv2.imshow('test', cv2.resize(image_display, (width * image_scale, height * image_scale)))
        
        if ((time_stamp - prev_time) >  (frame_per_second * 1000)):
            video_writer.write(image_display) 
            prev_time = time_stamp 
        
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        
        ...

    cv2.destroyAllWindows()
    video_writer.release() 


def get_event_frame(events,
    event_points = None, width = 128, height = 128,
    threshold = 0.9, decay = 0.005, image_scale = 2,
    frame_per_second = 1/60 , event_time_include = False): # seconds per frame 
    image = np.zeros((height, width), dtype=np.uint8)
    
    if event_points:
        events = events[:event_points]

    prev_x, prev_y, prev_time = 0, 0, 0 
    peak, spike = 1, 1 # 255, 255 
    
    for event_idx, event in enumerate(events):
        time_stamp, x, y = event[0], int(event[1]), int(event[2])
        
        if not tl.is_with_in_manhattan_distance(prev_x, prev_y, x, y):
            prev_x, prev_y = x, y 
            continue
        prev_x, prev_y = x, y 

        # spike of the neuron 
        image[y, x] = spike

        # decay of the neuron
        image = image - (decay * image ) #* (time_stamp - prev_time))
        image[image < 0] = 0 

        if ((time_stamp - prev_time) >  (frame_per_second * 1000)):
            yield image 

            # if event_time_include:
            #     print(f"[time stamp] -- timestamp {time_stamp}  -- prevstamp -- {prev_time} -- diff {((time_stamp - prev_time)/1000)}")
            #     time.sleep((time_stamp - prev_time)/1000)
            prev_time = time_stamp 
        
    
if __name__ == "__main__":
    
    # load event camera data 
    events = tl.load_event_data(
        # './event_csv/split_data/artificial/a_b7_a.csv') # Replace with your actual file path
        './event_csv/split_data/class5/user02_led.csv')  # Replace with your actual file path
    save_event_as_video(events, 'test.mp4', frame_per_second=1/60)
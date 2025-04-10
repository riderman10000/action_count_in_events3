import numpy as np 
import pandas as pd 
import cv2 

import tools as tl 
import e2v 

def segment_event(events, new_csv_file, event_points=None):
    
    height, width = 128, 128 # event camera resolution 
    # create image 
    image = np.zeros((height, width, 3), dtype=np.uint16)
    
    if event_points:
        events = events[:event_points]
    
    image_scale = 1
    frame_per_second = 1/60 # frame per second 
    prev_x, prev_y, prev_time = 0, 0, 0 
    peak, spike = 255, 255
    decay = 0.005
    
    for event_idx, event in enumerate(events):
        time_stamp, x, y = event[0], int(event[1]), int(event[2]) 
        
        # spike of the neuron 
        image[y, x] = spike 
        
        # decay of the neuron
        image = image - (decay * image ) #* (time_stamp - prev_time))
        image[image < 0] = 0 
        
        print(event_idx, image.max())
        image_display = image.astype(np.uint8)
        
        cv2.imshow('test', cv2.resize(image_display, (width * image_scale, height * image_scale)))
        
        if ((time_stamp - prev_time) >  (frame_per_second * 1000)): 
            prev_time = time_stamp 
        
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            
        
        ...
    cv2.destroyAllWindows()
    
    
    # Create a DataFrame from the events
    df = pd.DataFrame(events, columns=['timestamp', 'x', 'y'])
    
    # Save the DataFrame to a CSV file
    df.to_csv(new_csv_file, index=False, header=False)


if __name__ == "__main__":
    # load event camera data 
    events = tl.load_event_data(
        # './event_csv/split_data/artificial/a_b7_a.csv') # Replace with your actual file path
        './event_csv/split_data/class5/user02_led.csv')  # Replace with your actual file path
    # save_event_as_video(events, 'test.mp4', frame_per_second=1/30)
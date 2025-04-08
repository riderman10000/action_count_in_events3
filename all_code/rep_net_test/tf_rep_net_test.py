import tensorflow as tf 
import tensorflow_hub as hub 

import cv2 

repnet_model = hub.load("https://tfhub.dev/google/repnet/1")

# load the video frames 
cap = cv2.VideoCapture("humming_bird.mp4")

# read from the video 
frames = [] 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break 
    
    frames.append(frame)
    
# convert frames to a fromat exprected by RepNet 
frame_tensor = tf.convert_to_tensor(frames, dtype=tf.float32)

# use repnet to count repetitions 
counts, per_frame_counts, _, _ = repnet_model.signatures['serving_default'](frame_tensor)

# output the repetition count 
print(f"repetitions: {counts.numpy()}")
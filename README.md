# 1. all_code

Store all code files, `main.ipynb` is the main function.

# 2. event_csv

Store csv files of all events after operation.

## 2.1 split_data

It stores the event csv data after cutting according to the action start and end labels indicated by the labels_clean folder, and the artificial folder stores the artificial synthetic event csv data.

## 2.2 compress_event_manhattan

It stores the event csv file after performing “Transforming events to time series” on the data in the split_data folder, and the artificial folder stores the event csv file after processing the artificial synthetic data.

### smooth_by_pca

It store the event csv file after "Extracting features of key action trail" data from the compress_event_manhattan folder. 

#### compress_by_mean

It store the event csv file after "Smoothing key trail" data from the smooth_by_pca folder. 

# 3. labels

## 3.1 gesture_mapping.csv

Holds a mapping between class categories and action names.

## 3.2 labels_orginal

Store the initial label of the [DvsGesture Dataset](https://research.ibm.com/interactive/dvsgesture/), which indicates the beginning and end timestamps of each class of actions.

## 3.3 labels_clean

Store the label data after cleaning labels_orginal folder, and the specific operation is the timestamp of the start and end of all actions minus the timestamp of the first action start.

# 4. video

## 4.1 nature

Store user02 class2, 4-7 action for video files.

## 4.2 artificial

Frames containing synthetic data, each containing 2000 event points.

## 4.3 artificial_video

Storage of artificial folder each frame in the synthesis of video files, frame rate to 15.

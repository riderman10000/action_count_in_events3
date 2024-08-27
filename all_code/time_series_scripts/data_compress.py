import numpy as np 
import pandas as pd 
import statsmodels.api as sm 
from sklearn.decomposition import PCA 

# manhattan compression 

# manhattan distance with two coordinates 
def compute_distance(x1,y1,x2,y2):
    return abs(x1-x2),abs(y1-y2)

# By comparing with the next event point, determine whether the current event point is noise
def is_noise(row,next_event,delta):
    # The next point of the current point is too far away and count == 1, then the current point is considered a noise point
    x_dis,y_dis = compute_distance(row[1],row[2],next_event[1],next_event[2])
    # The current event point is noise, skipping does not enter
    if x_dis > delta or y_dis > delta:
        # Noise point
        return True
    else:
        return False
    
# Write the aggregation point into the CSV file
def write_to_csv(temp_x,temp_y,count,path):
    pd.DataFrame(data=[[temp_x/count,temp_y/count]]).to_csv(
        path, mode='a', header=False, index=False)

# Select the starting point of the cluster
def select_start_point(df: pd.DataFrame, delta):
    for index,row in df.iterrows():
        d1,d2 = compute_distance(row[1],row[2],df['x'][index+1],df['y'][index+1])
        if d1 <= delta and d2 < delta:
            # Explain that there are other points around the current point, the probability is not the noise point
            return index,row   
        
# manhattan compression 
def compress_by_Manhattan(file_name,class_num,delta=5,count_margin=100,nature_flag=True):
    file_path = None
    to_file_path = None
    # Natural data path
    if nature_flag:
        file_path = f'../../event_csv/split_data/class{class_num}/{file_name}'
        to_file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/{file_name}'
    # Artificial synthesis data path
    else:
        file_path = f'../../event_csv/split_data/artificial/{file_name}'
        to_file_path = f'../../event_csv/compress_event_manhattan/articicial/{file_name}'  
    
    # df = pd.read_csv(file_path, skiprows=1)
    df = pd.read_csv(file_path)

    # manhattan distance comparison object [the initial point may be noise point]
    start, row = select_start_point(df, delta)
    # row[0] is the timestamp column 
    baseline_x = row[1]
    baseline_y = row[2] 

    # manhattan distance to be written 
    temp_x = 0
    temp_y = 0 
    count = 0 
    pd.DataFrame(data=[['x', 'y']]).to_csv(to_file_path, mode='w', header=False, index=False)
    # travel every line 
    for index, row in df.iterrows():
        if index < start:
            continue
        # at the distance from manhattan, gather at a point, take the average  value 
        x_dis, y_dis = compute_distance(baseline_x, baseline_y, row[1], row[2])
        # focus on up to count_margin a point 
        if x_dis <= delta and y_dis <= delta and count < count_margin:
            # denominator of average 
            count = count + 1 
            temp_x = temp_x + row[1] 
            temp_y = temp_y + row[2]
        else: 
            # arrive at the last event point location 
            if index + 1 >= df.shape[0]:
                if count > 1 : 
                    write_to_csv(temp_x, temp_y, count, to_file_path)
                break
            next_event = df.iloc[index + 1]
            # the next point of the current point is too far away and count == 1, 
            # then the current point is considered a noise point 
            if count ==1 and is_noise(row, next_event, delta):
                # The current event point is noise and will be skipped and not entered.
                continue
            write_to_csv(temp_x, temp_y, count, to_file_path)
            baseline_x = row[1] 
            baseline_y = row[2] 
            temp_x = row[1] 
            temp_y = row[2] 
            count = 1

# PCA main component 
def PCA_method(data: pd.DataFrame):
    # get the NDarray form of dataframe 
    data = data.values 
    # one - dimensional 
    pca = PCA(n_components=1) 
    # apply PCA to data 
    pca_data = pca.fit_transform(data)
    pca_data = np.reshape(pca_data, -1)
    # HP filter 
    _, smooth = sm.tsa.filters.hpfilter(pca_data) 
    return smooth

# PCA 
def dimensionality_reduction_PCA(file_name,class_num,nature_flag=True):
    df = None 
    to_file_path = None 
    if nature_flag:
        # Data after time and space filtration
        df = pd.read_csv(f'../../event_csv/compress_event_manhattan/class{class_num}/{file_name}')
        to_file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/{file_name}'
    else:
        df = pd.read_csv(f'../../event_csv/compress_event_manhattan/articicial/{file_name}')
        to_file_path = f'../../event_csv/compress_event_manhattan/articicial/smooth_by_pca/{file_name}'
    # PCA main component analysis, as long as the first dimension 
    data = PCA_method(df) 
    pd.DataFrame(data, columns=['value']).to_csv(
        to_file_path, mode='w', header=True, index=False)
    
# Mean compression 
def compress_by_mean(file_name, class_num, chunksize = 100, nature_flag = True):
    file_path = None 
    to_file_path = None 
    if nature_flag:
        file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/{file_name}'
        to_file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/compress_by_mean/{file_name}'
    else: 
        # artificial synthesis data path 
        file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/{file_name}'
        to_file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/compress_by_mean/{file_name}'
    
    df = pd.read_csv(file_path, chunksize=chunksize, usecols=['value'])
    pd.DataFrame(data=[['value']]).to_csv(
        to_file_path, mode='w', header=False, index=False)
    
    for chunk in df:
        temp = pd.DataFrame([chunk.mean()])
        temp.to_csv(
            to_file_path, index=False, header=False, mode='a')

# two-person integration 
# waveform smooth 
def distance_mean_meanline(file_name,class_num=-1,delta=5,count=100,mean_count=100,nature_flag=True):
    # Manhattan distance compression
    compress_by_Manhattan(file_name,class_num,delta=delta,count_margin=count,nature_flag=nature_flag)
    # PCA + HP filter
    dimensionality_reduction_PCA(file_name,class_num,nature_flag=nature_flag)
    # Average compression
    compress_by_mean(file_name,class_num,chunksize=mean_count,nature_flag=nature_flag)
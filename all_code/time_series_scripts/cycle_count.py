import numpy as np 
import pandas as pd 
from fastdtw import fastdtw
import pymannkendall as mk

# find a monotonous jumping point 

# through Mann-kendall as a monotonous judgement standard 
# data is the time sequence server  -- dynamic candidate selection 
def get_index_of_bottom_and_top_by_mk(data):
    win_size = 10 
    step = 5 
    first = np.inf
    second = -np.inf
    flag = True 
    final_win_change = None
    while(second < first):
        # record the total number of pane divided 
        win_sum = int(1 + (data.shape[0] - win_size)/step if data.shape[0] > win_size else 0)
        # each pane starting index 
        win_start_index = np.arange(0, win_sum * step, step=step)
        # mutation pane index [Later processing as an intermediate index in the mniddle pane]
        win_change = np.array([])
        # current window trend [Increasing, Decreasing, No Trend]
        win_trend = np.array([])

        # traversion all pane 
        for i in range(win_sum):
            # pane data 
            win_data = data[win_start_index[i]: win_start_index[i] + win_size]
            # add  the current window trend 
            win_trend = np.append(win_trend, mk.original_test(win_data)[0])

        # traversing the trend of each pane 
        for i in range(1, win_trend.shape[0]):
            # the previous one is not increasing and the current is increasing, indicating that this is a mutation point 
            if win_trend[i] == 'increasing' and win_trend[i-1] != 'increasing':
                win_change = np.append(win_change, win_start_index[i-1])
            elif win_trend[i] == 'decreasing' and win_trend[i-1] != 'decreasing':
                win_change = np.append(win_change, win_start_index[i-1])

        # the window takes the intermediate value as the segmentation line 
        win_change = win_change + win_size / 2 
        win_change = win_change.astype(np.int32)
        # start and end teh division line 
        win_change = np.insert(win_change, 0, 0)
        # -1 prevent cross - border 
        win_change = np.append(win_change, data.shape[0] - 1)
        # the variance of currently dividing the pane 
        variance = np.var(np.diff(win_change)) 

        if flag:
            first = variance 
        else : 
            second = variance

        # it shows that the variance of the square difference at this time 
        # is greater than the difference in the previous cutting method.
        # select the previous cutting method as the final method 
        if second >= first:
            break 
        flag = not flag 
        win_size = win_size + 5 
        final_win_change = win_change 

    # the index is the starting label of the rising edge to 1 to 1 
    top_win = np.zeros(final_win_change.shape[0])
    if data[final_win_change[0]] <= data[final_win_change[1]]:
        top_win[0] = 1
    for i in range(1,final_win_change.shape[0]):
        if data[final_win_change[i-1]] >= data[final_win_change[i]]:
            top_win[i] = 1 
    return final_win_change,top_win,win_size,step 

# cycle count 
def get_count(result):
    count = 1 
    for i in range(result.shape[0]):
        # 0 without processing 
        if i == 0 or result[i] == 0 or result[i-1] == 0:
            continue 
        # the two errors are small, which is the same action
        if result[i] - result[i-1] <= 2 :
            count = count + 1
        # 0
        else:
            return count 
    return count 

# return time sequence rise/decrease along the average value of the price after the mutual comparison
def get_dtw_mean_cost(win_change, top_win, data):
    win_change_length = win_change.shape[0]
    # rising along the number 
    top_count = np.count_nonzero(top_win == 1)
    # drop along the number 
    bottom_count = top_win.shape[0] - top_count
    # storage rising along dtw comparison results 
    avg_cost_by_dtw_top = np.zeros(shape=(top_count, top_count))
    avg_cost_by_dtw_bottom = np.zeros(shape=(bottom_count, bottom_count))
    # rising/down index along the line 
    k_top = 0 
    k_bottom = 0 
    # column index 
    g_top = 0 
    g_bottom = 0 
    # guaranteed not to cross the border, bubbling comparison 
    for i in range(0, win_change_length - 1):
        # avoid repeated comparisons in the same paragraph 
        if top_win[i] == top_win[i+1]:
            continue
        # explain that i point to the beginning of the rising edge 
        if top_win[i] == 1 :
            g_top = k_top + 1 
        else:
            g_bottom = k_bottom + 1 
            
        for j in range(i+1, win_change_length -1 ):
            if top_win[j] == top_win[j+1]:
                continue
            
            # you need to let j point to the latter of i rising edge 
            if top_win[i] == 1 and top_win[j] == 1:
                # get the matching price of two time sequences 
                cost, _ = fastdtw(data[win_change[i]: win_change[i+1]], data[win_change[j] : win_change[j+1]])
                # stay in the comparison of the rising along the comparison
                num = data[win_change[j] : win_change[j+1]].shape[0] + data[win_change[i] : win_change[i+1]].shape[0]
                avg_cost_by_dtw_top[k_top][g_top] = cost/num 
                avg_cost_by_dtw_bottom[g_top][k_top] = cost/num 
                g_top = g_top + 1 
            elif top_win[i] == 0 and top_win[j] == 0:
                # get the matching price of two time sequences 
                cost, _ = fastdtw(data[win_change[i] : win_change[i+1]], data[win_change[j] : win_change[j+1]])
                # stay in the comparison of the rising along the comparison
                num = data[win_change[j] : win_change[j+1]].shape[0] + data[win_change[i] : win_change[i+1]].shape[0]
                avg_cost_by_dtw_bottom[k_bottom][g_bottom] = cost/num
                avg_cost_by_dtw_bottom[g_bottom][k_bottom] = cost/num 
                g_top = g_top + 1 
                
        if top_win[i] == 1:
            k_top = k_top + 1 
        else : 
            k_bottom = k_bottom + 1 
    
    # delete the fulll 0 line and the last 0 delete
    avg_cost_by_dtw_top = avg_cost_by_dtw_top[:-1, :-1]
    avg_cost_by_dtw_bottom = avg_cost_by_dtw_bottom[:-1, :-1]
    
    # replace your own comparison price to the average value of other numbers 
    for arr in avg_cost_by_dtw_top:
        if arr.shape[0] != 1:
            temp = np.sum(arr)/(arr.shape[0] - 1)
            arr[arr == 0] = temp 
    for arr in avg_cost_by_dtw_bottom:
        if arr.shape[0] != 1:
            temp = np.sum(arr)/(arr.shape[0] - 1)
            arr[arr == 0] = temp 
    
    result_top = np.array([])
    result_bottom = np.array([])
    if avg_cost_by_dtw_top.shape[0] != 0:
        result_top = np.sort(np.mean(avg_cost_by_dtw_top, axis=1))
    if avg_cost_by_dtw_bottom.shape[0] != 0:
        result_bottom = np.sort(np.mean(avg_cost_by_dtw_bottom, axis=1))
    
    # get the rising edge count 
    count_top = get_count(result_top) 
    # get the falling edge count 
    count_bottom = get_count(result_bottom)
    
    # return larger rising or falling edge count 
    return count_top if count_top > count_bottom else count_bottom


def get_count_by_cost(file_name, class_num = -1, nature_flag = True):
    file_path = None 
    if nature_flag:
        file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/compress_by_mean/{file_name}'
    else:
        # Artificial synthesis data
        file_path = f'../../event_csv/compress_event_manhattan/articicial/smooth_by_pca/compress_by_mean/{file_name}'
    # data after PCA and compress by mean 
    pca_data = pd.read_csv(file_path)['value']
    win_change, top_win, win_size, step = get_index_of_bottom_and_top_by_mk(pca_data)
    return get_dtw_mean_cost(win_change, top_win, pca_data)

# get all action cycle prediction infromation 
def get_all_count(file_names, nature_flag= True):
    # storage predictive value 
    pred_count = np.array([])
    if nature_flag:
        for i in range(2, 8):
            for name in file_names:
                if i == 3:
                    continue 
                count = get_count_by_cost(f'{name}', i)
                pred_count = np.append(pred_count, count)
                print(f"The file name is {name} middle class_num = {i} the number of repetitions of the action is: {count}")
            print("------------------------")
    else: 
        # artificial synthesis data 
        for name in file_names:
            count = get_count_by_cost(name, nature_flag=False) 
            pred_count = np.append(pred_count, count) 
            print(f"The file name is {name} the number of repetitions of the action is: {count}")
    return pred_count

# results criteria 

# Mean Absolute error, an average absolute error
def MAE(pred_count, real_count):
    return np.mean(np.abs(real_count - pred_count)/real_count)

# off-by-one (OBO) count error 
def OBO(pred_count, real_count):
    # predictive value and real value error 
    temp = np.abs(real_count - pred_count)
    # the proportion of the prediction value of the error is less than the same 
    return temp[temp <= 1].shape[0]/temp.shape[0]


# Index calculations under different conditions 

# calculate the overall error of differene movements under the same light 
def same_illumination_diff_action(file_names, pred_count):
    # True data of the original data
    nature_real_count = np.load('../npy_file/nature_data_real_count.npy')
    
    # Repnet network's prediction label on natural data
    repnet_nature_pred_count = np.load('../npy_file/repnet_nature_data_real_count.npy')
        
    start = 0 
    for name in file_names:
        print(f'Light conditions are{name[7:-4]}MAE=',MAE(pred_count[start::5],nature_real_count[start::5]))
        print(f'The light condition in the repnet is{name[7:-4]}MAE=',MAE(repnet_nature_pred_count[start::5],nature_real_count[start::5]))
        print(f'Light conditions are{name[7:-4]}OBO=',OBO(pred_count[start::5],nature_real_count[start::5]))
        print(f'The light condition in the repnet is{name[7:-4]}OBO=',OBO(repnet_nature_pred_count[start::5],nature_real_count[start::5]))
        start = start + 1
        print('-----------------')

# calculate the overall error of the same action under different light 
def diff_illumination_same_action(pred_count):
    start = 0 
    for i in range(2, 8):
        if i == 3:
            continue
        print(f'class={i}MAE of action=',MAE(pred_count[start:start+5],nature_real_count[start:start+5]))
        print(f'repnet middleclass={i}MAE of action=',MAE(repnet_nature_pred_count[start:start+5],nature_real_count[start:start+5]))
        print(f'class={i}Action OBO=',OBO(pred_count[start:start+5],nature_real_count[start:start+5]))
        print(f'repnet class={i}Action OBO=',OBO(repnet_nature_pred_count[start:start+5],nature_real_count[start:start+5]))
        
        start = start + 5
        print('-----------------')
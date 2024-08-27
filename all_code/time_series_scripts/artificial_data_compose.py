import pandas as pd 

'''
Randomly select a single action in class2 as A. The A here is the second repeat action of class2 in user02_fluorescent
class7's single action B as action B. The B here is the 7th repeat action of class7 in user02_fluorescent 
A5 represents the synthesis of the action A 5 times; the A3_B7 action a first synthesizes 3 times 
and then continues to synthesize 7 times;

A3_B13_A3 means that the action A synthesizes 3 times, continues to synthesize 13 times B action,
and then continues to synthesize 3 times A action. 
'''

# synthetic synthesis 
def get_same(file_name, repeat_times):
    # get a single action 
    df = pd.read_csv(
        f'../../event_csv/split_data/artificial/{file_name}.csv', 
        usecols=['timestamp','x','y'])
    # synthetic repeat_times times 
    df1 = df 
    for i in range(repeat_times - 1):
        df1 = pd.concat([df1, df], ignore_index=True)
    pd.DataFrame([['timestamp', 'x', 'y']]).to_csv(
        f"../../event_csv/split_data/artificial/{file_name}{repeat_times}.csv",
        index=False, header=False, mode='w',
    )
    df1.to_csv(
        f"../../event_csv/split_data/artificial/{file_name}{repeat_times}.csv",
        index=False, header=False, mode='a',
    )
    ...

# stitching before and after the same action 
def get_front_or_tail(repeat_times_A, repeat_times_B):
    # action A 
    df_A = pd.read_csv(f'../../event_csv/split_data/artificial/a{repeat_times_A}.csv')
    # action B 
    df_B = pd.read_csv(f'../../event_csv/split_data/artificial/b{repeat_times_B}.csv')

    pd.DataFrame([['timestamp', 'x', 'y']]).to_csv(
        f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}.csv',
        index=False, header=False, mode='w')
    
    # B connected in front of A 
    pd.concat([df_B, df_A], ignore_index=True).to_csv(
        f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}.csv',
        index=False, header=False, mode='a')
    
    pd.DataFrame([['timestamp', 'x', 'y']]).to_csv(
        f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}.csv',
        index=False, header=False, mode='w')
 
    # B connected behind A 
    pd.concat([df_A, df_B], ignore_index=True).to_csv(
        f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}.csv',
        index=False, header=False, mode='a')
    ...

# FLAG is True, the B action is sandwiched in the middle 
def get_mid(repeat_times_A, repeat_times_B, flag=True):
    if repeat_times_A == 1:
        repeat_times_A = ''
    if repeat_times_B == 1: 
        repeat_times_B = ''

    # action A 
    df_A = pd.read_csv(
        f'../../event_csv/split_data/artificial/a{repeat_times_A}.csv'
    )
    # action B 
    df_B = pd.read_csv(
        f'../../event_csv/split_data/artificial/a{repeat_times_B}.csv'
    )

    if flag: 
        pd.DataFrame([['timestamp', 'x', 'y']]).to_csv(
            f'../../event_csv/split_data/artificial/a{repeat_times_A}_b{repeat_times_B}_a{repeat_times_A}.csv',
            index=False, header=False, mode='w'
        )
        pd.concat([df_A, df_B, df_A], ignore_index=True).to_csv(
            f'../../event_csv/split_data/artificial/a{repeat_times_A}_b{repeat_times_B}_a{repeat_times_A}.csv',
            index=False, header=False, mode='a'
        )
    else: 
        pd.DataFrame([['timestamp', 'x', 'y']]).to_csv(
            f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}_b{repeat_times_B}.csv',
            index=False, header=False, mode='w'
        )
        pd.concat([df_B, df_A, df_B], ignore_index=True).to_csv(
            f'../../event_csv/split_data/artificial/b{repeat_times_B}_a{repeat_times_A}_b{repeat_times_B}.csv',
            index=False, header=False, mode='a'
        )
    ...
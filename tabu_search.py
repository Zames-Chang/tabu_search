import time
def cumsum(x):
    result = []
    temp = 0
    for i in x:
        temp += i
        result.append(temp)
    return result
def arrange(arrange_arr,data):
    now = data.copy()
    for var in ['jobs','time','due','weights']:
        temp = []
        for i in arrange_arr:
            temp.append(now[var][i-1])
        now[var] = temp
    return now
def myswap_arr(arrange_arr):
    result = []
    copy = arrange_arr.copy()
    for i in range(len(copy)-1):
        temp = myswap(copy,[i,i+1])
        result.append(temp)
    return result
def myswap(x,index):
    i = index[0]
    j = index[1]
    result = x.copy()
    temp = result[i]
    result[i] = result[j]
    result[j] = temp
    return result
def loss(data):
    result = 0
    process_time = cumsum(data['time'])
    for index in range(len(data['weights'])):
        w = data['weights'][index]
        d = data['due'][index]
        p = process_time[index]
        x = max(p-d,0)
        result += w*x
    return result
def checkTabu(arrange_arr,tabu_list):
    if(len(tabu_list) == 0):
        return True
    for tabu in tabu_list:
        i = tabu[0]
        j = tabu[1]
        for index in range(len(arrange_arr)-1):
            if(arrange_arr[index] == i and arrange_arr[index+1] == j):
                #print(arrange_arr)
                return False
    return True
def train_one_step(data,tabu_list,tabu_size):
    init_loss = loss(data)
    current = data.copy()
    big_loss = 9999999
    tabu = []
    neighborhoods = myswap_arr(data['jobs'])
    for index,neighborhood in enumerate(neighborhoods):
        #print(neighborhood)
        if(checkTabu(neighborhood,tabu_list)):
            #print(neighborhood)
            temp = arrange(neighborhood,current)
            temp_loss = loss(temp)
            #print("temp_loss=",temp_loss)
            if(temp_loss < big_loss):
                tabu = [current['jobs'][index],current['jobs'][index+1]]
                current = temp
    if(tabu != []):
        tabu_list.append(tabu)
    if(len(tabu_list) > tabu_size):
        tabu_list.pop(0)
    return current
def train(data,tabu_size,steps):
    tabu_list = []
    copy = data.copy()
    z = 0
    optimal = data.copy()
    current_loss = 99999999
    for i in range(steps):
        copy = train_one_step(copy,tabu_list,tabu_size)
        if(loss(copy) < current_loss):
            z = i
            print("current_loss = ",loss(copy))
            print("tabu_list = ",tabu_list)
            current_loss = loss(copy)
            optimal = copy.copy()
    return optimal,z
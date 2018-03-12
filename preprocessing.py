def get_numeric_types():
    return ["REAL","INT"]


def read_transaction_data(path):
    attribute_names_types = []
    transactions = []
    past_data_marker = False
    with open(path) as fp:
        for line in fp:
            if line.startswith('%'):
                continue
            elif line.startswith('@ATTRIBUTE'):
                attribute_names_types.append((line.split()[1],line.split()[2]))
            elif line.startswith('@DATA'):
                past_data_marker = True
            elif past_data_marker and line:
                transaction = []
                attributes = line.split(',')
                for i in range(len(attributes)):
                    if attribute_names_types[i][1] in get_numeric_types():
                        transaction.append(float(attributes[i]))
                    else:
                        transaction.append(attributes[i].strip('\n'))
                transactions.append(transaction)
        return transactions, attribute_names_types



def _get_intervals(data, attr_info, num_bins, ignore_attr=None):
    intervals = []
    types = [attr_info[i][1] for i in range(len(attr_info))]
    for i in range(len(attr_info)):
 
        if types[i] not in get_numeric_types() or i==ignore_attr or i-len(attr_info)==ignore_attr:
            intervals.append("N/A")
            continue

        data_points = [data[j][i] for j in range(len(data))]
        minval = min(data_points)
        diff = max(data_points) - minval
        interval_size = diff/num_bins
        cur_interval_points = [minval+(i+1)*interval_size for i in range(num_bins-1)]
        cur_intervals = []
        for i in range(len(cur_interval_points)):
            if i == 0:
                cur_intervals.append((-float('Inf'),cur_interval_points[i]))
            else:
                cur_intervals.append((cur_interval_points[i-1], cur_interval_points[i]))
        cur_intervals.append((cur_interval_points[i],float('Inf')))
        intervals.append(cur_intervals)
    return intervals

def make_discrete(data, attr_info, num_bins, ignore_attr=None):
    
    class_attr = -1 if not ignore_attr else ignore_attr

    intervals = _get_intervals(data, attr_info, num_bins, ignore_attr)
    print(intervals)
    names = [info[0] for info in attr_info]
    print(names)
    name_val_dict = {}
    for i,name in enumerate(names):
        name_val_dict[name] = []
        if not isinstance(intervals[i],list):
            continue
 
        for j in range(len(intervals[i])):
            name_val_dict[name].append(intervals[i][j])
    print(name_val_dict)
    
    discrete_data = []
    for transaction in data:
        discrete_transaction = []
        for i,item in enumerate(transaction):
            name = names[i]
            for j,interval in enumerate(name_val_dict[name]):
                if item > interval[0] and item < interval[1]:
                    discrete_transaction.append(j)
        discrete_transaction.append(transaction[class_attr])
        discrete_data.append(discrete_transaction)
    print(discrete_data)
    return discrete_data, name_val_dict
                
def main():
    transactions, attr_info = read_transaction_data("iris.txt")
    discrete_transactions, translation_dict = make_discrete(transactions, attr_info, 3,-1)

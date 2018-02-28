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
        interval_size = sum([data[j][i] for j in range(len(data))])/(len(data)*num_bins)
        cur_interval_points = [(i+1)*interval_size for i in range(num_bins-1)]
        cur_intervals = []
        for i in range(len(cur_interval_points)):
            if i == 0:
                cur_intervals.append((-float('Inf'),cur_interval_points[i]))
            else:
                cur_intervals.appen(cur_interval_points[i-1], cur_interval_points[i])
        cur_intervals.append((cur_interval_points[i],float('Inf')))
        intervals.append(cur_intervals)
    return intervals

def make_discrete(data, attr_info, num_bins, ignore_attr=None):
    intervals = _get_intervals(data, attr_info, num_bins, ignore_attr)
    print(intervals)

def main():
    transactions, attr_info = read_transaction_data("iris.txt")
    print(transactions)
    make_discrete(transactions, attr_info, 2, -1)

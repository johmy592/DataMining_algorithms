from preprocessing import *

def get_unique_items(transactions):
    items = []
    for t in transactions:
        for i in t:
            items.append(i)
    unique_items = set(items)
    return [[i] for i in unique_items]

def check_support(itemset, transactions, minsup):
    cur_support = 0
    for t in transactions:
        contains_itemset = True
        for item in itemset:
            if item not in t:
                contains_itemset = False
                break
        if contains_itemset:
            cur_support += 1
    return cur_support >= minsup
        
def get_next_candidates(prev_large):
    # Currently assumes that relative order is consistent

    next_candidates = []
    for i in range(len(prev_large)):
        for j in range(i+1,len(prev_large)):
            if prev_large[i][:-1] == prev_large[j][:-1]:
                candidate = prev_large[i][:-1] + [prev_large[i][-1]] + [prev_large[j][-1]]
                next_candidates.append(candidate)
    return next_candidates

def get_large_x_itemsets(candidates, transactions, minsup):
    Lx = []
    for c in candidates:
        if check_support(c,transactions,minsup):
            Lx.append(c)
    return Lx


def apriori(filename, minsup):
    # NOTE: Currently the algorithm assumes that relative order
    # of items in transactions is consistent.
    transactions, attr_info = read_transaction_data(filename)
    all_large_sets = []
    s1_candidates = get_unique_items(transactions)
    L1 = get_large_x_itemsets(s1_candidates, transactions, minsup)
    all_large_sets += L1
    candidates = get_next_candidates(L1)
    while candidates:
        Lx = get_large_x_itemsets(candidates, transactions, minsup)
        all_large_sets += Lx
        candidates = get_next_candidates(Lx)
    return all_large_sets

def generate_rules(filename, minsup, minconf):
    pass 

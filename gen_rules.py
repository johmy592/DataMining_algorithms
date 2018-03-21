def check_confidence(lhs, rhs, transactions, minconf):
    total = 0
    confirmations = 0
    for t in transactions:
        lhs_present = False 
        rhs_present = True
        for item in lhs:
            if item in t:
                lhs_present = True
                break
        if lhs_present:
            total += 1
            for item in rhs:
                if item not in t:
                    rhs_present = False
                    break
            if rhs_present:
                confirmations += 1
    
    return (confirmations/total) >= minconf if total > 0 else 0

def get_sm1_subsets(itemset):
    """
    Get subsets of size = size - 1.
    Returns a list of the subsets. 
    """
    
    subsets = []
    for i in itemset:
        cur_set = []
        for j in itemset:
            if i != j:
                cur_set.append(j)
        subsets.append(cur_set)
    return subsets 
    

def process_one_rule(lhs, rhs, transactions, minconf):
    """
    Returns the best rule that is based on rhs and satisfies minconf 
    """
    # I believe this now works, but gets an empty set at the end for some reason
    lefthand_sides = []
    processed_sets = []
    if not check_confidence(lhs, rhs, transactions, minconf):
        return None
    lefthand_sides.append(lhs)
    processed_sets.append(lhs)
    next_sets = get_sm1_subsets(lhs)
    while(next_sets):
        remaining_candidates = []
        for s in next_sets:
            print("NOW CHECKING: ", s)
            #processed_sets.append(s)
            if check_confidence(s, rhs, transactions, minconf):
                lefthand_sides.append(s)
                remaining_candidates.append(s)
        next_sets = []
        for s in remaining_candidates:
            for subset in get_sm1_subsets(s):
                if subset not in processed_sets:
                    processed_sets.append(subset)
                    next_sets.append(subset)
    return lefthand_sides
 

def process_one_itemset(itemset, transactions, minconf):
    pass

def gen_rules(large_itemsets, transactions,  minconf):
    # Filter out all large-1 itemsets
    rule_candidates = [s for s in large_itemsets if len(s) > 1]
    
        
    

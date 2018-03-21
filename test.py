import apriori as ap
import gen_rules as gr
import preprocessing as pp

def test_rules(filename, minconf):
    transactions, attr_info = pp.read_transaction_data(filename)
    large_itemsets = ap.apriori(filename,3)
    #lhs = large_itemsets[-1][:-1]
    #rhs = [large_itemsets[-1][-1]]

    lhs = ['A','B','C']
    rhs = ['Iris-setosa']
    print(lhs,rhs)
    print(gr.process_one_rule(lhs,rhs, transactions, minconf))    

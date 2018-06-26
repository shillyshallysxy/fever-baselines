from prettytable import PrettyTable

def analyse(predictions, actual):
    # table = {"actual_label": { "pred_label": count, "pred_label": "count"}, ...}
    supports = "SUPPORTS"
    refutes = "REFUTES"
    nei = "NOT ENOUGH INFO"
    table = {}

    for e1 in [supports, refutes, nei]:
        table[e1] = {}
        for e2 in [supports, refutes, nei]:
            table[e1][e2] = 0

    for pred_instance, actual_instance in zip(predictions, actual):
        table[actual_instance["label"]][pred_instance["predicted_label"]] += 1


    tab = PrettyTable()
    tab.field_names = [supports, refutes, nei]
    tab.add_row([supports, table[supports][supports], table[supports][refutes], table[supports][nei]])
    tab.add_row([refutes, table[refutes][refutes], table[refutes][refutes], table[refutes][nei]])
    tab.add_row([nei, table[nei][refutes], table[nei][refutes], table[nei][nei]])

    tot = 0
    for e1 in table.keys():
        for e2 in table[e1].keys():
            tot += table[e1][e2]
    print("total", tot)

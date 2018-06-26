import pandas
import numpy as np

def analyse(predictions, actual):
    # table = {"actual_label": { "pred_label": count, "pred_label": "count"}, ...}
    confusion_mat = np.zeros((3,3), dtype=np.int32)
    eye = np.eye(3)
    label2idx = {"SUPPORTS": 0, "REFUTES": 1, "NOT ENOUGH INFO": 2}
    labels = [label for label, val in sorted(label2idx.items(), key=lambda x: x[1])]

    for pred_instance, actual_instance in zip(predictions, actual):
        confusion_mat[label2idx[actual_instance["label"]], label2idx[pred_instance["predicted_label"]]] += 1

    print("actual \ predicted")
    df = pandas.DataFrame(confusion_mat, labels, labels)
    print(df)

    pre = np.sum(np.multiply(confusion_mat, eye), axis=0) / np.sum(confusion_mat, axis=0)
    rec = np.sum(np.multiply(confusion_mat, eye), axis=0) / np.sum(confusion_mat, axis=1)

    print("precision", pre)
    print("recall", rec)

import argparse
import json
import sys
from fever.scorer import fever_score
from prettytable import PrettyTable
from analyse import print_confusion_mat, save_wrong_instances, save_simple_result

parser = argparse.ArgumentParser()
parser.add_argument("--predicted_labels",type=str)

parser.add_argument("--predicted_evidence",type=str)
parser.add_argument("--actual",type=str)
parser.add_argument("--score_file",type=str)

args = parser.parse_args()

predicted_labels =[]
predicted_evidence = []
actual = []

with open(args.predicted_labels,"r") as predictions_file:
    for line in predictions_file:
        predicted_labels.append(json.loads(line)["predicted"])


with open(args.predicted_evidence,"r") as predictions_file:
    for line in predictions_file:
        predicted_evidence.append(json.loads(line)["predicted_sentences"])

with open(args.actual, "r") as actual_file:
    for line in actual_file:
        actual.append(json.loads(line))

predictions = []
for ev,label in zip(predicted_evidence,predicted_labels):
    predictions.append({"predicted_evidence":ev,"predicted_label":label})

score,acc,precision,recall,f1 = fever_score(predictions,actual)
print_confusion_mat(predictions, actual)
save_simple_result(args.score_file, score, acc, precision, recall)
# save_wrong_instances(args.actual, args.predicted_labels, args.predicted_evidence, args.score_file)

tab = PrettyTable()
tab.field_names = ["FEVER Score", "Label Accuracy", "Evidence Precision", "Evidence Recall", "Evidence F1"]
tab.add_row((round(score,4),round(acc,4),round(precision,4),round(recall,4),round(f1,4)))

print(tab)

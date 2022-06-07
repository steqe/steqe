import datetime
import random


def transform_readable_labels(label):
    ret_map = {
        "overall_num": "<extra_id_1>",
        "non_overall_num": "<extra_id_2>",
        "dct": "<extra_id_3>",
        "unknown": "<extra_id_4>",
        "unsure": "<extra_id_5>",
        "day": "<extra_id_6>",
        "non_us": "<extra_id_7>",
        "us": "<extra_id_8>",
        "worldwide": "<extra_id_9>",
        "non_worldwide": "<extra_id_10>",
    }
    reverse_map = {}
    for k in ret_map:
        reverse_map[ret_map[k]] = k
    if label in reverse_map:
        return reverse_map[label]
    return label


label_map_calfire = {
    "Number of fires": 1,
    "Physical measurements": 2,
    "People impacted (positively/negatively)": 3,
    "Items impacted (positively/negatively)": 4,
    "Resources": 5,
    "None of the above": 6,
}

label_map_blm = {
    "Number of protests or relevant activities -- Happened or planned to happen": 1,
    "Number of deaths caused by the protests or following skirmishes": 2,
    "Number of shootings during the protests or following skirmishes": 3,
    "Number of arrests due to the protests or following skirmishes": 4,
    "Number of injuries caused by the protests or following skirmishes": 5,
    "Number of participants in protests or relevant activities": 6,
    "Number of protests or relevant activities -- Cancelled": 7,
    "Number of people maintaining order": 8,
    "None of the above apply (vague text, not about protests, rate, etc.)": 9,
}

label_map_covid = {
    'Recoveries from COVID-19': 1,
    'None of the above apply (vague text, not COVID, rate, future, etc.)': 10,
    'Infections: confirmed or tested positive for COVID-19': 2,
    'Deaths: definitely caused by COVID-19': 4,
    'Patients with COVID-19: hospitalized': 7,
    'Patients with COVID-19: on ventilators': 8,
    'Deaths: likely caused by COVID-19': 3,
    'Tests performed for COVID-19: results not mentioned, pending, or mixed': 5,
    'Tests performed for COVID-19: result is negative': 6,
    'Patients with COVID-19: ICU': 9,
}


def get_inverse_str(idx, m):
    for k in m:
        if m[k] == idx:
            return k
    return "failure"


def end_to_end_evaluation():
    domain = "blm"
    typing_prediction_file = ""
    spatial_prediction_file = ""
    temporal_prediction_file = ""
    typing_gold_lines = [x.strip() for x in open("../data/for_t5/test/{}_typing.txt".format(domain)).readlines()]
    typing_prediction_lines = [x.strip() for x in open(typing_prediction_file).readlines()]
    spatial_gold_lines = [x.strip() for x in open("../data/for_t5/test/{}_spatial.txt".format(domain)).readlines()]
    spatial_prediction_lines = [x.strip() for x in open(spatial_prediction_file).readlines()]
    temporal_gold_lines = [x.strip() for x in open("../data/for_t5/test/{}_temporal.txt".format(domain)).readlines()]
    temporal_prediction_lines = [x.strip() for x in open(temporal_prediction_file).readlines()]
    correct = 0
    for i in range(0, len(typing_gold_lines)):
        label = temporal_gold_lines[i].split("\t")[1].split()[2:]
        dct = temporal_gold_lines[i].split("\t")[0].split("dct: ")[1].split(", ")[1]
        datetime_obj = datetime.datetime.strptime(dct, "%b %d %Y")
        dct_str = str(datetime_obj).split()[0]
        prediction = temporal_prediction_lines[i].split()[1:3]
        label = [transform_readable_labels(x) for x in label]
        prediction = [transform_readable_labels(x) for x in prediction]
        start_label = label[0]
        end_label = label[1]
        if len(prediction[1]) > 10:
            prediction[1] = prediction[1][:10]
        start_pred = prediction[0]
        end_pred = prediction[1]
        if start_label == "unknown" and end_label == dct_str:
            mapped_label = "overall"
        else:
            mapped_label = "nonoverall"
        if start_pred == "unknown" and end_pred == dct_str:
            mapped_pred = "overall"
        else:
            mapped_pred = "nonoverall"
        if mapped_label == mapped_pred:
            type_prediction = typing_prediction_lines[i]
            type_prediction = type_prediction.replace("<extra", " <extra")
            type_prediction = type_prediction.replace(">", "> ")
            type_prediction = type_prediction.split()[2]
            type_gold = typing_gold_lines[i].split("\t")[-1].split()[2]
            # if True:
            if type_prediction == type_gold:
                slabel = spatial_gold_lines[i].split("\t")[-1].split()[1:-1]
                gold_interpretable_lab = [transform_readable_labels(x) for x in slabel]
                gold_interpretable_lab_ = []
                for gi in gold_interpretable_lab:
                    if gi == "</s>":
                        continue
                    gold_interpretable_lab_.append(gi)
                gold_interpretable_lab = gold_interpretable_lab_
                sprediction = spatial_prediction_lines[i].replace("<extra", " <extra")
                sprediction = sprediction.split()[1:7]
                gold_interpretable_pred = [transform_readable_labels(x) for x in sprediction]
                if gold_interpretable_pred == "</s>":
                    gold_interpretable_pred = gold_interpretable_pred[:-1]
                if len(gold_interpretable_pred) > len(gold_interpretable_lab):
                    gold_interpretable_pred = gold_interpretable_pred[:len(gold_interpretable_lab)]
                if gold_interpretable_pred == gold_interpretable_lab:
                    correct += 1
    print(correct / float(len(typing_gold_lines)))


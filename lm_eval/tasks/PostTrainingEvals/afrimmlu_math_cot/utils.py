import os
from lm_eval.utils import weighted_f1_score

curr_dir = os.path.dirname(os.path.abspath(__file__))


def doc_to_choice(doc):
    choices = eval(doc["choices"])
    return choices


def doc_to_text(doc):
    with open(os.path.join(curr_dir, "prompt.txt"), "r") as f:
        output = f.read()

    choices = eval(doc["choices"])
    text = output.format(
        subject=doc["subject"],
        question=doc["question"],
        choice1=choices[0],
        choice2=choices[1],
        choice3=choices[2],
        choice4=choices[3],
    )
    return text

def doc_to_target(doc):
    option =  doc["answer"]
    index_of_option = ['A', 'B', 'C', 'D'].index(option)

    choices = eval(doc["choices"])

    return  choices[index_of_option]

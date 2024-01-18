import pandas as pd
import argparse
from tqdm import tqdm
import json

def check_eq(ref, pred):
    if type(ref) != type(pred):
        return False
    if isinstance(ref, list):
        if len(ref) != len(pred):
            return False
        # sort list
        ref = sorted(ref, key=lambda x: str(x))
        pred = sorted(pred, key=lambda x: str(x))
        for i in range(len(ref)):
            if not check_eq(ref[i], pred[i]):
                return False
        return True
    if isinstance(ref, dict):
        if len(ref) != len(pred):
            return False
        for k in ref:
            if k not in pred:
                return False
            if not check_eq(ref[k], pred[k]):
                return False
        return True
    return ref == pred # for str, int, float, bool


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='chatglm3-6b',
                        choices=["chatglm3-6b", "Baichuan2-13B-Chat", "Qwen-14B-Chat",
                                 "gpt-3.5-turbo", "gpt-4", "Yi-34B-Chat", "Qwen-74B-Chat"])
    args = parser.parse_args()
    model_name = args.model_name

    df = pd.read_csv(f"./data/test_data-{model_name}-execution.csv")
    correct_list = []
    for i in tqdm(range(len(df))):
        row = df.iloc[i]
        try:
            ref = json.loads(row["sql-预期执行结果"].replace("'", '"'))
        except:
            ref = []
        try:
            pred = json.loads(row[f"sql-{model_name}执行结果"].replace("'", '"'))
        except:
            pred = []
        correct_list.append(check_eq(ref, pred))
    print(f"Accuracy: {sum(correct_list) / len(correct_list)}")
    print(f"Details: {correct_list}")
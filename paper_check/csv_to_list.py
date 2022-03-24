import pandas as pd

def csv_to_list(csv_path):
    master_csv = pd.read_csv(csv_path)
    output_list = master_csv.values.tolist()
    output_list = [element[0] for element in output_list]
    return output_list
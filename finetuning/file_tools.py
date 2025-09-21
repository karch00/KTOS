import os
import json
from typing_extensions import Literal

def readJsonFiles(path: str, _data: list = []) -> list[list[dict]]:
    """
    Searches through a directory in search of json data and returns the ensemble of it.\n
    Does not support directly reading json files.

    Args:
        path: (str): Base directory path to search for data
        _data (list[str]): Current extracted data; EXCLUSIVELY USED BY RECURSION
    Returns:
        data (list[list[dict]]): List of lists of data gathered; each item is the data of a file
    """
    dir_tree = list(os.walk(path))
    
    for branch in dir_tree:
        dir_path = branch[0]
        files = branch[2]
        
        for leaf in files:
            if not ".json" in leaf:
                continue
    
            with open(f"{dir_path}/{leaf}", mode="r", encoding="utf-8") as f:
                file_data = json.load(f)
            _data.append(file_data)
    
    return _data

def validateJsonData(data: list[dict], architecture: Literal["unsloth", "hf-causal", "hf-instruct", "hf-class", "hf-question"]) -> list:
    """
    Corrects the data to match unsloth LLM input by removing incorrectly formatted entries.\n
    Expects a list of dictionaries with each dictionary being a point of data including (varies with architecture):\n
        - Instruction
        - Input
        - Output

    Args:
        data (list[dict]): List of data to validate
        architecture (Literal): Training architecture
    Returns:
        return_data (list): Corrected data
    """
    formats= {
        "unsloth": {
            "instruction": {"type": [str]},
            "input": {"type": [str]}, 
            "output": {"type": [str]}
        },
        "hf-causal": {
            "text": {"type": [str]},
        },
        "hf-instruct": {
            "instruction": {"type": [str]},
            "input": {"type": [str]},
            "output": {"type": [str]}
        },
        "hf-class": {
            "text": {"type": [str]},
            "label": {"type": [str, int]}
        },
        "hf-question": {
            "context": {"type": [str]},
            "question": {"type": [str]},
            "answer": {"type": [str]}
        }
    }
    
    entry_format = formats[architecture]
    return_data = []

    for idx in range(len(data)):
        entry = data[idx]
        correct_counter = 0
        
        for key, value in entry.items():
            if key not in entry_format or type(value) not in entry_format[key]["type"]:
                break
            correct_counter+=1
        
        return_data.append(entry) if len(entry.keys()) == correct_counter else ...

    return return_data 

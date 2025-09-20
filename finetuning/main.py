import torch
from unsloth import FastLanguageModel
from datasets import Dataset

def checkGPU() -> bool:
    """
    Check if GPU CUDA is available.\n
    Returns True if available, False otherwise.
    """
    cuda_available = torch.cuda.is_available()
    card = torch.cuda.get_device_name(0) if cuda_available else "No card detected"
    
    print(f"CUDA available: {cuda_available}\nGPU: {card}")
    return cuda_available

class UnslothTuning():
    """
    Unsloth tuning functions
    """

    def loadModel(model_name: str, sequence_length: int, data_type: str = None, load_4_bit: bool = False, load_8_bit: bool = False, gpu_memory_utilization: float = 0.5) -> tuple:
        """
        Loads the model to be fine tuned using unsloth.
        Args:
            model_name (str): The model name USER/MODEL
            sequence_length (int): Max sequence length in tokens
            data_type (str): Tensor data type
            load_4_bit (bool): Load model in 4 bit
            load_8_bit (bool): Load model in 8 bit
            gpu_memory_utilization (float): Percentage of gpu memory used, between 0 and 1
        """
        if gpu_memory_utilization <= 0 or gpu_memory_utilization >= 1:
            message = "[WARNING] GPU memory usage set to %s, defaulting to 50%"
            message.replace("%s", "0% or under" if gpu_memory_utilization <= 0 else "100% or over")

            gpu_memory_utilization = 0.5
        elif gpu_memory_utilization > 0.85:
            print(\
    f"""
    [WARNING]----------------------------------------------[WARNING]
    [WARNING] GPU memory usage set to {gpu_memory_utilization*100}                 [WARNING]
    [WARNING] This may lead to unstability or even crashes [WARNING]
    [WARNING] Press any button to dismiss                  [WARNING]
    [WARNING]----------------------------------------------[WARNING]
    """)

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=sequence_length,
            dtype=data_type,
            load_in_4bit=load_4_bit,
            load_in_8bit=load_8_bit,
            gpu_memory_utilization=gpu_memory_utilization
        )

        return model, tokenizer

    def preprocessData(data_path: str):
        raise NotImplementedError()
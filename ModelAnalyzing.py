import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM
import numpy as np
from ChatbotEvaluator import ChatbotEvaluator
import textwrap

def setup_model(model_name="t5-small"):
    # Check if the model is t5 model type.
    if model_name.startswith("t5"):
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

    elif model_name.startswith("facebook/bart"):
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

    elif model_name.startswith("gpt2"):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

    else:
        raise ValueError("Unknown model or model is not supported")
    
    return tokenizer, model

def analyze_t5_model(model_name="t5-small", input_text=None, task="translation", max_length=512):

    """
    Comprehensive analysis of T5 model performance and characteristics
    
    Args:
        model_name (str): Hugging Face T5 model name
        input_text (str): Text to analyze (optional)
        task (str): Model task type (translation, summarization, etc.)
    
    Returns:
        dict: Comprehensive model analysis
    """

    def generate_text(text, max_length=150):
        inputs = tokenizer(f"{task}: {text}", return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs["input_ids"], max_length=max_length)
        t = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(len(t))
        return t

    def analyze_page(input_text, paragraph_len=512):
        words = input_text.split()

        chunks = [" ".join(words[i:i+paragraph_len]) for i in range(0, len(words), paragraph_len)]

        analyzed_chunks = [generate_text(chunk) for chunk in chunks]

        final_output = " ".join(analyzed_chunks)

        return final_output

    # Load model and tokenizer
    tokenizer, model = setup_model(model_name)

    analysis = {
        'model_name': model_name,
        'task': task,
        'architecture': {
            'total_parameters': sum(p.numel() for p in model.parameters()),
            'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad)
        }
    }

    if len(input_text.split()) > 512:
        final_output = analyze_page(input_text)
        while len(final_output.split()) > 1000:
            print("Begin next task")
            final_output = analyze_page(final_output)
    else:
        final_output = input_text

    print("Begin final task")
    if final_output:
        inputs = tokenizer(final_output, return_tensors="pt", max_length=max_length, truncation=True)

        # Put tokens in the analysis.
        analysis['tokenization'] = {
            'input_text': input_text,
            'input_length': len(inputs['input_ids'][0]),
            'token_count': inputs['input_ids'].shape[1],
            'attention_mask_sum': inputs['attention_mask'].sum().item()
        }

        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=max_length + 100)
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Get the generated text.
        analysis['generation'] = {
            'generated_text': generated_text,
            'generation_length': len(tokenizer.encode(generated_text))
        }

    analysis["computational_profile"] = {
        'model_dtype': str(next(model.parameters()).dtype)
    }

    return analysis

def read_and_analyze(text, model="t5-base", task="summarize", max_length=200):
    if model.startswith("t5"):
        input_text = f"{task}: {text}"

    elif model.startswith("facebook/bart"):
        input_text = text

    elif model.startswith("gpt2"):
        input_text = f"{task}: {text}"

    print(type(text))

    detailed_analysis = analyze_t5_model(
        model_name=model,
        input_text=input_text,
        task=task,
        max_length=max_length
    )

    evaluator = ChatbotEvaluator()

    metrics = evaluator.calculate_metrics(text, detailed_analysis["generation"]['generated_text'], task_type=task)

    return detailed_analysis, metrics
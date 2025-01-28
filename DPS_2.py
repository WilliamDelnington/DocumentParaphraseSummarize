import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import numpy as np
from DPS_3 import ChatbotEvaluator

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

    # Load model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    analysis = {
        'model_name': model_name,
        'task': task,
        'architecture': {
            'total_parameters': sum(p.numel() for p in model.parameters()),
            'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad)
        }
    }

    if input_text:
        inputs = tokenizer(input_text, return_tensors="pt", max_length=max_length, truncation=True)

        analysis['tokenization'] = {
            'input_length': len(inputs['input_ids'][0]),
            'token_count': inputs['input_ids'].shape[1],
            'attention_mask_sum': inputs['attention_mask'].sum().item()
        }

        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=200)
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        analysis['generation'] = {
            'generated_text': generated_text,
            'generation_length': len(tokenizer.encode(generated_text))
        }

    analysis["computational_profile"] = {
        'model_dtype': str(next(model.parameters()).dtype)
    }

    return analysis

if __name__ == "__main__":
    with open("./testDocument.txt", "r", encoding="utf-8") as file:
        text = file.read()

    detailed_analysis = analyze_t5_model(
        model_name="t5-base",
        input_text=f"Summarize: {text}",
        task="summarization"
    )

    print(detailed_analysis)

    evaluator = ChatbotEvaluator()

    metrics = evaluator.calculate_metrics(text, detailed_analysis["generation"]['generated_text'])

    print(metrics)
# Document Paraphrasing and Summarizing Chatbot

## Overview

This project is a chatbot designed to paraphrase and summarize documents efficiently. It utilizes the T5, BART, and GPT2 Transformer models and supports fundamental conversation handling for better user interaction.

## Features

- **Document Summarization**: Extracts key points and produces concise document summaries.
- **Text Paraphrasing**: Rephrases input text while retaining its original meaning.
- **Interactive Chatbot**: Engages users through a conversational interface.
- **Customizable NLP Models**: Supports T5-based transformers or other fine-tuned models for text generation.

## Technologies Used

- **Python**: Core programming language for implementation.
- **Hugging Face Transformers**: For pre-trained language models (e.g., T5).
- **Flask**: Backend framework for deploying the chatbot.
- **NLTK**: For tokenization and sentiment analysis.
- **ROUGE Metrics**: To evaluate the summarization quality.
- **Docker**: For containerizing the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WilliamDelnington/DocumentParaphraseSummarize.git
   cd DocumentParaphraseSummarize
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv .venv (Python 3.10)
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Chatbot Locally:**

   ```bash
   python app.py
   ```

   This starts a Flask/Django server accessible at `http://127.0.0.1:5000/`.

2. **Input a Document:** Upload a text file or paste the content directly into the chatbot interface.

3. **Specifying a Task:**

   - `Summarize`: Returns a concise summary of the document.
   - `Paraphrase`: Outputs a rephrased version of the input text.

4. **View Results:** Results are displayed in real-time.

## File Structure

```
.
├── app.py                   # Main application file
├── requirements.txt         # Dependencies
├── static/                  # Static files when using with the templates
├── templates/               # HTML templates for the web interface
├── README.md                # Project documentation
└── testDocument.txt         # Example input document
```

## Model Training

1. **Prepare Data**:

   - Collect and preprocess documents for summarization and paraphrasing.
   - Split data into training, validation, and test sets.

2. **Fine-tune T5**: Use Hugging Face's `Trainer` API to fine-tune the T5 (or BART, GPT2) model for summarization and paraphrasing tasks.

   ```python
   from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, BartTokenizer, BartForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM

   # Load pre-trained T5 model and tokenizer
   model_name = "t5-small" # Use any related t5 models.
   model = T5ForConditionalGeneration.from_pretrained(model_name)
   tokenizer = T5Tokenizer.from_pretrained(model_name)

   # Load pre-trained BART model and tokenizer
   model_name = "bart-base" # Use any related BART models.
   model = BartForConditionalGeneration.from_pretrained(model_name)
   tokenizer = BartTokenizer.from_pretrained(model_name)

   # Load pre-trained GPT2 model and tokenizer
   model_name = "gpt2" # Use any related t5 models.
   model = AutoModelForCausalLM.from_pretrained(model_name)
   tokenizer = AutoTokenizer.from_pretrained(model_name)

   # Fine-tuning code goes here...
   ```

3. **Evaluate Model**: Use ROUGE metrics to measure summarization quality and adjust hyperparameters as needed.

## Deployment

- **Local Deployment**: Run the chatbot locally for testing.

- **Cloud Deployment**: Use platforms like AWS, Google Cloud, or Heroku to deploy the chatbot for public access.

- **Docker Deployment**: Build and deploy using Docker:

  ```bash
  docker build -t chatbot .
  docker run -p 5000:5000 chatbot
  ```

## Future Improvements

- Enhance multi-language support.
- Implement sentiment-aware summarization.
- Optimize model for faster inference.
- Add user authentication and history tracking.

## Contributors

- [Nguyen Vu Gia Huy - BA12-088](https://github.com/WilliamDelnington) (Group Leader)
- Trinh Quang Minh - BA12-127
- Lai Phu Huy - BA12-084
- Nguyen Nu Lan Anh - BA12-016

## Acknowledgments

- Hugging Face for pre-trained T5, BART and GPT2 models.
- NLTK, ROUGE, BERT and BLEU for NLP tools.
- Flask for backend support.

---

Feel free to reach out with questions or suggestions!


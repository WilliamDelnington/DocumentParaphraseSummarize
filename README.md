# Document Paraphrasing and Summarizing Chatbot

## Overview

This project is a chatbot designed to paraphrase and summarize documents. Built using state-of-the-art natural language processing (NLP) techniques, it provides an efficient way to process large volumes of text and extract concise summaries or generate paraphrased versions of the input text.

## Features

- **Document Summarization**: Extracts key points from long documents.
- **Text Paraphrasing**: Rephrases input text while retaining its original meaning.
- **Interactive Chatbot**: Engages users through a conversational interface.
- **Customizable NLP Models**: Supports T5-based transformers or other fine-tuned models for text generation.
- **Multi-Language Support**: Capable of working with texts in multiple languages.

## Technologies Used

- **Python**: Core programming language for implementation.
- **Hugging Face Transformers**: For pre-trained language models (e.g., T5).
- **Flask/Django**: Backend framework for deploying the chatbot.
- **Google Colab/Jupyter Notebook**: For experimentation and training.
- **NLTK**: For tokenization and sentiment analysis.
- **ROUGE Metrics**: To evaluate the summarization quality.
- **Docker**: For containerizing the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WilliamDelnington/DocumentParaphraseSummarize.git
   cd document-chatbot
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

3. **Select a Task:**

   - `Summarize`: Returns a concise summary of the document.
   - `Paraphrase`: Outputs a rephrased version of the input text.

4. **View Results:** Results are displayed in real-time and can be exported as a text file.

## File Structure

```
.
├── app.py                   # Main application file
├── requirements.txt         # Dependencies
├── models/                  # Pre-trained models and fine-tuned weights
├── static/                  # Static files (CSS, JS, etc.)
├── templates/               # HTML templates for the web interface
├── README.md                # Project documentation
└── testDocument.txt         # Example input document
```

## Model Training

1. **Prepare Data**:

   - Collect and preprocess documents for summarization and paraphrasing.
   - Split data into training, validation, and test sets.

2. **Fine-tune T5**: Use Hugging Face's `Trainer` API to fine-tune the T5 model for summarization and paraphrasing tasks.

   ```python
   from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

   # Load pre-trained T5 model and tokenizer
   model = T5ForConditionalGeneration.from_pretrained("t5-small")
   tokenizer = T5Tokenizer.from_pretrained("t5-small")

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

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributors

- [Nguyen Vu Gia Huy - BA12-088](https://github.com/WilliamDelnington) (Group Leader)
- Trinh Quang Minh - BA12-127
- Lai Phu Huy - BA12-084
- Nguyen Nu Lan Anh - BA12-016

## Acknowledgments

- Hugging Face for pre-trained T5 models.
- NLTK and ROUGE for NLP tools.
- Flask/Django for backend support.

---

Feel free to reach out with questions or suggestions!


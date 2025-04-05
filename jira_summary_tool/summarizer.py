# summarizer.py
import os, openai

# Initialize OpenAI API key from environment (could also use cfg passed in)
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_issue(text, cfg):
    """Return a tuple (high_level_summary, detailed_summary) for the given text."""
    # High-level summary request
    hl_prompt = f"Summarize the following issue in a single sentence:\n{text}"
    hl_response = openai.ChatCompletion.create(
        model=cfg.openai_model,
        messages=[{"role": "user", "content": hl_prompt}],
        temperature=0.5
    )
    high_level = hl_response['choices'][0]['message']['content'].strip()
    
    # Detailed summary request
    det_prompt = f"Provide a detailed summary of the following issue:\n{text}"
    det_response = openai.ChatCompletion.create(
        model=cfg.openai_model,
        messages=[{"role": "user", "content": det_prompt}],
        temperature=0.7
    )
    detailed = det_response['choices'][0]['message']['content'].strip()
    
    return high_level, detailed

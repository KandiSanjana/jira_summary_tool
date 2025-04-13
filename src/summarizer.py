import cohere

def summarize_issue(text, cfg):
    co = cohere.Client(cfg.cohere_api_key)

    try:
        print("Sending summarization request to Cohere")
        response = co.summarize(
            text=text,
            length='auto',           # Options: short, medium, long, auto
            format='paragraph',      # Options: paragraph or bullets
            temperature=0.3
        )

        summary = response.summary.strip()
        return summary  # No separate high/detailed distinction in Cohere

    except Exception as e:
        print(f"❌ Error during summarization: {e}")
        raise

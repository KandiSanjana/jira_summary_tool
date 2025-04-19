import logging
import cohere
from typing import Optional

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self, api_key: str):
        """Initialize the Cohere client with API key."""
        self.client = cohere.Client(api_key)

    def summarize_issue(self, text: str, length: str = 'auto', format: str = 'paragraph') -> Optional[str]:
        """
        Generate a summary of the given text using Cohere's API.
        
        Args:
            text: The text to summarize
            length: Summary length ('short', 'medium', 'long', 'auto')
            format: Output format ('paragraph' or 'bullets')
            
        Returns:
            The generated summary or None if summarization fails
        """
        if not text:
            logger.warning("Empty text provided for summarization")
            return None

        try:
            logger.debug("Sending summarization request to Cohere")
            response = self.client.summarize(
                text=text,
                length=length,
                format=format,
                temperature=0.3
            )

            summary = response.summary.strip()
            logger.debug(f"Successfully generated summary: {summary}")
            return summary

        except cohere.CohereError as e:
            logger.error(f"Cohere API error during summarization: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during summarization: {e}")
            return None

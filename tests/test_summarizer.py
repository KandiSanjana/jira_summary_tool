# test_summarizer.py
import pytest
from jira_summary_tool import summarizer

class DummyResponse:
    def __getitem__(self, key):
        # Simulate OpenAI response structure
        if key == 'choices':
            return [ {'message': {'content': 'This is a summary.'}} ]

def test_summarize_issue(monkeypatch):
    # Monkeypatch the OpenAI API call
    monkeypatch.setattr(summarizer.openai.ChatCompletion, "create",
                        lambda **kwargs: DummyResponse())
    text = "Summary: Test\nDescription: Test issue description."
    cfg = type("C", (), {"openai_model": "gpt-3.5-turbo"})
    high_level, detailed = summarizer.summarize_issue(text, cfg)
    assert isinstance(high_level, str) and isinstance(detailed, str)
    assert "summary" in high_level.lower() or high_level != ""
    assert "summary" in detailed.lower() or detailed != ""

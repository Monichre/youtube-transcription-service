import os
from openai import OpenAI
from anthropic import Anthropic
from disclosure_agent_ingestion.research_prompt import research_prompt
import json

openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")


class ContentAnalysisEngine:
    def __init__(self):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.anthropic_client = Anthropic(api_key=anthropic_api_key)

    def get_claude_analysis(self, transcript):
        """Get analysis from Claude"""
        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=research_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": transcript
                    }
                ]
            )
            # Extract the text content from the message
            return message.content[0].text
        except Exception as e:
            print(f"Claude Analysis Error: {e}")
            return None

    def analyze_content(self, content_text):
        """Analyze transcript text using both OpenAI and Claude"""
        try:

            # openai_analysis = self.get_openai_analysis(content_text)
            claude_analysis = self.get_claude_analysis(content_text)

            analysis_section = "=== APPLIED RESEARCH METHODOLOGY CONTENT ANALYSIS ===\n\n"

            # if openai_analysis:
            #     analysis_section += "OpenAI Analysis:\n"
            #     analysis_section += openai_analysis
            #     analysis_section += "\n\n"

            if claude_analysis:
                analysis_section += "Research Agent Analysis:\n"
                analysis_section += claude_analysis
                analysis_section += "\n\n"

            analysis_section += "=== ORIGINAL CONTENT ===\n\n"

            return analysis_section
        except Exception as e:
            print(f"Analysis Error: {e}")
            return None

# app/agent.py
from typing import Dict
from app.utils import sanitize_markdown, guard_length

class TextAgent:
    """
    A simple, text-only agent. No external dependencies.
    Replace `generate_reply` with an actual LLM call when ready.
    """

    def __init__(self):
        # You can store preferences or memory here later.
        self.max_reply_len = 4096

    def classify_intent(self, user_message: str) -> str:
        msg = user_message.lower()
        if msg.startswith("/help") or "help" in msg:
            return "help"
        if "workflow" in msg or "automation" in msg:
            return "automation"
        return "chat"

    def generate_reply(self, user_message: str) -> str:
        intent = self.classify_intent(user_message)

        if intent == "help":
            reply = (
                "Welcome! I’m a text-only AI agent.\n\n"
                "- Send any message and I’ll respond.\n"
                "- Ask about simple automation or planning, and I’ll outline steps.\n"
                "- I’m a web service, so you can POST text here.\n\n"
                "Future features: memory, tools (Sheets, YouTube), and chat updates."
            )
        elif intent == "automation":
            reply = (
                "Here’s a simple plan to start an automation:\n"
                "1) Define the goal (e.g., daily summary).\n"
                "2) Identify inputs (web pages/APIs).\n"
                "3) Draft steps (fetch → process → summarize → notify).\n"
                "4) Test with sample data.\n"
                "5) Add logging for visibility.\n\n"
                "When you’re ready, we can connect this agent to tools and workflows."
            )
        else:
            # Friendly, concise default reply
            reply = (
                "Got it. I’m a minimal AI agent right now—text in, text out.\n"
                "Tell me what you want to achieve, and I’ll outline clear steps."
            )

        reply = sanitize_markdown(reply)
        reply = guard_length(reply, self.max_reply_len)
        return reply

# Create a single shared agent instance
agent = TextAgent()
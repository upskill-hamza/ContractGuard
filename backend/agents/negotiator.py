from .base import Agent

class NegotiatorAgent(Agent):
    def __init__(self, mcp_client):
        super().__init__("Negotiator")
        self.mcp_client = mcp_client
        self.templates = {
            "termination": "Propose mutual termination with {notice_days} days notice.",
            "liability": "Suggest a liability cap of ${amount}.",
            "governing_law": "Request governing law be changed to {state}.",
            "auto_renewal": "Add a clause requiring explicit written consent for renewal."
        }

    def run(self, issues):
        suggestions = []
        for issue in issues:
            # Try MCP tool first
            advice = self.mcp_client.call_tool(
                "generate_negotiation_talking_points",
                {"issue": issue.get("explanation", issue.get("rule", ""))}
            )
            suggestion_text = advice.get("suggestion", "")
            if not suggestion_text:
                suggestion_text = self._template_suggestion(issue)

            suggestions.append({
                "clause_id": issue.get("clause_id", ""),
                "issue": issue.get("explanation", issue.get("rule", "")),
                "suggestion": suggestion_text
            })
        return suggestions

    def _template_suggestion(self, issue):
        text = str(issue).lower()
        if "termination" in text:
            return self.templates["termination"].format(notice_days=90)
        elif "liability" in text:
            return self.templates["liability"].format(amount="500,000")
        elif "governing law" in text:
            return self.templates["governing_law"].format(state="California")
        elif "renewal" in text:
            return self.templates["auto_renewal"]
        return "Negotiate to remove or modify this clause."
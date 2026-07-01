import json
from .base import Agent

class RiskAnalyzerAgent(Agent):
    def __init__(self, mcp_client):
        super().__init__("RiskAnalyzer")
        self.mcp_client = mcp_client
        with open("data/legal_kb.json", "r") as f:
            self.kb = json.load(f)

    def run(self, clauses):
        annotated = []
        for clause in clauses:
            risks = self._analyze_clause(clause)
            annotated.append({**clause, "risks": risks})
        return annotated

    def _analyze_clause(self, clause):
        risks = []
        text_lower = clause["text"].lower()

        # 1. Local knowledge base
        for item in self.kb:
            if item["phrase"].lower() in text_lower:
                risks.append({
                    "type": "risky_phrase",
                    "level": item["risk"],
                    "explanation": item["explanation"],
                    "source": "local_kb"
                })

        # 2. MCP: search legal definitions for complex terms
        complex_terms = self._extract_complex_terms(clause["text"])
        for term in complex_terms:
            definition = self.mcp_client.call_tool("search_legal_definitions", {"term": term})
            if definition.get("is_risky"):
                risks.append({
                    "type": "legal_term_risk",
                    "level": "medium",
                    "explanation": definition["explanation"],
                    "source": "mcp"
                })

        # 3. MCP: check similar contracts
        similar = self.mcp_client.call_tool("check_similar_contracts", {"clause_text": clause["text"]})
        if similar.get("common_dispute"):
            risks.append({
                "type": "dispute_prone",
                "level": "high",
                "explanation": similar["explanation"],
                "source": "mcp"
            })
        return risks

    def _extract_complex_terms(self, text):
        candidate_terms = ["indemnification", "force majeure", "arbitration",
                           "liquidated damages", "severability", "waiver", "subrogation"]
        found = []
        for term in candidate_terms:
            if term in text.lower():
                found.append(term)
        return found
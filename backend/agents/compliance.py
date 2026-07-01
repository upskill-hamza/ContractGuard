from .base import Agent
from backend.security.policy_vault import PolicyVault

class ComplianceAgent(Agent):
    def __init__(self):
        super().__init__("Compliance")

    def run(self, clauses, vault: PolicyVault):
        rules = vault.get_rules()
        violations = []
        for clause in clauses:
            for rule in rules:
                if self._clause_violates_rule(clause, rule):
                    violations.append({
                        "clause_id": clause["id"],
                        "rule": rule["description"],
                        "severity": rule.get("severity", "high"),
                        "suggestion": rule.get("suggestion", "")
                    })
        return violations

    def _clause_violates_rule(self, clause, rule):
        text = clause["text"].lower()
        rule_type = rule.get("type", "must_not_contain")
        if rule_type == "must_contain":
            return rule["keyword"].lower() not in text
        elif rule_type == "must_not_contain":
            return rule["keyword"].lower() in text
        elif rule_type == "governing_law":
            return "state of california" not in text
        return False
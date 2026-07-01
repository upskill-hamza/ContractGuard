"""Tool implementations for the ContractGuard MCP server."""

LEGAL_DEFINITIONS = {
    "indemnification": {
        "definition": "A promise to compensate for loss or damage.",
        "is_risky": True,
        "explanation": "Indemnification clauses can shift unexpected liability to your business."
    },
    "force majeure": {
        "definition": "Unforeseeable circumstances preventing contract fulfillment.",
        "is_risky": False,
        "explanation": "Standard clause; ensure it covers both parties equally."
    },
    "arbitration": {
        "definition": "Dispute resolution outside court.",
        "is_risky": False,
        "explanation": "Arbitration clauses can limit your right to sue."
    },
    "liquidated damages": {
        "definition": "Pre-agreed sum payable for breach.",
        "is_risky": True,
        "explanation": "Amount should be reasonable; excessive liquidated damages may be unenforceable."
    },
    "severability": {
        "definition": "If one clause is invalid, the rest of the contract stands.",
        "is_risky": False,
        "explanation": "Standard protective clause."
    }
}

def search_legal_definitions(term: str) -> dict:
    term_lower = term.lower()
    return LEGAL_DEFINITIONS.get(term_lower, {"definition": "No definition found", "is_risky": False})

def check_similar_contracts(clause_text: str) -> dict:
    text_lower = clause_text.lower()
    if "termination" in text_lower and "without cause" in text_lower:
        return {"common_dispute": True, "explanation": "Termination without cause often leads to disputes."}
    elif "liability" in text_lower and "unlimited" in text_lower:
        return {"common_dispute": True, "explanation": "Unlimited liability clauses are rarely accepted."}
    return {"common_dispute": False, "explanation": ""}

def generate_negotiation_talking_points(issue: str) -> dict:
    issue_lower = issue.lower()
    if "indemnification" in issue_lower:
        return {"suggestion": "Suggest mutual indemnification and cap at contract value."}
    elif "termination" in issue_lower:
        return {"suggestion": "Increase notice period to 90 days and require cause."}
    elif "liability" in issue_lower:
        return {"suggestion": "Propose a liability cap equal to fees paid."}
    elif "auto" in issue_lower and "renew" in issue_lower:
        return {"suggestion": "Add opt-out option 30 days before auto-renewal."}
    else:
        return {"suggestion": "Request a fairer alternative or removal."}
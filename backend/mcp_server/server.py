"""
MCP Server for ContractGuard.
Uses FastMCP from the mcp package (version >=1.28.1).
"""

from mcp.server.fastmcp import FastMCP
from .tools import search_legal_definitions, check_similar_contracts, generate_negotiation_talking_points

# Create the server
mcp = FastMCP("contract-tools")

@mcp.tool()
def tool_search_legal_definitions(term: str) -> dict:
    """Search for a legal term and get its definition and risk assessment."""
    return search_legal_definitions(term)

@mcp.tool()
def tool_check_similar_contracts(clause_text: str) -> dict:
    """Check if similar clauses often lead to disputes."""
    return check_similar_contracts(clause_text)

@mcp.tool()
def tool_generate_negotiation_talking_points(issue: str) -> dict:
    """Generate negotiation suggestions for a given issue."""
    return generate_negotiation_talking_points(issue)

if __name__ == "__main__":
    mcp.run()
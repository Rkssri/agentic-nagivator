from fastmcp import FastMCP

mcp = FastMCP("Customer MCP Server")

customer_id_counter = 0

@mcp.tool()
def addCustomer(name: str, email: str) -> dict:
    """Add a new customer"""
    # In a real application, you would save this to a database
    global customer_id_counter
    customer_id_counter += 1
    return {"id": customer_id_counter, "name": name, "email": email}

@mcp.tool()
def getCustomer(customer_id: int) -> dict:
    """Get customer details by ID"""
    # In a real application, you would retrieve this from a database
    customers = {
        1: {"id": 1, "name": "Rakesh Shrivastava", "email": "rakesh.shrivastava@example.com"},
        2: {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"}
    }
    return customers.get(customer_id, {"id": customer_id, "name": "Unknown", "email": "unknown@example.com"})

if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
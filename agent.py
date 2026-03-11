# installing required package for langhchain and open ai
# pip install -qU langchain-openai

from langchain.agents import create_agent

#Start define tools
def get_orders(customer_id: str) -> dict:
    """Get all orders for a given customer.
    
    Args:
        customer_id: The customer email address to retrieve orders for
        
    Returns:
        dict: Contains customer_id and list of orders with id, amount, and status
    """
    return {
        "customer_id": customer_id,
        "orders": [
            {"order_id": "ORD001", "amount": 250.00, "status": "completed"},
            {"order_id": "ORD002", "amount": 150.50, "status": "pending"}
        ],
        "total_count": 2
    }

def get_orders_ById(order_id: str) -> dict:
    """Get detailed information for a specific order by ID.
    
    Args:
        order_id: The order ID to retrieve
        
    Returns:
        dict: Contains order details including id, customer, amount, and status
    """
    return {
        "order_id": order_id,
        "customer": "John Doe",
        "amount": 250.00,
        "status": "completed",
        "items": ["Item1", "Item2"],
        "date_created": "2026-03-03"
    }

def create_orders(customer_id: str, product: str, quantity: int) -> dict:
    """Create a new order for a given customer.
    
    Args:
        customer_id: The customer email address placing the order
        product: The product name to order
        quantity: The quantity of items to order
        
    Returns:
        dict: Contains order confirmation details with new order_id and status
    """
    return {
        "order_id": "ORD003",
        "customer_id": customer_id,
        "product": product,
        "quantity": quantity,
        "status": "created",
        "message": f"Order created successfully for {quantity} {product}(s) for customer {customer_id}"
    }

#End define tools

#Create agent
agent = create_agent(
    model="gpt-4o",
    tools=[get_orders, get_orders_ById, create_orders],
    system_prompt="You are a helpful assistant to manage orders for customers. You can retrieve orders by customer email or order ID, and create new orders based on customer requests.",
)

# Interactive agent loop
print("Order Management Agent - Type 'exit' to quit\n")
while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "exit":
        print("Exiting agent...")
        break
    
    if not user_input:
        print("Please enter a valid request.\n")
        continue
    
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        
        # Extract the agent's response message
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            # Get the last message (should be the agent's response)
            if messages:
                last_message = messages[-1]
                # Extract content from the message object
                response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                response_text = "No response received"
        else:
            response_text = str(result)
        
        print(f"\nAgent: {response_text}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")


# Order Creator Agent

An intelligent order management agent built with LangChain that uses GPT-4o to help manage customer orders conversationally.

## Overview

The Order Creator Agent is an AI-powered assistant that helps manage orders for customers. It can retrieve orders by customer email or order ID, and create new orders based on natural language requests. The agent uses OpenAI's GPT-4o model to understand user intentions and interact with order management tools.

## Features

- **Retrieve Orders by Customer**: Get all orders for a specific customer by their email address
- **Get Order Details**: Look up detailed information about a specific order by order ID
- **Create Orders**: Create new orders for customers with product and quantity specifications
- **Conversational Interface**: Interact with the agent using natural language

## Prerequisites

Before running the agent, ensure you have:

- Python 3.8+
- OpenAI API key
- Required packages (see installation section)

## Installation

1. **Set up a virtual environment** (recommended):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate  # macOS/Linux
```

2. **Install required packages**:
```bash
pip install -qU langchain-openai
```

Alternatively, install from the requirements file:
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:
   - Create an environment variable `OPENAI_API_KEY` with your API key
   - Or set it in your `.env` file (if using python-dotenv)

## Usage

Run the agent:
```bash
python agent.py
```

The agent will start an interactive session where you can type commands:

### Example Commands

- "Show me all orders for john@example.com"
- "Can you tell me the status of order ORD001?"
- "I'd like to create an order for alice@example.com - 5 units of Widget ABC"
- "Get my recent orders"

Type `exit` to quit the agent.

## Available Tools

The agent has access to the following tools:

### 1. `get_orders(customer_id: str)`
Retrieves all orders for a given customer.

**Parameters:**
- `customer_id` (str): Customer email address

**Returns:**
- Dictionary containing customer ID, list of orders, and total count

### 2. `get_orders_ById(order_id: str)`
Gets detailed information for a specific order.

**Parameters:**
- `order_id` (str): The order ID to retrieve

**Returns:**
- Dictionary with order details (customer, amount, status, items, date created)

### 3. `create_orders(customer_id: str, product: str, quantity: int)`
Creates a new order for a customer.

**Parameters:**
- `customer_id` (str): Customer email address
- `product` (str): Product name to order
- `quantity` (int): Number of items to order

**Returns:**
- Dictionary with order confirmation details and new order ID

## Project Structure

```
OrderCreator/
├── agent.py                 # Main agent code
├── README.md               # This file
├── Pre-requisites.txt      # Setup instructions

```

## Configuration

The agent is configured with:
- **Model**: GPT-4o
- **System Prompt**: "You are a helpful assistant to manage orders for customers..."
- **Temperature**: Default (uses model defaults)

## Error Handling

The agent includes error handling for:
- Empty user input
- API errors or failed requests
- Invalid responses from the model

## Notes

- The current implementation uses mock data for demonstration purposes
- Connect to a real database by modifying the tool functions
- Store sensitive information (API keys) securely using environment variables
- The agent runs in an infinite loop until the user types "exit"

## Future Enhancements

- Integration with real database backend
- Order modification and cancellation
- Customer authentication
- Payment processing
- Order tracking and notifications
- Multi-language support

## Troubleshooting

### "Module not found" errors
Ensure you've installed all required packages:
```bash
pip install -qU langchain-openai
```

### API Key Issues
Make sure your `OPENAI_API_KEY` environment variable is set correctly:
```bash
$env:OPENAI_API_KEY = "your-api-key-here"  # PowerShell
echo $OPENAI_API_KEY  # Verify it's set
```

### Agent returns errors
Check that:
- Your OpenAI API key is valid
- You have sufficient API credits
- Your internet connection is active

## License

This project is intended for educational and demonstration purposes.

## Support

For issues or questions, refer to the LangChain documentation: https://python.langchain.com/

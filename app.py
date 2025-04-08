from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable is not set')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)
CORS(app)

# Store API key securely
API_KEY = os.getenv('EXCHANGE_API_KEY')
if not API_KEY:
    raise ValueError('EXCHANGE_API_KEY environment variable is not set')
API_BASE_URL = 'https://api.exchangerate-api.com/v4/latest/'

# Supported currencies
SUPPORTED_CURRENCIES = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW', 'SGD', 'INR', 'USDT']

# Chat responses for domain-specific interactions
CHAT_RESPONSES = {
    'greeting': 'Hello! I can help you convert between different currencies. What would you like to convert?',
    'help': 'I can help you convert between various currencies. Simply enter the amount and select the currencies you want to convert between.',
    'supported_currencies': f'I support the following currencies: {", ".join(SUPPORTED_CURRENCIES)}',
    'invalid_query': 'I can only help with currency conversions. Please ask me about converting between different currencies.',
    'error': 'Sorry, I encountered an error. Please try again with a valid currency conversion request.'
}

from currency_mapping import get_currency_code, get_supported_countries

def extract_currency_info(message):
    """Extract currency information from message using country names."""
    words = message.lower().split()
    from_currency = to_currency = None
    amount = None

    # Extract amount
    for i, word in enumerate(words):
        try:
            amount = float(word)
            break
        except ValueError:
            continue

    # Look for currency codes and country names
    for word in words:
        if word in ['to', 'into', 'in']:
            continue
        currency_code = get_currency_code(word)
        if currency_code:
            if from_currency is None:
                from_currency = currency_code
            else:
                to_currency = currency_code
                break

    return amount, from_currency, to_currency

def process_chat_message(message):
    """Process chat messages using Gemini AI"""
    try:
        # First try to extract currency conversion info
        amount, from_currency, to_currency = extract_currency_info(message)
        
        # If we have all the necessary information, perform the conversion
        if amount and from_currency and to_currency:
            exchange_rate = get_exchange_rate(from_currency, to_currency)
            if exchange_rate:
                converted_amount = amount * exchange_rate
                response = f"""
Converting {amount} {from_currency} to {to_currency}:

• Amount: {amount} {from_currency}
• Exchange Rate: 1 {from_currency} = {exchange_rate} {to_currency}
• Converted Amount: {round(converted_amount, 2)} {to_currency}

Note: Exchange rates are updated in real-time and may vary slightly."""
                return response
        
        # If no conversion possible, use Gemini AI with structured prompt
        prompt = f"""You are a currency conversion assistant. Provide a clear, structured response with:
- Greet the user
- Address their query: {message}
- If applicable, explain the conversion process
- Provide examples of valid queries
Keep the response focused on currency conversion topics."""
        
        response = model.generate_content(prompt).text
        return response

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return CHAT_RESPONSES['error']

    # If no conversion possible, check for other currency-related questions
    if any(word in message for word in ['rate', 'exchange', 'conversion']):
        return "I can help you convert between currencies. Try asking something like:\n- Convert 100 USD to EUR\n- What's 50 pounds in dollars\n- 1000 yen to yuan"
    
    return CHAT_RESPONSES['invalid_query']  # Let the conversion handler process the message

def get_exchange_rate(from_currency, to_currency):
    try:
        # Remove 'USDT' special case as it's equivalent to 'USD' for conversion
        if from_currency == 'USDT':
            from_currency = 'USD'
        if to_currency == 'USDT':
            to_currency = 'USD'
            
        url = f'{API_BASE_URL}{from_currency}'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            rates = data.get('rates', {})
            if to_currency in rates:
                return rates[to_currency]
            else:
                print(f'Target currency {to_currency} not found in rates')
                return None
        else:
            print(f'API request failed with status code: {response.status_code}')
            return None
    except Exception as e:
        print(f'Error fetching exchange rate: {str(e)}')
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bg.jpg')
def serve_background():
    return send_from_directory('templates', 'bg.jpg')

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
            
        # Process the chat message
        response = process_chat_message(message)
        if response:
            return jsonify({'response': response})
            
        # If no specific chat response, treat as conversion request
        return jsonify({'response': CHAT_RESPONSES['invalid_query']})
            
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        data = request.get_json()
        from_currency = data.get('from_currency').upper()
        to_currency = data.get('to_currency').upper()
        amount = float(data.get('amount', 0))

        if not all([from_currency, to_currency, amount]):
            return jsonify({
                'error': 'Please provide all required fields: from_currency, to_currency, and amount'
            }), 400

        if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
            return jsonify({
                'error': f'Currency not supported. Supported currencies are: {", ".join(SUPPORTED_CURRENCIES)}'
            }), 400

        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400

        exchange_rate = get_exchange_rate(from_currency, to_currency)
        
        if exchange_rate is None:
            return jsonify({'error': 'Failed to fetch exchange rate'}), 500

        converted_amount = amount * exchange_rate
        
        return jsonify({
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'converted_amount': round(converted_amount, 2),
            'exchange_rate': exchange_rate
        })

    except ValueError:
        return jsonify({'error': 'Invalid amount provided'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# Currency-converter-Chat-Bot..

A modern web application that combines real-time currency conversion with an AI-powered chatbot interface. The application provides both direct currency conversion and natural language processing capabilities for a more intuitive user experience.

## Features

- **Real-time Currency Conversion**: Convert between 15 major currencies including USD, EUR, JPY, GBP, and more
- **AI-Powered Chat Interface**: Natural language processing for conversational currency queries
- **Modern UI/UX**: Responsive design with beautiful animations and visual feedback
- **Real-time Exchange Rates**: Integration with ExchangeRate API for up-to-date conversion rates

## Technology Stack

### Backend
- **Flask**: Python web framework for the backend server
- **Google Gemini AI**: Advanced language model for natural conversation processing
- **ExchangeRate API**: Real-time currency exchange rate data
- **Python-dotenv**: Environment variable management
- **Flask-CORS**: Cross-Origin Resource Sharing support

### Frontend
- **HTML5/CSS3**: Modern, responsive layout
- **JavaScript**: Asynchronous API calls and dynamic UI updates
- **CSS Animations**: Smooth transitions and loading states
- **Flexbox/Grid**: Responsive design implementation

## Core Concepts

### 1. Currency Conversion Engine
- Direct integration with ExchangeRate API
- Support for 15 major world currencies
- Real-time exchange rate fetching
- Error handling and validation

### 2. AI Chat Integration
- Natural language processing using Google Gemini AI
- Contextual understanding of currency-related queries
- Intelligent response generation
- Fallback responses for unsupported queries

### 3. Modern Frontend Architecture
- Responsive design principles
- Glass morphism UI effects
- Real-time chat interface
- Animated loading states and transitions

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```env
   EXCHANGE_API_KEY=your_exchange_rate_api_key
   GEMINI_API_KEY=your_gemini_ai_api_key
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

### `/convert` (POST)
- Handles direct currency conversion requests
- Requires: from_currency, to_currency, amount
- Returns: converted amount and exchange rate

### `/chat` (POST)
- Processes natural language queries
- Accepts: text messages
- Returns: AI-generated responses or conversion results

## Security Features

- Environment variable protection for API keys
- Input validation and sanitization
- Error handling and rate limiting
- Secure API integration

## UI/UX Features

- Intuitive chat interface
- Real-time conversion updates
- Loading animations and visual feedback
- Mobile-responsive design
- Glass morphism effects for modern aesthetics

## Error Handling

- Comprehensive error messages
- Fallback responses for API failures
- Input validation feedback
- Network error handling

## Future Enhancements

- Historical rate tracking
- Currency rate alerts
- More currency pairs
- Advanced chat features
- Rate trend visualization

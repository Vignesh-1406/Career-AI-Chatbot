# Career Advisor Chatbot using Gemini API

A production-ready, AI-powered career guidance chatbot built with Python, Streamlit, and Google Gemini API. Provides structured, practical, step-by-step career advice with multi-turn conversation support.

## 🎯 Features

- **Intelligent Career Guidance**: Powered by Google's Gemini API with expertly-crafted system prompts
- **Multi-Turn Conversations**: Maintains context across multiple messages
- **Session Management**: Conversation history with optimization
- **Professional UI**: Clean Streamlit interface with chat-like experience
- **Production-Ready**: Clean architecture, comprehensive logging, error handling
- **Modular Design**: Separation of concerns with domain, service, and UI layers
- **Configuration Management**: Environment-based configuration with validation

## 🏗️ Architecture

The project follows **Clean Architecture** principles:

```
chatbot/
├── app.py                          # UI Layer (Streamlit)
├── config.py                       # Configuration Management
├── services/
│   └── gemini_service.py          # Gemini API Integration Layer
├── prompts/
│   └── system_prompt.py           # Prompt Engineering
├── memory/
│   └── session_memory.py          # Session State Management
├── utils/
│   └── logger.py                  # Logging Utility
├── requirements.txt                # Python Dependencies
├── .env.example                    # Environment Template
└── README.md                       # This file
```

### Architecture Layers

| Layer | File | Responsibility |
|-------|------|-----------------|
| **Presentation** | `app.py` | Streamlit UI, user interactions |
| **Application** | Services, Memory | Business logic orchestration |
| **Domain** | `services/gemini_api.py` | External API integration |
| **Infrastructure** | `config.py`, `utils/` | Configuration, logging |

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- pip package manager

### Installation

1. **Clone or navigate to the project directory**

```bash
cd path/to/chatbot
```

2. **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment configuration**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get it from: https://aistudio.google.com/app/apikeys
```

5. **Run the application**

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔑 Getting Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in the `.env` file as `GEMINI_API_KEY=your_key_here`

## 📋 Configuration

Edit `.env` file to customize:

```env
# API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# Response Behavior
TEMPERATURE=0.7          # 0=deterministic, 1=creative
MAX_TOKENS=1024         # Max response length

# Session Management
MAX_CONVERSATION_HISTORY=20
SESSION_TIMEOUT_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `GEMINI_API_KEY` | - | Your API key (required) |
| `GEMINI_MODEL` | gemini-1.5-pro | AI model version |
| `TEMPERATURE` | 0.7 | Response creativity (0.0-1.0) |
| `MAX_TOKENS` | 1024 | Max response length |
| `MAX_CONVERSATION_HISTORY` | 20 | Messages to keep in memory |
| `LOG_LEVEL` | INFO | Logging detail level |

## 🚀 Usage

### Basic Usage

1. **Start the app** with `streamlit run app.py`
2. **Ask a career question** in the chat input
3. **Get AI-powered guidance** in real-time

### Example Prompts

- "Help me plan a career transition from finance to tech"
- "What skills do I need to become a data scientist?"
- "How do I prepare for a senior manager interview?"
- "Create a 12-month career development plan for me"
- "How can I negotiate a better salary?"

### Sidebar Features

- **Session Statistics**: View conversation metrics
- **API Status**: Check Gemini API connection
- **Test Connection**: Verify API configuration
- **Clear History**: Reset conversation
- **Export Conversation**: Download as JSON

## 📊 Project Structure Details

### `app.py` - Streamlit UI Layer
- Page configuration and styling
- Session state management
- Chat interface rendering
- User input handling
- Response generation orchestration

### `config.py` - Configuration Management
- Environment variable loading
- Configuration validation
- Centralized settings management
- Default values with overrides

### `services/gemini_service.py` - API Integration
- Gemini API communication
- Error handling and retries
- Response processing
- Fallback responses
- API metrics logging

### `prompts/system_prompt.py` - Prompt Engineering
- System prompt definition
- Career advisor role specification
- Response format guidelines
- Domain constraints
- Request templates

### `memory/session_memory.py` - Session Management
- Conversation history tracking
- Multi-turn context preservation
- Memory optimization
- Session statistics
- Export/import functionality

### `utils/logger.py` - Logging Utility
- Centralized logging configuration
- File and console handlers
- Rotating file handler
- Structured logging methods
- API call tracking

## 🔍 Key Features Explained

### Multi-Turn Conversations

The chatbot maintains full conversation context:

```python
# System automatically maintains history
# Each response includes all previous messages
conversation_history = [
    {"role": "user", "content": "I want to switch careers"},
    {"role": "assistant", "content": "Great! Let's explore that..."},
    {"role": "user", "content": "I'm from finance"},
    # System remembers previous context
]
```

### Error Handling

Comprehensive error handling with fallback responses:

- API connection failures → Graceful fallback
- Blocked prompts → Safe user notification
- Invalid responses → Retry or inform user
- Configuration errors → Clear validation messages

### Session Memory Optimization

Automatically manages memory:

```python
# Keeps last N messages to prevent memory bloat
# Falls back to recent context if history too long
# Tracks session statistics and metrics
session_memory.optimize_memory()
```

## 🧪 Testing

### Test API Connection

```bash
# From the Streamlit UI
Click "Test API Connection" in the sidebar
```

### Test Locally

```python
# Python shell test
from services.gemini_service import GeminiService

is_connected = GeminiService.test_connection()
print("Connected!" if is_connected else "Failed to connect")
```

## 📝 Logging

Logs are written to `app.log`:

```
2025-02-18 10:30:45 - chatbot - INFO - Gemini API configured successfully
2025-02-18 10:31:20 - chatbot - INFO - User Interaction - Message Length: 45
2025-02-18 10:31:25 - chatbot - DEBUG - API Metrics - Input: 234, Output: 567
```

View logs:
```bash
tail -f app.log        # macOS/Linux
Get-Content app.log -Tail 10 -Wait  # Windows PowerShell
```

## 🛠️ Development

### Adding New Features

1. **Add to appropriate layer** (UI → app.py, API → services, Config → config.py)
2. **Follow existing patterns** (logging, error handling, type hints)
3. **Add comprehensive docstrings** with Args, Returns, Raises
4. **Update this README** with new usage examples
5. **Test thoroughly** with various inputs

### Extending the Chatbot

#### Add New Career Guidance Module

```python
# In prompts/system_prompt.py
class NewGuidanceModule:
    PROMPT = "Your specialized prompt here..."
    
    @staticmethod
    def get_prompt():
        return NewGuidanceModule.PROMPT
```

#### Add Custom Response Processing

```python
# In services/gemini_service.py
def process_response(self, response):
    # Add custom processing logic
    return processed_response
```

## ⚠️ Important Notes

### Security

- **Never commit `.env` file** to version control
- **Rotate API keys** regularly
- **Use environment variables** for all secrets
- **Request logging** doesn't log sensitive data by default

### Rate Limiting

- **Free tier**: Limited requests per minute
- **Monitor logs** for rate limit errors
- **Use `MAX_CONVERSATION_HISTORY`** to control token usage

### Best Practices

1. ✅ Keep API key in `.env`, never hardcode
2. ✅ Use virtual environment for dependencies
3. ✅ Review logs regularly for errors
4. ✅ Optimize conversation history for performance
5. ✅ Test configuration before deployment

## 🐛 Troubleshooting

### "GEMINI_API_KEY not set" Error

```bash
# Solution: Make sure .env file exists and has API key
cp .env.example .env
# Edit .env with your actual API key
```

### API Connection Fails

```bash
# Check API key is correct
# Verify internet connection
# Try test connection button in sidebar
# Check logs: tail -f app.log
```

### Empty Response from API

```bash
# Check logs for error details
# Verify model name is correct in .env
# Try simpler test question
# Increase MAX_TOKENS if response cuts off
```

### High Token Usage

```bash
# Reduce MAX_CONVERSATION_HISTORY
# Decrease MAX_TOKENS
# Clear history frequently
```

## 📚 Resources

- [Google Gemini API](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python dotenv Guide](https://github.com/theskumar/python-dotenv)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 🤝 Contributing

To enhance this project:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include logging for debugging
4. Update README with changes
5. Test thoroughly before committing

## 📄 License

This project is provided as-is for educational and development purposes.

## 🎓 Learning Outcomes

This project demonstrates:

- Clean Architecture principles
- API integration best practices
- Session/state management
- Error handling and logging
- Environment configuration
- Streamlit UI development
- Production-ready code standards

---

**Need Help?**
- Check the [Troubleshooting](#-troubleshooting) section
- Review logs in `app.log`
- Verify your `.env` configuration
- Test API connection from the sidebar

**Last Updated**: February 2025

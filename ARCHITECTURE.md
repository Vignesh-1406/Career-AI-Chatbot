"""
Architecture Documentation for Career Advisor Chatbot

This document explains the clean architecture design and how components interact.
"""

# ============================================================================
# ARCHITECTURE OVERVIEW
# ============================================================================

"""
The Career Advisor Chatbot follows Clean Architecture principles to ensure:
- Modularity: Each component has a single responsibility
- Testability: Components can be tested independently
- Maintainability: Easy to understand and modify
- Scalability: Simple to add new features

Architecture Layers (from outside to inside):
1. Presentation Layer (UI)
2. Application Layer (Business Logic)
3. Domain Layer (Core Logic)
4. Infrastructure Layer (External Services & Utilities)


                    ┌─────────────────────────┐
                    │   UI LAYER (Streamlit)  │
                    │      (app.py)           │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  APPLICATION LAYER      │
                    │  - Memory Management    │
                    │  - Service Orchestration│
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
    ┌───▼────────┐  ┌───────────▼──────────┐  ┌──────────▼──┐
    │ SERVICES   │  │ PROMPTS & CONFIG │  │ MEMORY      │
    │ (Gemini)   │  │ (Prompt Eng)    │  │ (Session)   │
    └────────────┘  └──────────────────┘  └─────────────┘
        │                    │                    │
    ┌───▼────────────────────▼────────────────────▼──────┐
    │       INFRASTRUCTURE LAYER                         │
    │  - Logging (logger.py)                            │
    │  - Configuration (config.py)                      │
    │  - Utilities (utils/)                             │
    └───┬─────────────────────────────────────────────────┘
        │
    ┌───▼──────────────────────────────────────────────┐
    │  EXTERNAL SERVICES                              │
    │  - Google Gemini API                            │
    │  - Environment Variables                         │
    │  - File System (Logging)                        │
    └──────────────────────────────────────────────────┘
"""


# ============================================================================
# COMPONENT RESPONSIBILITIES
# ============================================================================

"""
1. PRESENTATION LAYER (app.py)
   ├─ Responsibilities:
   │  ├─ Render UI components (chat interface, sidebar)
   │  ├─ Handle user interactions (input, buttons)
   │  ├─ Manage Streamlit session state
   │  ├─ Route requests to services
   │  └─ Display responses to user
   │
   ├─ Key Functions:
   │  ├─ configure_page(): Page setup and styling
   │  ├─ initialize_session_state(): State management
   │  ├─ render_sidebar(): Sidebar UI and controls
   │  ├─ render_chat_interface(): Main chat UI
   │  ├─ render_conversation_history(): Message display
   │  ├─ render_input_area(): User input handling
   │  └─ get_assistant_response(): API integration
   │
   └─ Dependencies:
      ├─ config.py (Configuration)
      ├─ services/gemini_service.py (API calls)
      ├─ memory/session_memory.py (State)
      ├─ prompts/system_prompt.py (Prompts)
      └─ utils/logger.py (Logging)


2. APPLICATION LAYER
   │
   ├─ services/gemini_service.py (API Integration)
   │  ├─ Responsibilities:
   │  │  ├─ Handle Gemini API communication
   │  │  ├─ Error handling and recovery
   │  │  ├─ Response validation
   │  │  ├─ Logging and monitoring
   │  │  └─ Fallback response generation
   │  │
   │  ├─ Key Methods:
   │  │  ├─ send_message(): Main API call
   │  │  ├─ validate_response(): Quality checks
   │  │  ├─ get_model_info(): Configuration info
   │  │  ├─ test_connection(): Connection testing
   │  │  └─ _get_fallback_response(): Error handling
   │  │
   │  └─ Dependencies:
   │     ├─ config.py (API key, settings)
   │     ├─ prompts/system_prompt.py (Prompts)
   │     └─ utils/logger.py (Logging)
   │
   ├─ memory/session_memory.py (State Management)
   │  ├─ Responsibilities:
   │  │  ├─ Maintain conversation history
   │  │  ├─ Context preservation
   │  │  ├─ Memory optimization
   │  │  ├─ Session statistics
   │  │  └─ Conversation export/import
   │  │
   │  ├─ Key Methods:
   │  │  ├─ add_user_message(): Store user input
   │  │  ├─ add_assistant_message(): Store response
   │  │  ├─ get_conversation_history(): Format for API
   │  │  ├─ optimize_memory(): Memory management
   │  │  ├─ clear_history(): Reset session
   │  │  └─ export_conversation(): Data export
   │  │
   │  └─ Dependencies:
   │     ├─ config.py (Settings)
   │     └─ utils/logger.py (Logging)
   │
   └─ prompts/system_prompt.py (Prompt Engineering)
      ├─ Responsibilities:
      │  ├─ Define system prompt
      │  ├─ Provide response templates
      │  ├─ Context-based prompt selection
      │  └─ Prompt optimization
      │
      ├─ Key Classes:
      │  ├─ SystemPrompt: Main career advisor prompt
      │  ├─ ResponseTemplate: Response formatting
      │  └─ get_prompt_for_context(): Dynamic prompts
      │
      └─ Dependencies:
         └─ None (Pure configuration)


3. INFRASTRUCTURE LAYER
   │
   ├─ config.py (Configuration Management)
   │  ├─ Responsibilities:
   │  │  ├─ Load environment variables
   │  │  ├─ Validate configuration
   │  │  ├─ Provide centralized settings
   │  │  └─ Set defaults
   │  │
   │  ├─ Key Classes:
   │  │  └─ Config: Centralized settings class
   │  │
   │  └─ Load Order:
   │     1. Load .env file
   │     2. Read environment variables
   │     3. Apply defaults
   │     4. Validate on access
   │
   └─ utils/logger.py (Logging)
      ├─ Responsibilities:
      │  ├─ Configure logging handlers
      │  ├─ Provide centralized logger
      │  ├─ Log to file and console
      │  ├─ Track API calls
      │  └─ Error logging
      │
      ├─ Key Methods:
      │  ├─ get_logger(): Get logger instance
      │  ├─ log_api_call(): API metrics
      │  ├─ log_error(): Error tracking
      │  └─ log_user_interaction(): Audit trail
      │
      └─ Dependencies:
         └─ config.py (Log settings)
"""


# ============================================================================
# DATA FLOW
# ============================================================================

"""
USER INPUT FLOW:
─────────────────

1. User types message in Streamlit UI
   └─→ app.py: render_input_area()
   
2. Message added to session memory
   └─→ memory_session.py: add_user_message()
   
3. Display user message in chat
   └─→ app.py: render_chat_interface()
   
4. Get conversation history
   └─→ memory_session.py: get_conversation_history()
   
5. Send to Gemini API
   └─→ services/gemini_service.py: send_message()
   
6. Gemini processes with system prompt
   └─→ prompts/system_prompt.py: SystemPrompt.get_system_prompt()
   
7. Validate response
   └─→ services/gemini_service.py: validate_response()
   
8. Add response to memory
   └─→ memory_session.py: add_assistant_message()
   
9. Display response in chat
   └─→ app.py: render_chat_interface()
   
10. Log interaction
    └─→ utils/logger.py: ChatbotLogger.log_user_interaction()


API CALL DETAILS:
─────────────────

Request Object:
{
  "role": "user/assistant",
  "content": "message text"
}

Gemini Configuration:
{
  "model": Config.GEMINI_MODEL,
  "system_instruction": SystemPrompt.get_system_prompt(),
  "generation_config": {
    "temperature": Config.TEMPERATURE,
    "max_output_tokens": Config.MAX_TOKENS
  }
}

Response Processing:
1. Extract text from response
2. Validate content
3. Log metrics
4. Handle errors gracefully
5. Return to UI
"""


# ============================================================================
# ERROR HANDLING STRATEGY
# ============================================================================

"""
ERROR HANDLING FLOW:
────────────────────

API Error
    │
    ├─→ BlockedPromptException
    │   └─→ Log warning
    │   └─→ Return safe fallback
    │
    ├─→ APIError
    │   └─→ Log error details
    │   └─→ Return connection error fallback
    │
    └─→ General Exception
        └─→ Log traceback
        └─→ Return generic error fallback


FALLBACK RESPONSES:
───────────────────
- Blocked content: "I'm not able to provide guidance on this topic..."
- API Error: "I'm experiencing technical difficulties..."
- Empty Response: "Failed to generate response. Please try again."


VALIDATION LAYERS:
──────────────────
1. Configuration validation (config.py)
   ├─ Check API key present
   ├─ Validate temperature range
   ├─ Check token limits
   
2. Input validation
   ├─ Non-empty user input
   ├─ Reasonable message length
   
3. Response validation
   ├─ Non-empty response
   ├─ Minimum length check
   ├─ Type verification
"""


# ============================================================================
# DESIGN PATTERNS USED
# ============================================================================

"""
1. SINGLETON PATTERN
   └─ Config class: Single instance throughout app
   └─ Logger: Centralized logging instance

2. SERVICE LOCATOR PATTERN
   └─ Streamlit session state manages service instances
   └─ app.py orchestrates service calls

3. REPOSITORY PATTERN
   └─ SessionMemory acts as repository for conversation data

4. TEMPLATE METHOD PATTERN
   └─ SystemPrompt defines response templates
   └─ GeminiService follows template for API calls

5. FACTORY PATTERN
   └─ get_logger() factory method
   └─ get_prompt_for_context() factory method
"""


# ============================================================================
# EXTENSION POINTS
# ============================================================================

"""
1. ADD NEW CAREER GUIDANCE DOMAIN
   Location: prompts/system_prompt.py
   Add new ResponseTemplate class
   Create domain-specific prompt
   
2. ADD NEW MEMORY STORAGE
   Location: memory/session_memory.py
   Extend SessionMemory class
   Add persistence methods
   
3. ADD NEW LOGGING HANDLER
   Location: utils/logger.py
   Extend ChatbotLogger class
   Add handler in _initialize_logger()
   
4. ADD NEW AI MODEL SUPPORT
   Location: services/gemini_service.py
   Add model selection logic
   Handle model-specific parameters
   
5. ADD NEW UI COMPONENTS
   Location: app.py
   Create render_* functions
   Use Streamlit components
"""


# ============================================================================
# TESTING STRATEGY
# ============================================================================

"""
UNIT TESTS:
───────────
- config.py: Test configuration loading and validation
- memory/session_memory.py: Test message management
- prompts/system_prompt.py: Test prompt generation
- utils/logger.py: Test logging output

INTEGRATION TESTS:
──────────────────
- services/gemini_service.py: Test API integration
- app.py: Test UI with mock services

END-TO-END TESTS:
─────────────────
- Full conversation flow
- Error scenarios
- Session persistence
"""


# ============================================================================
# DEPLOYMENT CONSIDERATIONS
# ============================================================================

"""
PRODUCTION CHECKLIST:
─────────────────────
□ API key in environment variables (not hardcoded)
□ Error handling covers all edge cases
□ Logging configured for production
□ Rate limiting considered
□ Memory optimization enabled
□ Security headers configured
□ CORS configured for deployment
□ Performance monitoring enabled
□ Backup/recovery strategy
□ Monitoring and alerts setup
"""


# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

"""
MEMORY OPTIMIZATION:
────────────────────
- SessionMemory.optimize_memory() removes old messages
- MAX_CONVERSATION_HISTORY limits memory usage
- get_context_window() manages token usage

API OPTIMIZATION:
─────────────────
- Reuse model instance where possible
- Batch similar requests
- Implement request caching if needed

UI OPTIMIZATION:
────────────────
- Lazy loading of components
- Efficient rendering in Streamlit
- Session state for avoiding reruns
"""

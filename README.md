AI Assistant Bot
Telegram bot and web interface with AI based on Pollinations AI.
Backend: FastAPI (REST API)
- Frontend: Streamlit (web interface)
- Additional: Telegram bot
- AI: Pollinations AI (free, no API keys)
- Database: SQLite

Project Structure:
backend FastAPI:
1)api.py - REST API endpoints
2)database.py - Database operations
3)pollinations_client.py - AI client
Streamlit frontend:
1)app.py - Web interface
2) utils - Utilities
3) init_db.py - Database initialization
bot.py - Telegram bot
req.txt - Dependencies
.env - Environment variables

Features:
1)Chat with AI in Telegram
2)Web interface with chat
3)Conversation history in database
4)Free AI (Pollinations)

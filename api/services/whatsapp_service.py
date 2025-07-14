import logging
import time
from typing import Dict, Optional, Any

from config import settings

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self, rag_service=None, translation_service=None, maps_service=None, weather_service=None):
        self.rag_service = rag_service
        self.translation_service = translation_service
        self.maps_service = maps_service
        self.weather_service = weather_service
        
        self.twilio_account_sid = settings.twilio_account_sid
        self.twilio_auth_token = settings.twilio_auth_token
        self.twilio_phone_number = settings.twilio_phone_number
        
        # User session states
        self.user_sessions = {}  # phone_number -> session_state
        
    def initialize(self):
        """Initialize the WhatsApp service"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            logger.warning("Twilio credentials not configured - WhatsApp features will be disabled")
        else:
            logger.info("WhatsApp service initialized successfully")
    
    def get_user_session(self, user_phone: str) -> Dict[str, Any]:
        """Get or create user session"""
        if user_phone not in self.user_sessions:
            self.user_sessions[user_phone] = {
                "state": "welcome",
                "data": {}
            }
        return self.user_sessions[user_phone]
    
    def reset_user_session(self, user_phone: str):
        """Reset user session to welcome state"""
        self.user_sessions[user_phone] = {
            "state": "welcome",
            "data": {}
        }
    
    def get_welcome_message(self) -> str:
        """Generate the initial welcome message"""
        return """🌍 *Welcome to Hura Tourism Chatbot!*

I'm your AI assistant for exploring Kigali, Rwanda. I can help you with:

• Tourism information and recommendations
• English ↔ Kinyarwanda translation
• Location and directions help
• Weather information

*How to get started:*
Type *menu* to see all available services and start exploring!

🇷🇼 Ready to explore Rwanda? Type *menu* to begin!"""
    
    def get_main_menu(self) -> str:
        """Generate the main menu"""
        return """📋 *Main Menu*

Please select a service:

1️⃣ *Ask Questions*
Get information about Kigali, attractions, culture, and tourism.

2️⃣ *Translation*
Translate between English and Kinyarwanda.

3️⃣ *Location Help*
Find places, get directions, and discover nearby locations.

4️⃣ *Weather*
Get current weather and forecasts for Kigali.

---
*Commands:*
• Type a number (1-4) to select a service
• Type *menu* to see this menu again
• Type *quit* to reset and start over"""
    
    def get_translation_menu(self) -> str:
        """Generate the translation sub-menu"""
        return """🔄 *Translation Service*

Choose a translation direction:

a) *English to Kinyarwanda*
Translate English text to Kinyarwanda.

b) *Kinyarwanda to English*
Translate Kinyarwanda text to English.

---
*Commands:*
• Type 'a' or 'b' to select direction
• Type *menu* to go back to main menu
• Type *quit* to reset and start over"""
    
    def get_location_menu(self) -> str:
        """Generate the location service menu"""
        return """🗺️ *Location Service*

I can help you find places and get directions in Kigali.

*Examples of what you can ask:*
• "Where is Kimironko market?"
• "How do I get to Kigali Genocide Memorial?"
• "Find restaurants near me"
• "Directions to Kigali International Airport"

Please type your location question:

---
*Commands:*
• Type *menu* to go back to main menu
• Type *quit* to reset and start over"""
    
    def get_weather_menu(self) -> str:
        """Generate the weather service menu"""
        return """🌤️ *Weather Service*

I can provide weather information for Kigali.

*Examples of what you can ask:*
• "What's the weather today?"
• "Weather forecast for this week"
• "Is it going to rain tomorrow?"
• "Temperature in Kigali"

Please type your weather question:

---
*Commands:*
• Type *menu* to go back to main menu
• Type *quit* to reset and start over"""
    
    def get_qa_menu(self) -> str:
        """Generate the Q&A service menu"""
        return """🤖 *Question & Answer Service*

I can answer questions about Kigali, Rwanda, tourism, culture, and attractions.

*Examples of what you can ask:*
• "Tell me about Kigali Genocide Memorial"
• "What are the best restaurants in Kigali?"
• "How safe is Kigali for tourists?"
• "What's the best time to visit Rwanda?"
• "Tell me about Rwandan culture"

Please type your question:

---
*Commands:*
• Type *menu* to go back to main menu
• Type *quit* to reset and start over"""
    
    def process_qa_query(self, query: str) -> str:
        """Process a Q&A query using local RAG service"""
        if not self.rag_service:
            return "❌ Q&A service is not available at the moment. Please try again later."
        
        try:
            start_time = time.time()
            response = self.rag_service.query(query)
            process_time = time.time() - start_time
            
            # Format for WhatsApp
            formatted_response = f"🤖 *Answer:*\n{response}"
            
            return formatted_response
        except Exception as e:
            logger.error(f"Q&A processing error: {e}")
            return "❌ Sorry, I couldn't process your question. Please try again."
    
    def process_translation(self, text: str, direction: str = "en2rw") -> str:
        """Process a translation request using local translation service"""
        if not self.translation_service:
            return "❌ Translation service is not available at the moment. Please try again later."
        
        if not text.strip():
            return "❌ Please provide text to translate."
        
        try:
            if direction == "en2rw":
                translation = self.translation_service.translate_en_to_rw(text)
            else:
                translation = self.translation_service.translate_rw_to_en(text)
            
            source_lang = "English" if direction == "en2rw" else "Kinyarwanda"
            target_lang = "Kinyarwanda" if direction == "en2rw" else "English"
            
            return f"🔄 *Translation ({source_lang} → {target_lang}):*\n\n*Original:* {text}\n*Translation:* {translation}"
        except Exception as e:
            logger.error(f"Translation processing error: {e}")
            return "❌ Translation failed. Please try again."
    
    def process_maps_query(self, query: str) -> str:
        """Process a maps/location query using local maps service and add Google Maps link"""
        if not self.maps_service:
            return "❌ Location service is not available at the moment. Please check with your hotel or local information center."
        try:
            response = self.maps_service.process_maps_query(query)
            # Try to extract an address or location from the response for the Google Maps link
            # We'll use the first line or the whole response as the search query
            address = response.split('\n')[0] if '\n' in response else response
            maps_url = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"
            return f"🗺️ *Location Information:*\n{response}\n\n🌐 [Open in Google Maps]({maps_url})"
        except Exception as e:
            logger.error(f"Maps processing error: {e}")
            return "❌ Location service is not available at the moment. Please check with your hotel or local information center."
    
    def process_weather_query(self, query: str) -> str:
        """Process a weather query using local weather service"""
        if not self.weather_service:
            return "❌ Weather service is not available at the moment. Please check a weather app or website."
        
        try:
            response = self.weather_service.process_weather_query(query)
            return f"🌤️ *Weather Information:*\n{response}"
        except Exception as e:
            logger.error(f"Weather processing error: {e}")
            return "❌ Weather service is not available at the moment. Please check a weather app or website."
    
    def process_message(self, message: str, user_phone: str) -> str:
        """Main message processing function with state management"""
        try:
            # Get user session
            session = self.get_user_session(user_phone)
            current_state = session["state"]
            message_lower = message.lower().strip()
            
            logger.info(f"Processing message from {user_phone}: '{message}' (state: {current_state})")
            
            # Handle global commands
            if message_lower == "quit":
                self.reset_user_session(user_phone)
                return self.get_welcome_message()
            
            if message_lower == "menu":
                session["state"] = "main_menu"
                return self.get_main_menu()
            
            # Handle different states
            if current_state == "welcome":
                # Welcome state - show welcome message and wait for menu request
                if message_lower in ["menu", "help", "start"]:
                    session["state"] = "main_menu"
                    return self.get_main_menu()
                else:
                    # Show welcome message and stay in welcome state
                    return self.get_welcome_message()
            
            elif current_state == "main_menu":
                return self.handle_main_menu(message, session)
            
            elif current_state == "translation_menu":
                return self.handle_translation_menu(message, session)
            
            elif current_state == "translation_input":
                return self.handle_translation_input(message, session)
            
            elif current_state == "qa_input":
                return self.handle_qa_input(message, session)
            
            elif current_state == "location_input":
                return self.handle_location_input(message, session)
            
            elif current_state == "weather_input":
                return self.handle_weather_input(message, session)
            
            else:
                # Unknown state, reset to welcome
                self.reset_user_session(user_phone)
                return self.get_welcome_message()
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "❌ Sorry, I encountered an error. Please try again or type 'menu' for help."
    
    def handle_main_menu(self, message: str, session: Dict[str, Any]) -> str:
        """Handle main menu selection"""
        message_lower = message.lower().strip()
        
        if message_lower in ["1", "1.", "one"]:
            session["state"] = "qa_input"
            return self.get_qa_menu()
        
        elif message_lower in ["2", "2.", "two"]:
            session["state"] = "translation_menu"
            return self.get_translation_menu()
        
        elif message_lower in ["3", "3.", "three"]:
            session["state"] = "location_input"
            return self.get_location_menu()
        
        elif message_lower in ["4", "4.", "four"]:
            session["state"] = "weather_input"
            return self.get_weather_menu()
        
        else:
            return """❌ Please select a valid option (1-4).

📋 *Main Menu*

1️⃣ Ask Questions
2️⃣ Translation  
3️⃣ Location Help
4️⃣ Weather

Type a number to continue, or type *menu* to see the full menu again."""
    
    def handle_translation_menu(self, message: str, session: Dict[str, Any]) -> str:
        """Handle translation menu selection"""
        message_lower = message.lower().strip()
        
        if message_lower in ["a", "a.", "english to kinyarwanda"]:
            session["state"] = "translation_input"
            session["data"]["direction"] = "en2rw"
            return """🔄 *English to Kinyarwanda Translation*

Please type the English text you want to translate:

*Example:* Hello, how are you?

---
Type *menu* to go back to main menu"""
        
        elif message_lower in ["b", "b.", "kinyarwanda to english"]:
            session["state"] = "translation_input"
            session["data"]["direction"] = "rw2en"
            return """🔄 *Kinyarwanda to English Translation*

Please type the Kinyarwanda text you want to translate:

*Example:* Muraho, amakuru?

---
Type *menu* to go back to main menu"""
        
        else:
            return """❌ Please select a valid option (a or b).

🔄 *Translation Service*

a) English to Kinyarwanda
b) Kinyarwanda to English

Type 'a' or 'b' to continue, or type *menu* to go back."""
    
    def handle_translation_input(self, message: str, session: Dict[str, Any]) -> str:
        """Handle translation text input"""
        direction = session["data"].get("direction", "en2rw")
        result = self.process_translation(message, direction)
        # Stay in translation_input state until menu/quit
        return f"{result}\n\n📋 Type *menu* to see other services, or send another sentence to translate."

    def handle_qa_input(self, message: str, session: Dict[str, Any]) -> str:
        """Handle Q&A text input"""
        result = self.process_qa_query(message)
        # Stay in qa_input state until menu/quit
        return f"{result}\n\n📋 Type *menu* to see other services, or ask another question."

    def handle_location_input(self, message: str, session: Dict[str, Any]) -> str:
        """Handle location text input"""
        result = self.process_maps_query(message)
        # Stay in location_input state until menu/quit
        return f"{result}\n\n📋 Type *menu* to see other services, or ask another location question."

    def handle_weather_input(self, message: str, session: Dict[str, Any]) -> str:
        """Handle weather text input"""
        result = self.process_weather_query(message)
        # Stay in weather_input state until menu/quit
        return f"{result}\n\n📋 Type *menu* to see other services, or ask another weather question."
    
    def send_whatsapp_message(self, to_phone: str, message: str) -> bool:
        """Send a WhatsApp message via Twilio"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            logger.error("Twilio credentials not configured")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            # Format phone number for WhatsApp
            if not to_phone.startswith('whatsapp:'):
                to_phone = f"whatsapp:{to_phone}"
            
            from_phone = f"whatsapp:{self.twilio_phone_number}"
            
            message = client.messages.create(
                body=message,
                from_=from_phone,
                to=to_phone
            )
            
            logger.info(f"WhatsApp message sent: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False 
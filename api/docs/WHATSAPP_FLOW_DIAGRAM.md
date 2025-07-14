# 📱 WhatsApp Menu-Based Flow Diagram

## 🔄 **Complete User Journey**

```
User sends "Hi" or any greeting
           ↓
    ┌─────────────────┐
    │   Welcome       │
    │   Message       │
    │   + Main Menu   │
    └─────────────────┘
           ↓
    User selects option
           ↓
    ┌─────────────────┐
    │   Main Menu     │
    │   1. Ask Q&A    │
    │   2. Translation│
    │   3. Location   │
    │   4. Weather    │
    └─────────────────┘
           ↓
    User types number (1-4)
           ↓
    ┌─────────────────┐
    │ Service Menu    │
    │ (Q&A/Location/  │
    │  Weather) OR    │
    │ Translation     │
    │ Direction Menu  │
    └─────────────────┘
           ↓
    User provides input
           ↓
    ┌─────────────────┐
    │   API Call      │
    │   + Response    │
    └─────────────────┘
           ↓
    ┌─────────────────┐
    │ Return to       │
    │ Main Menu       │
    └─────────────────┘
```

## 📋 **Detailed Flow Breakdown**

### **1. Initial Contact**

```
User: "Hi"
Bot: Welcome message
User: "menu"
Bot: Main menu
```

### **2. Main Menu Selection**

```
User: "1" (Q&A)
Bot: Q&A service menu

User: "2" (Translation)
Bot: Translation direction menu

User: "3" (Location)
Bot: Location service menu

User: "4" (Weather)
Bot: Weather service menu
```

### **3. Service-Specific Flows**

#### **Q&A Flow:**

```
User: "1"
Bot: "Question & Answer Service - Please type your question:"
User: "Tell me about Kigali"
Bot: [Tourism information response]
Bot: "Type menu to see other services"
```

#### **Translation Flow:**

```
User: "2"
Bot: "Translation Service - Choose direction: a) English→Kinyarwanda b) Kinyarwanda→English"
User: "a"
Bot: "English to Kinyarwanda - Please type English text:"
User: "Hello, how are you?"
Bot: [Translation response]
Bot: "Type menu to see other services"
```

#### **Location Flow:**

```
User: "3"
Bot: "Location Service - Please type your location question:"
User: "Where is Kimironko?"
Bot: [Location information response]
Bot: "Type menu to see other services"
```

#### **Weather Flow:**

```
User: "4"
Bot: "Weather Service - Please type your weather question:"
User: "What's the weather today?"
Bot: [Weather information response]
Bot: "Type menu to see other services"
```

## 🎯 **Global Commands**

### **Available at Any Time:**

- **`menu`** → Returns to main menu
- **`quit`** → Resets conversation to welcome

### **Error Handling:**

- **Invalid option** → Shows error + valid options
- **Empty input** → Prompts for valid input
- **Service unavailable** → Graceful fallback message

## 📱 **WhatsApp Message Examples**

### **Complete Q&A Session:**

```
User: Hi
Bot: 🌍 Welcome to Hura Tourism Chatbot!
     I'm your AI assistant for exploring Kigali, Rwanda...
     Type menu to see all available services and start exploring!

User: menu
Bot: 📋 Main Menu
     Please select a service:
     1️⃣ Ask Questions
     2️⃣ Translation
     3️⃣ Location Help
     4️⃣ Weather

User: 1
Bot: 🤖 Question & Answer Service
     I can answer questions about Kigali, Rwanda, tourism...
     Please type your question:

User: Tell me about Kigali Genocide Memorial
Bot: 🤖 Answer:
     The Kigali Genocide Memorial is a powerful and moving tribute...
     ⏱️ Processed in 2.34 seconds
     📋 Type menu to see other services
```

### **Complete Translation Session:**

```
User: 2
Bot: 🔄 Translation Service
     Choose a translation direction:
     a) English to Kinyarwanda
     b) Kinyarwanda to English

User: a
Bot: 🔄 English to Kinyarwanda Translation
     Please type the English text you want to translate:
     Example: Hello, how are you?

User: Hello, how are you?
Bot: 🔄 Translation (English → Kinyarwanda):
     Original: Hello, how are you?
     Translation: Muraho, amakuru?
     📋 Type menu to see other services
```

## 🔧 **State Management**

### **Session States:**

- **`welcome`** → Initial state
- **`main_menu`** → Main menu displayed
- **`qa_input`** → Waiting for Q&A question
- **`translation_menu`** → Translation direction selection
- **`translation_input`** → Waiting for translation text
- **`location_input`** → Waiting for location question
- **`weather_input`** → Waiting for weather question

### **Session Data:**

- **Translation direction** → "en2rw" or "rw2en"
- **User preferences** → Future enhancements

## 🎨 **User Experience Features**

### **Visual Elements:**

- **Emojis** for visual appeal
- **Bold text** for emphasis
- **Numbered options** for clarity
- **Clear sections** with headers

### **User-Friendly Features:**

- **Examples** in each menu
- **Clear instructions** at each step
- **Error messages** with helpful guidance
- **Processing time** for transparency
- **Easy navigation** with menu/quit commands

### **Accessibility:**

- **Case-insensitive** commands
- **Multiple input formats** (1, 1., one)
- **Graceful error handling**
- **Clear feedback** at each step

---

**This menu-based approach provides a structured, user-friendly experience that guides users through each service step-by-step! 🇷🇼📱**

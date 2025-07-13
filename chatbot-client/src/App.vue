<template>
  <div id="app">
    <div class="chat-container">
      <div class="chat-header">
        <h1>Povo Chatbot</h1>
        <div class="session-info" v-if="currentSession">
          <small>Flow: {{ getCurrentFlow() }} | Session: {{ sessionId.substring(0, 8) }}...</small>
        </div>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message', message.type]"
        >
          <div class="message-content">
            <div class="message-text">{{ message.text }}</div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <input 
          v-model="userInput" 
          @keyup.enter="sendMessage"
          placeholder="Type your message..."
          :disabled="isLoading"
        />
        <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
          {{ isLoading ? 'Sending...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false,
      sessionId: this.generateSessionId(),
      userId: this.generateUserId(),
      currentSession: null, // Store the current session object
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return
      
      const userMessage = this.userInput.trim()
      this.userInput = ''
      
      // Add user message to chat
      this.addMessage(userMessage, 'user')
      
      this.isLoading = true

      const body = {
          body: {
            message: {
              text: userMessage
            },
            session: this.currentSession || {
              id: this.sessionId,
              flow: 'general',
              new: true, // true if this is the first message
              data: {}
            },
            user: {
              id: this.userId,
              data: {}
            }
          }
      }

      console.log('Sending message:', JSON.stringify(body, null, 2))
      
      try {
        const response = await axios.post('http://localhost:8080/chat', body)

        // Save the updated session from the response
        if (response.data.session) {
          this.currentSession = response.data.session
          console.log('Session updated:', JSON.stringify(this.currentSession.data, null, 2))
        }
        
        // Add bot response to chat
        this.addMessage(response.data.response, 'bot')
        
      } catch (error) {
        console.error('Error sending message:', error)
        this.addMessage('Sorry, I encountered an error. Please try again.', 'bot')
      } finally {
        this.isLoading = false
      }
    },
    
    addMessage(text, type) {
      this.messages.push({
        text,
        type,
        timestamp: new Date()
      })
      
      // Scroll to bottom after message is added
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    formatTime(timestamp) {
      return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    
    generateSessionId() {
      return 'session-' + Math.random().toString(36).substr(2, 9)
    },
    
    generateUserId() {
      return 'user-' + Math.random().toString(36).substr(2, 9)
    },

    // Session management methods
    getSessionData() {
      return this.currentSession ? this.currentSession.data : {}
    },

    getCurrentFlow() {
      return this.currentFlow || 'general'
    },

    resetSession() {
      this.currentSession = null
      this.currentFlow = null
      this.sessionId = this.generateSessionId()
      this.messages = []
      this.addMessage('I\'m Povo, your AI assistant. How can I help you today?', 'bot')
    }
  },
  
  mounted() {
    // Add welcome message
    this.addMessage('I\'m Povo, your AI assistant. How can I help you today?', 'bot')
  }
}
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.chat-container {
  width: 90%;
  max-width: 600px;
  height: 80vh;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.session-info {
  margin-top: 8px;
  opacity: 0.8;
  font-size: 12px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.bot .message-content {
  background: #f1f3f4;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message-text {
  margin-bottom: 4px;
  line-height: 1.4;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input input:focus {
  border-color: #667eea;
}

.chat-input input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.chat-input button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.chat-input button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Scrollbar styling */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 
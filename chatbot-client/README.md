# Povo Chatbot Client

A simple Vue 3 chatbot client that connects to your Povo chatbot API.

## Features

- Modern Vue 3 composition API
- Real-time chat interface
- Beautiful gradient design
- Responsive layout
- Session management
- Error handling

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   # or
   npm start
   ```

3. **Open your browser** and navigate to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm start` - Alias for dev command
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run serve` - Alias for preview command
- `npm run lint` - Run ESLint to check code quality

## API Configuration

The client is configured to connect to your chatbot API at `http://localhost:8000`. Make sure your FastAPI server is running on that port.

To change the API endpoint, modify the URL in `src/App.vue`:

```javascript
const response = await axios.post('http://localhost:8000/chat', {
  // ... request body
})
```

## Request Format

The client sends requests in the format expected by your API:

```json
{
  "body": {
    "message": {
      "text": "User message"
    },
    "session": {
      "id": "session-abc",
      "new": true,
      "data": {}
    },
    "user": {
      "id": "user-123",
      "data": {}
    }
  }
}
```

## Development

- **Hot Reload**: Changes to your code will automatically refresh the browser
- **Port**: The app runs on port 3000 by default
- **Host**: Configured to accept connections from any host (useful for mobile testing)

## Build for Production

```bash
npm run build
```

This will create a `dist` folder with the production-ready files.

## Technologies Used

- Vue 3
- Vite
- Axios
- ESLint
- CSS3 with gradients and animations 
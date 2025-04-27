require("dotenv").config();
const axios = require("axios");
const { v4: uuidv4 } = require("uuid");

// Predefined responses for common queries
const predefinedResponses = {
  "what are your services":
    "We offer web development, AI integration, and UI/UX design! Want details on any of these?",
  "hi|hello|hey": "Hey there! How can I assist you today?",
  "contact|reach out":
    "You can reach us at contact@mywebsite.com or call us at (123) 456-7890.",
  "hours|open":
    "We’re available Monday to Friday, 9 AM to 5 PM. Drop us a message anytime!",
  "can tell me in details":
    "Sure! Web development includes custom websites and maintenance. AI integration offers chatbots and predictive models. UI/UX design focuses on user-friendly interfaces. Let me know which you’d like to explore further!",
  "make|create|build llm|language model|chatgpt|deepseek|grok":
    "That’s a highly specialized request! I’ll need to check with the owner to see if we can take on this project. Please contact us directly at contact@mywebsite.com for further discussion.", // New response
};

// In-memory conversation history (reset per request)
let conversationHistory = [];

async function getBotResponse(userMessage) {
  const normalizedMessage = userMessage.toLowerCase().trim();

  // Check for predefined responses
  for (const [key, response] of Object.entries(predefinedResponses)) {
    if (normalizedMessage.match(new RegExp(`\\b${key}\\b`))) {
      // Use word boundary for better matching
      conversationHistory = [{ user: userMessage, bot: response }];
      return response;
    }
  }

  // Generate a unique session ID for each request
  const sessionId = uuidv4();
  const messages = [
    {
      role: "system",
      content: `You are a friendly chatbot for a web development company. Provide concise, professional responses. Avoid technical advice on building any project how it can be done and is it possible to make it or not and try to gather info from the user first about his project and based on that tell them is it possible to make the project or not. Session ID: ${sessionId}`,
    },
    { role: "user", content: userMessage },
  ];

  try {
    const response = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.3-70b-versatile",
        messages: messages,
        max_tokens: 200,
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.GROQ_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    const botReply =
      response.data.choices[0].message.content ||
      "Sorry, I didn’t get that. Can you rephrase?";
    conversationHistory = [{ user: userMessage, bot: botReply }];
    return botReply;
  } catch (error) {
    console.error("Groq API Error:", error.message);
    const fallbackReply =
      "Oops, something went wrong! Try asking again or contact support.";
    conversationHistory = [{ user: userMessage, bot: fallbackReply }];
    return fallbackReply;
  }
}

module.exports = { getBotResponse };

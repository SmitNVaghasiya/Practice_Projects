const express = require("express");
const { getBotResponse } = require("./chatbot");
const cors = require("cors"); // Added CORS
const app = express();
const port = 3000;

app.use(express.json());
app.use(cors()); // Enable CORS for all origins
app.use(express.static("../public")); // Serve frontend files

// Endpoint to handle chatbot queries
app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  if (!userMessage) {
    return res.status(400).json({ reply: "Please send a message." });
  }

  try {
    const botReply = await getBotResponse(userMessage);
    res.json({ reply: botReply });
  } catch (error) {
    console.error("Server error:", error);
    res.status(500).json({ reply: "Something went wrong on the server!" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

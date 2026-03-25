using System;

namespace OutlookClaudeAddin.UI
{
    /// <summary>
    /// Represents a single message in the chat.
    /// </summary>
    public class ChatMessage
    {
        public string Role { get; set; }      // "user", "assistant", "system"
        public string Content { get; set; }
        public DateTime Timestamp { get; set; }

        public ChatMessage() { }

        public ChatMessage(string role, string content)
        {
            Role = role;
            Content = content;
            Timestamp = DateTime.Now;
        }

        public bool IsUser => Role == "user";
        public bool IsAssistant => Role == "assistant";
        public bool IsSystem => Role == "system";
    }
}

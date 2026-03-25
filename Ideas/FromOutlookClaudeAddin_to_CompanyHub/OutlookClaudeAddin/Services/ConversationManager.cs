using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace OutlookClaudeAddin.Services
{
    /// <summary>
    /// Manages conversation history for multi-turn Claude interactions.
    /// Can be extended for persistence, multiple conversations, etc.
    /// Currently the history is managed directly in ClaudeService.
    /// This class is reserved for future expansion (e.g., saving/loading chats).
    /// </summary>
    public class ConversationManager
    {
        private readonly List<JObject> _history = new List<JObject>();

        public IReadOnlyList<JObject> History => _history.AsReadOnly();

        public void AddUserMessage(string content)
        {
            _history.Add(new JObject
            {
                ["role"] = "user",
                ["content"] = content
            });
        }

        public void AddAssistantMessage(JArray content)
        {
            _history.Add(new JObject
            {
                ["role"] = "assistant",
                ["content"] = content
            });
        }

        public void AddToolResults(JArray toolResults)
        {
            _history.Add(new JObject
            {
                ["role"] = "user",
                ["content"] = toolResults
            });
        }

        public void Clear()
        {
            _history.Clear();
        }
    }
}

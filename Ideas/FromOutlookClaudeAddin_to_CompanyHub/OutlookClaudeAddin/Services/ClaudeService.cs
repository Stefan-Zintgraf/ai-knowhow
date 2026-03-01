using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Tools;

namespace OutlookClaudeAddin.Services
{
    /// <summary>
    /// Handles all communication with the Anthropic Claude API.
    /// Implements the tool_use loop: send message → receive tool_use → execute tool → send result → repeat.
    /// </summary>
    public class ClaudeService
    {
        private const string ApiUrl = "https://api.anthropic.com/v1/messages";
        private const string Model = "claude-sonnet-4-6";
        private const int MaxTokens = 4096;
        private const int MaxToolLoops = 10; // Safety limit

        private readonly string _apiKey;
        private readonly HttpClient _httpClient;
        private readonly List<JObject> _toolSchemas;
        private readonly List<JObject> _conversationHistory = new List<JObject>();

        private static readonly string SystemPrompt =
            "Du bist ein Outlook E-Mail-Assistent. Du hilfst dem Benutzer seine E-Mails zu verwalten.\n\n" +
            "WICHTIGE DATENSCHUTZ-EINSCHRÄNKUNG:\n" +
            "Du hast KEINEN Zugriff auf den Inhalt/Body von E-Mails. Du kannst NUR Metadaten sehen:\n" +
            "- Betreff, Absender, Empfänger, CC, Datum, Status, Anhänge\n" +
            "Du kannst den E-Mail-Text NICHT lesen. Versuche NIEMALS den Body abzurufen.\n\n" +
            "Verfügbare Aktionen:\n" +
            "- E-Mails suchen (nach Absender, Betreff, Empfänger - NICHT nach Inhalt)\n" +
            "- E-Mail-Metadaten anzeigen (Betreff, Absender, Empfänger, Datum, Anhänge)\n" +
            "- E-Mails beantworten, verfassen, verschieben, löschen\n" +
            "- Ordner anzeigen, erstellen, verschieben, löschen\n\n" +
            "Typischer Workflow:\n" +
            "1. Erst suchen/laden (list_recent_emails oder search_by_subject/sender/recipient)\n" +
            "2. Dann Metadaten anzeigen (view_email_cache)\n" +
            "3. Dann Aktion ausführen (move_email, reply_to_email, etc.)\n\n" +
            "Wenn du E-Mails nach Absender-Domain filterst (z.B. '@acontis.com'), " +
            "prüfe immer die E-Mail-Adresse in spitzen Klammern (<...>), nicht nur den Anzeigenamen. " +
            "Der Anzeigename kann unvollständig oder irreführend sein.\n\n" +
            "Antworte immer auf Deutsch. Sei präzise und hilfreich.";

        public ClaudeService(string apiKey)
        {
            _apiKey = apiKey;

            // Force TLS 1.2 (.NET 4.7.2 may default to older protocols)
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12;

            _httpClient = new HttpClient();
            _httpClient.Timeout = TimeSpan.FromSeconds(120);
            _httpClient.DefaultRequestHeaders.Add("x-api-key", apiKey);
            _httpClient.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");
            _toolSchemas = ToolDefinitions.GetAllToolSchemas();
        }

        /// <summary>
        /// Send a user message and handle the full tool_use loop.
        /// Returns the final text response from Claude.
        /// </summary>
        public async Task<string> SendMessageAsync(string userMessage, OutlookToolExecutor toolExecutor)
        {
            // Add user message to history
            _conversationHistory.Add(new JObject
            {
                ["role"] = "user",
                ["content"] = userMessage
            });

            int loopCount = 0;

            while (loopCount < MaxToolLoops)
            {
                loopCount++;

                // Call Claude API
                var response = await CallClaudeApiAsync();

                // Parse response content
                var content = response["content"] as JArray;
                if (content == null || content.Count == 0)
                    return "Keine Antwort erhalten.";

                var stopReason = response.Value<string>("stop_reason");

                // Add assistant response to history
                _conversationHistory.Add(new JObject
                {
                    ["role"] = "assistant",
                    ["content"] = content
                });

                // If stop_reason is "end_turn" or no tool_use blocks, extract text and return
                if (stopReason != "tool_use")
                {
                    return ExtractTextFromContent(content);
                }

                // Handle tool_use blocks
                var toolResults = new JArray();

                foreach (var block in content)
                {
                    if (block.Value<string>("type") == "tool_use")
                    {
                        string toolName = block.Value<string>("name");
                        string toolUseId = block.Value<string>("id");
                        var toolInput = block["input"] as JObject ?? new JObject();

                        // Execute the tool
                        string result;
                        try
                        {
                            result = await toolExecutor.ExecuteToolAsync(toolName, toolInput);
                        }
                        catch (Exception ex)
                        {
                            result = JsonConvert.SerializeObject(new { error = ex.Message });
                        }

                        toolResults.Add(new JObject
                        {
                            ["type"] = "tool_result",
                            ["tool_use_id"] = toolUseId,
                            ["content"] = result
                        });
                    }
                }

                // Add tool results as user message (Claude API convention)
                if (toolResults.Count > 0)
                {
                    _conversationHistory.Add(new JObject
                    {
                        ["role"] = "user",
                        ["content"] = toolResults
                    });
                }
            }

            return "Maximale Anzahl an Tool-Aufrufen erreicht. Bitte versuche es erneut.";
        }

        /// <summary>
        /// Clear conversation history for new chat.
        /// </summary>
        public void ClearHistory()
        {
            _conversationHistory.Clear();
        }

        private async Task<JObject> CallClaudeApiAsync()
        {
            var requestBody = new JObject
            {
                ["model"] = Model,
                ["max_tokens"] = MaxTokens,
                ["system"] = SystemPrompt,
                ["messages"] = new JArray(_conversationHistory.ToArray()),
                ["tools"] = new JArray(_toolSchemas.ToArray())
            };

            var httpContent = new StringContent(
                requestBody.ToString(Formatting.None),
                Encoding.UTF8,
                "application/json");

            HttpResponseMessage httpResponse;
            try
            {
                httpResponse = await _httpClient.PostAsync(ApiUrl, httpContent);
            }
            catch (Exception ex)
            {
                throw new Exception($"HTTP-Verbindungsfehler: {ex.GetType().Name}: {ex.Message}");
            }

            var responseText = await httpResponse.Content.ReadAsStringAsync();

            if (!httpResponse.IsSuccessStatusCode)
            {
                throw new Exception($"Claude API Fehler ({(int)httpResponse.StatusCode} {httpResponse.StatusCode}): {responseText}");
            }

            return JObject.Parse(responseText);
        }

        private string ExtractTextFromContent(JArray content)
        {
            var textParts = new List<string>();

            foreach (var block in content)
            {
                if (block.Value<string>("type") == "text")
                {
                    textParts.Add(block.Value<string>("text"));
                }
            }

            return textParts.Count > 0
                ? string.Join("\n", textParts)
                : "Keine Textantwort erhalten.";
        }
    }
}

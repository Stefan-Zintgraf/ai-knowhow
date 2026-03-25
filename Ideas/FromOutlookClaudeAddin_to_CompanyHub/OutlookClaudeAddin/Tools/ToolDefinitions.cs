using Newtonsoft.Json.Linq;
using System.Collections.Generic;

namespace OutlookClaudeAddin.Tools
{
    /// <summary>
    /// Defines all 19 tool schemas for Claude API tool_use.
    /// These mirror the Python MCP server tools exactly.
    /// </summary>
    public static class ToolDefinitions
    {
        public static List<JObject> GetAllToolSchemas()
        {
            return new List<JObject>
            {
                // ===== SEARCH TOOLS (5) =====
                MakeTool("list_recent_emails",
                    "Load emails into cache and return count. Use view_email_cache to view them afterwards.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["days"] = Prop("integer", "Days to look back (1-36500, default: 7)"),
                            ["folder_name"] = Prop("string", "Folder to search (default: Inbox). Use full path like 'user@company.com/Inbox' or just 'Inbox'.")
                        }
                    }),

                MakeTool("search_email_by_subject",
                    "Search email subjects and load matching emails into cache. Only searches the subject field.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["search_term"] = Prop("string", "Plain text search term for subject"),
                            ["days"] = Prop("integer", "Days to look back (1-36500, default: 7)"),
                            ["folder_name"] = Prop("string", "Optional folder name to search (default: Inbox)"),
                            ["match_all"] = Prop("boolean", "If true, ALL terms must match (AND). If false, ANY term matches (OR). Default: true.")
                        },
                        ["required"] = new JArray("search_term")
                    }),

                MakeTool("search_email_by_sender_name",
                    "Search emails by sender name and load into cache. Search by name only, not email address.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["search_term"] = Prop("string", "Search term for sender name"),
                            ["days"] = Prop("integer", "Days to look back (default: 7)"),
                            ["folder_name"] = Prop("string", "Optional folder name"),
                            ["match_all"] = Prop("boolean", "AND logic if true (default), OR if false")
                        },
                        ["required"] = new JArray("search_term")
                    }),

                MakeTool("search_email_by_recipient_name",
                    "Search emails by recipient (To) name and load into cache. Search by name only.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["search_term"] = Prop("string", "Search term for recipient name"),
                            ["days"] = Prop("integer", "Days to look back (default: 7)"),
                            ["folder_name"] = Prop("string", "Optional folder name"),
                            ["match_all"] = Prop("boolean", "AND logic if true (default), OR if false")
                        },
                        ["required"] = new JArray("search_term")
                    }),

                // search_email_by_body REMOVED - privacy: no body access

                // ===== VIEWING TOOLS (4) =====
                MakeTool("view_email_cache",
                    "View cached emails (5 per page). Shows Subject, From, To, CC, Received, Status, Attachments.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["page"] = Prop("integer", "Page number (1-based, default: 1)")
                        }
                    }),

                MakeTool("get_email_by_number",
                    "Get email metadata by cache number. Returns subject, sender, recipients, date, status, and attachment info. Does NOT return email body content (privacy restriction).",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["email_number"] = Prop("integer", "Position in cache (1-based)")
                        },
                        ["required"] = new JArray("email_number")
                    }),

                MakeTool("load_emails_by_folder",
                    "Load emails from a specific folder into cache. Use EITHER 'days' OR 'max_emails', not both.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["folder_path"] = Prop("string", "Path to folder (e.g., 'user@company.com/Inbox/SubFolder')"),
                            ["days"] = Prop("integer", "Days to look back (mutually exclusive with max_emails)"),
                            ["max_emails"] = Prop("integer", "Max emails to load (mutually exclusive with days)")
                        },
                        ["required"] = new JArray("folder_path")
                    }),

                MakeTool("clear_email_cache",
                    "Clear the email cache. Use when you want to start fresh.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject()
                    }),

                // ===== EMAIL OPERATIONS (4) =====
                MakeTool("reply_to_email",
                    "Reply to an email by cache number. When to/cc are null, uses ReplyAll. When specified, uses Reply with custom recipients.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["email_number"] = Prop("integer", "Email position in cache (1-based)"),
                            ["reply_text"] = Prop("string", "Reply text to prepend"),
                            ["to_recipients"] = Prop("string", "Optional custom To recipients (comma-separated emails)"),
                            ["cc_recipients"] = Prop("string", "Optional custom CC recipients (comma-separated emails)")
                        },
                        ["required"] = new JArray("email_number", "reply_text")
                    }),

                MakeTool("compose_email",
                    "Compose and send a new email.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["recipient_email"] = Prop("string", "Recipient email(s), semicolon-separated for multiple"),
                            ["subject"] = Prop("string", "Subject line"),
                            ["body"] = Prop("string", "Email body text"),
                            ["cc_email"] = Prop("string", "Optional CC email(s), semicolon-separated")
                        },
                        ["required"] = new JArray("recipient_email", "subject", "body")
                    }),

                MakeTool("move_email",
                    "Move an email to a target folder.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["email_number"] = Prop("integer", "Email position in cache (1-based)"),
                            ["target_folder_name"] = Prop("string", "Target folder path (e.g., 'user@company.com/Inbox/SubFolder')")
                        },
                        ["required"] = new JArray("email_number", "target_folder_name")
                    }),

                MakeTool("delete_email",
                    "Move an email to Deleted Items.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["email_number"] = Prop("integer", "Email position in cache (1-based)")
                        },
                        ["required"] = new JArray("email_number")
                    }),

                // ===== FOLDER TOOLS (5) =====
                MakeTool("get_folder_list",
                    "List all Outlook mail folders in a hierarchical structure.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject()
                    }),

                MakeTool("list_subfolders",
                    "List direct subfolder names of a folder.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["folder_path"] = Prop("string", "Full path (e.g., 'user@company.com/Inbox')")
                        },
                        ["required"] = new JArray("folder_path")
                    }),

                MakeTool("create_folder",
                    "Create a new folder.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["folder_name"] = Prop("string", "Name of the folder to create"),
                            ["parent_folder_name"] = Prop("string", "Parent folder path (default: Inbox)")
                        },
                        ["required"] = new JArray("folder_name")
                    }),

                MakeTool("remove_folder",
                    "Remove an existing folder. Include email address as root, e.g., 'user@company.com/Inbox/SubFolder'.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["folder_name"] = Prop("string", "Full path of folder to remove")
                        },
                        ["required"] = new JArray("folder_name")
                    }),

                MakeTool("move_folder",
                    "Move a folder and all its emails to a new location.",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["source_folder_path"] = Prop("string", "Path of source folder"),
                            ["target_parent_path"] = Prop("string", "Path of target parent folder")
                        },
                        ["required"] = new JArray("source_folder_path", "target_parent_path")
                    }),

                // ===== BATCH (1) =====
                MakeTool("batch_forward_email",
                    "Forward an email to recipients from a CSV file (max 500 per batch via BCC).",
                    new JObject
                    {
                        ["type"] = "object",
                        ["properties"] = new JObject
                        {
                            ["email_number"] = Prop("integer", "Email position in cache (1-based)"),
                            ["csv_path"] = Prop("string", "Path to CSV file with 'email' column"),
                            ["custom_text"] = Prop("string", "Optional text to prepend to email body")
                        },
                        ["required"] = new JArray("email_number", "csv_path")
                    }),
            };
        }

        private static JObject MakeTool(string name, string description, JObject inputSchema)
        {
            return new JObject
            {
                ["name"] = name,
                ["description"] = description,
                ["input_schema"] = inputSchema
            };
        }

        private static JObject Prop(string type, string description)
        {
            return new JObject
            {
                ["type"] = type,
                ["description"] = description
            };
        }
    }
}

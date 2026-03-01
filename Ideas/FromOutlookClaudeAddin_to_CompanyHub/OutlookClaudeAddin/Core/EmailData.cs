using System;
using System.Collections.Generic;

namespace OutlookClaudeAddin.Core
{
    /// <summary>
    /// Represents extracted email data - mirrors the Python MCP server's email cache structure.
    /// </summary>
    public class EmailData
    {
        public string EntryId { get; set; }
        public string Subject { get; set; }
        public string SenderName { get; set; }
        public string SenderEmail { get; set; }
        public string To { get; set; }
        public string Cc { get; set; }
        public DateTime ReceivedTime { get; set; }
        public bool IsRead { get; set; }
        public string Body { get; set; }
        public string HtmlBody { get; set; }
        public int AttachmentCount { get; set; }
        public int EmbeddedImageCount { get; set; }
        public List<AttachmentInfo> Attachments { get; set; } = new List<AttachmentInfo>();
        public string FolderPath { get; set; }
        public string ConversationId { get; set; }

        /// <summary>
        /// Creates a minimal summary for cache listing (view_email_cache).
        /// </summary>
        public Dictionary<string, object> ToSummary(int number)
        {
            return new Dictionary<string, object>
            {
                ["number"] = number,
                ["subject"] = Subject ?? "(No Subject)",
                ["from"] = !string.IsNullOrEmpty(SenderName) && !string.IsNullOrEmpty(SenderEmail)
                    ? $"{SenderName} <{SenderEmail}>"
                    : SenderName ?? SenderEmail ?? "Unknown",
                ["to"] = To ?? "",
                ["cc"] = Cc ?? "",
                ["received"] = ReceivedTime.ToString("yyyy-MM-dd HH:mm:ss"),
                ["status"] = IsRead ? "Read" : "Unread",
                ["attachments_count"] = AttachmentCount,
                ["embedded_images_count"] = EmbeddedImageCount
            };
        }

        /// <summary>
        /// Creates a metadata-only text representation (no body content - privacy).
        /// </summary>
        public string ToMetadataOnly()
        {
            var text = $"Subject: {Subject}\n" +
                   $"From: {SenderName} <{SenderEmail}>\n" +
                   $"To: {To}\n" +
                   (string.IsNullOrEmpty(Cc) ? "" : $"CC: {Cc}\n") +
                   $"Received: {ReceivedTime:yyyy-MM-dd HH:mm:ss}\n" +
                   $"Status: {(IsRead ? "Read" : "Unread")}\n" +
                   $"Attachments: {AttachmentCount}";

            if (Attachments.Count > 0)
            {
                text += "\n--- Attachments ---\n";
                foreach (var att in Attachments)
                {
                    text += $"  - {att.FileName} ({FormatSize(att.Size)}){(att.IsEmbedded ? " [embedded]" : "")}\n";
                }
            }

            text += "\n[Body content hidden - privacy restriction]";
            return text;
        }

        /// <summary>
        /// Creates a basic text representation for get_email_by_number (basic mode).
        /// </summary>
        public string ToBasicText()
        {
            return ToMetadataOnly();
        }

        /// <summary>
        /// Creates an enhanced text representation with HTML and thread info.
        /// </summary>
        public string ToEnhancedText()
        {
            return ToMetadataOnly();
        }

        private static string FormatSize(long bytes)
        {
            if (bytes < 1024) return $"{bytes} B";
            if (bytes < 1024 * 1024) return $"{bytes / 1024.0:F1} KB";
            return $"{bytes / (1024.0 * 1024.0):F1} MB";
        }
    }

    public class AttachmentInfo
    {
        public string FileName { get; set; }
        public long Size { get; set; }
        public bool IsEmbedded { get; set; }
    }
}

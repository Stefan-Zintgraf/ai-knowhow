using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Tools.SearchTools
{
    /// <summary>
    /// Base class for all search tools. Provides common search workflow.
    /// </summary>
    public abstract class SearchToolBase : IOutlookTool
    {
        protected readonly Outlook.Application OutlookApp;
        protected readonly EmailCache Cache;
        protected readonly FolderNavigator FolderNav;

        public abstract string Name { get; }

        protected SearchToolBase(Outlook.Application outlookApp, EmailCache cache, FolderNavigator folderNav)
        {
            OutlookApp = outlookApp;
            Cache = cache;
            FolderNav = folderNav;
        }

        public Task<object> ExecuteAsync(JObject parameters)
        {
            return Task.FromResult(Execute(parameters));
        }

        protected abstract object Execute(JObject parameters);

        /// <summary>
        /// Common workflow: clear cache, search folder, load results, return count.
        /// </summary>
        protected object ExecuteSearch(string folderName, int days, Func<Outlook.MailItem, bool> matchFunc, string operationName)
        {
            Cache.Clear();

            var folder = FolderNav.GetFolder(folderName ?? "Inbox");
            var cutoff = DateTime.Now.AddDays(-days);
            int found = 0;

            var items = folder.Items;
            items.Sort("[ReceivedTime]", true); // newest first

            foreach (object rawItem in items)
            {
                var mail = rawItem as Outlook.MailItem;
                if (mail == null) continue;

                try
                {
                    if (mail.ReceivedTime < cutoff) break;

                    if (matchFunc(mail))
                    {
                        Cache.Add(ExtractEmailData(mail));
                        found++;
                    }
                }
                catch
                {
                    // Skip problematic items
                }
            }

            return new
            {
                type = "text",
                text = $"Found {found} emails from last {days} days. Use 'view_email_cache' to view them."
            };
        }

        /// <summary>
        /// Check if search terms match a text field.
        /// </summary>
        protected bool MatchesSearch(string text, string searchTerm, bool matchAll)
        {
            if (string.IsNullOrEmpty(text) || string.IsNullOrEmpty(searchTerm))
                return false;

            var terms = searchTerm.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var textLower = text.ToLowerInvariant();

            if (matchAll)
                return terms.All(t => textLower.Contains(t.ToLowerInvariant()));
            else
                return terms.Any(t => textLower.Contains(t.ToLowerInvariant()));
        }

        /// <summary>
        /// Extract email data from a MailItem into our cache model.
        /// </summary>
        protected EmailData ExtractEmailData(Outlook.MailItem mail)
        {
            var data = new EmailData
            {
                EntryId = mail.EntryID,
                Subject = SafeGet(() => mail.Subject, "(No Subject)"),
                SenderName = SafeGet(() => mail.SenderName, ""),
                SenderEmail = SafeGet(() => mail.SenderEmailAddress, ""),
                ReceivedTime = SafeGet(() => mail.ReceivedTime, DateTime.MinValue),
                IsRead = SafeGet(() => !mail.UnRead, false),
                // Body intentionally NOT loaded - privacy restriction
                To = SafeGet(() => mail.To, ""),
                Cc = SafeGet(() => mail.CC, ""),
            };

            try
            {
                data.AttachmentCount = mail.Attachments.Count;
                int embeddedCount = 0;
                foreach (Outlook.Attachment att in mail.Attachments)
                {
                    bool isEmbedded = IsEmbeddedImage(att);
                    data.Attachments.Add(new AttachmentInfo
                    {
                        FileName = SafeGet(() => att.FileName, "unknown"),
                        Size = SafeGet(() => (long)att.Size, 0L),
                        IsEmbedded = isEmbedded
                    });
                    if (isEmbedded) embeddedCount++;
                }
                data.EmbeddedImageCount = embeddedCount;
            }
            catch { }

            return data;
        }

        /// <summary>
        /// Detect if an attachment is an embedded image (inline, not a real attachment).
        /// Uses multiple heuristics like the Python MCP server.
        /// </summary>
        private bool IsEmbeddedImage(Outlook.Attachment att)
        {
            try
            {
                string fileName = SafeGet(() => att.FileName, "");

                // Check Content-ID property (PR_ATTACH_CONTENT_ID)
                try
                {
                    string contentId = att.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F") as string;
                    if (!string.IsNullOrEmpty(contentId)) return true;
                }
                catch { }

                // Check if it's an image type by extension
                var imageExtensions = new[] { ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico" };
                if (imageExtensions.Any(ext => fileName.EndsWith(ext, StringComparison.OrdinalIgnoreCase)))
                {
                    // Small images are likely inline
                    long size = SafeGet(() => (long)att.Size, 0L);
                    if (size < 50000) return true; // < 50KB likely inline

                    // Check naming patterns (e.g., "image001.png")
                    if (fileName.StartsWith("image", StringComparison.OrdinalIgnoreCase))
                        return true;
                }

                return false;
            }
            catch
            {
                return false;
            }
        }

        protected T SafeGet<T>(Func<T> getter, T defaultValue)
        {
            try { return getter(); }
            catch { return defaultValue; }
        }
    }

    // ===== Tool 1: list_recent_emails =====
    public class ListRecentEmailsTool : SearchToolBase
    {
        public override string Name => "list_recent_emails";

        public ListRecentEmailsTool(Outlook.Application app, EmailCache cache, FolderNavigator nav) : base(app, cache, nav) { }

        protected override object Execute(JObject p)
        {
            int days = p.Value<int?>("days") ?? 7;
            string folderName = p.Value<string>("folder_name");

            return ExecuteSearch(folderName, days, mail => true, "list_recent_emails");
        }
    }

    // ===== Tool 2: search_email_by_subject =====
    public class SearchBySubjectTool : SearchToolBase
    {
        public override string Name => "search_email_by_subject";

        public SearchBySubjectTool(Outlook.Application app, EmailCache cache, FolderNavigator nav) : base(app, cache, nav) { }

        protected override object Execute(JObject p)
        {
            string searchTerm = p.Value<string>("search_term");
            int days = p.Value<int?>("days") ?? 7;
            string folderName = p.Value<string>("folder_name");
            bool matchAll = p.Value<bool?>("match_all") ?? true;

            if (string.IsNullOrWhiteSpace(searchTerm))
                return new { type = "text", text = "Error: search_term is required." };

            return ExecuteSearch(folderName, days,
                mail => MatchesSearch(SafeGet(() => mail.Subject, ""), searchTerm, matchAll),
                "search_email_by_subject");
        }
    }

    // ===== Tool 3: search_email_by_sender_name =====
    public class SearchBySenderTool : SearchToolBase
    {
        public override string Name => "search_email_by_sender_name";

        public SearchBySenderTool(Outlook.Application app, EmailCache cache, FolderNavigator nav) : base(app, cache, nav) { }

        protected override object Execute(JObject p)
        {
            string searchTerm = p.Value<string>("search_term");
            int days = p.Value<int?>("days") ?? 7;
            string folderName = p.Value<string>("folder_name");
            bool matchAll = p.Value<bool?>("match_all") ?? true;

            if (string.IsNullOrWhiteSpace(searchTerm))
                return new { type = "text", text = "Error: search_term is required." };

            return ExecuteSearch(folderName, days,
                mail => MatchesSearch(SafeGet(() => mail.SenderName, ""), searchTerm, matchAll),
                "search_email_by_sender_name");
        }
    }

    // ===== Tool 4: search_email_by_recipient_name =====
    public class SearchByRecipientTool : SearchToolBase
    {
        public override string Name => "search_email_by_recipient_name";

        public SearchByRecipientTool(Outlook.Application app, EmailCache cache, FolderNavigator nav) : base(app, cache, nav) { }

        protected override object Execute(JObject p)
        {
            string searchTerm = p.Value<string>("search_term");
            int days = p.Value<int?>("days") ?? 7;
            string folderName = p.Value<string>("folder_name");
            bool matchAll = p.Value<bool?>("match_all") ?? true;

            if (string.IsNullOrWhiteSpace(searchTerm))
                return new { type = "text", text = "Error: search_term is required." };

            return ExecuteSearch(folderName, days,
                mail => MatchesSearch(SafeGet(() => mail.To, ""), searchTerm, matchAll),
                "search_email_by_recipient_name");
        }
    }

    // ===== Tool 5: search_email_by_body =====
    public class SearchByBodyTool : SearchToolBase
    {
        public override string Name => "search_email_by_body";

        public SearchByBodyTool(Outlook.Application app, EmailCache cache, FolderNavigator nav) : base(app, cache, nav) { }

        protected override object Execute(JObject p)
        {
            string searchTerm = p.Value<string>("search_term");
            int days = p.Value<int?>("days") ?? 7;
            string folderName = p.Value<string>("folder_name");
            bool matchAll = p.Value<bool?>("match_all") ?? true;

            if (string.IsNullOrWhiteSpace(searchTerm))
                return new { type = "text", text = "Error: search_term is required." };

            return ExecuteSearch(folderName, days,
                mail => MatchesSearch(SafeGet(() => mail.Body, ""), searchTerm, matchAll),
                "search_email_by_body");
        }
    }
}

using System;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Tools.ViewingTools
{
    // ===== Tool 6: view_email_cache =====
    public class ViewEmailCacheTool : IOutlookTool
    {
        private readonly EmailCache _cache;
        public string Name => "view_email_cache";

        public ViewEmailCacheTool(EmailCache cache) { _cache = cache; }

        public Task<object> ExecuteAsync(JObject p)
        {
            int page = p.Value<int?>("page") ?? 1;

            if (_cache.Count == 0)
            {
                return Task.FromResult<object>(new
                {
                    type = "text",
                    text = "No emails in cache. Use a search tool or list_recent_emails first."
                });
            }

            var (emails, totalPages, totalEmails) = _cache.GetPage(page);

            return Task.FromResult<object>(new
            {
                type = "json",
                data = new
                {
                    page,
                    total_pages = totalPages,
                    total_emails = totalEmails,
                    emails
                }
            });
        }
    }

    // ===== Tool 7: get_email_by_number =====
    public class GetEmailByNumberTool : IOutlookTool
    {
        private readonly EmailCache _cache;
        public string Name => "get_email_by_number";

        public GetEmailByNumberTool(EmailCache cache) { _cache = cache; }

        public Task<object> ExecuteAsync(JObject p)
        {
            int emailNumber = p.Value<int>("email_number");

            if (_cache.Count == 0)
            {
                return Task.FromResult<object>(new
                {
                    type = "text",
                    text = "No emails loaded. Use a search tool first."
                });
            }

            var email = _cache.GetByNumber(emailNumber);
            if (email == null)
            {
                return Task.FromResult<object>(new
                {
                    type = "text",
                    text = $"Invalid email number: {emailNumber}. Cache has {_cache.Count} emails."
                });
            }

            // Privacy: only return metadata, no body content
            string content = email.ToMetadataOnly();

            return Task.FromResult<object>(new { type = "text", text = content });
        }
    }

    // ===== Tool 8: load_emails_by_folder =====
    public class LoadEmailsByFolderTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly EmailCache _cache;
        private readonly FolderNavigator _folderNav;
        public string Name => "load_emails_by_folder";

        public LoadEmailsByFolderTool(Outlook.Application app, EmailCache cache, FolderNavigator nav)
        {
            _outlookApp = app;
            _cache = cache;
            _folderNav = nav;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            string folderPath = p.Value<string>("folder_path");
            int? days = p.Value<int?>("days");
            int? maxEmails = p.Value<int?>("max_emails");

            if (string.IsNullOrWhiteSpace(folderPath))
            {
                return Task.FromResult<object>(new
                {
                    type = "text",
                    text = "Error: folder_path is required."
                });
            }

            if (days.HasValue && maxEmails.HasValue)
            {
                return Task.FromResult<object>(new
                {
                    type = "text",
                    text = "Error: Use either 'days' or 'max_emails', not both."
                });
            }

            _cache.Clear();

            var folder = _folderNav.GetFolder(folderPath);
            var items = folder.Items;
            items.Sort("[ReceivedTime]", true);

            DateTime? cutoff = days.HasValue ? DateTime.Now.AddDays(-days.Value) : (DateTime?)null;
            int limit = maxEmails ?? 1000;
            int loaded = 0;

            // Enforce limits like Python MCP
            bool isInbox = folderPath.ToLowerInvariant().Contains("inbox");
            if (isInbox && limit > 30) limit = 30;
            if (!isInbox && limit > 1000) limit = 1000;

            foreach (object rawItem in items)
            {
                if (loaded >= limit) break;

                var mail = rawItem as Outlook.MailItem;
                if (mail == null) continue;

                try
                {
                    if (cutoff.HasValue && mail.ReceivedTime < cutoff.Value) break;

                    _cache.Add(ExtractMinimal(mail));
                    loaded++;
                }
                catch { }
            }

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Found {loaded} emails in '{folderPath}'. Use 'view_email_cache' to view them."
            });
        }

        private EmailData ExtractMinimal(Outlook.MailItem mail)
        {
            return new EmailData
            {
                EntryId = mail.EntryID,
                Subject = TryGet(() => mail.Subject, "(No Subject)"),
                SenderName = TryGet(() => mail.SenderName, ""),
                SenderEmail = TryGet(() => mail.SenderEmailAddress, ""),
                ReceivedTime = TryGet(() => mail.ReceivedTime, DateTime.MinValue),
                IsRead = TryGet(() => !mail.UnRead, false),
                To = TryGet(() => mail.To, ""),
                Cc = TryGet(() => mail.CC, ""),
                AttachmentCount = TryGet(() => mail.Attachments.Count, 0),
            };
        }

        private T TryGet<T>(Func<T> getter, T defaultValue)
        {
            try { return getter(); }
            catch { return defaultValue; }
        }
    }

    // ===== Tool 9: clear_email_cache =====
    public class ClearEmailCacheTool : IOutlookTool
    {
        private readonly EmailCache _cache;
        public string Name => "clear_email_cache";

        public ClearEmailCacheTool(EmailCache cache) { _cache = cache; }

        public Task<object> ExecuteAsync(JObject p)
        {
            _cache.Clear();
            return Task.FromResult<object>(new
            {
                type = "text",
                text = "Email cache cleared successfully."
            });
        }
    }
}

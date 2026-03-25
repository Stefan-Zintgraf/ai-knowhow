using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Tools.EmailOperationTools
{
    // ===== Tool 10: reply_to_email =====
    public class ReplyToEmailTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly EmailCache _cache;
        public string Name => "reply_to_email";

        public ReplyToEmailTool(Outlook.Application app, EmailCache cache)
        {
            _outlookApp = app;
            _cache = cache;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            int emailNumber = p.Value<int>("email_number");
            string replyText = p.Value<string>("reply_text");
            string toRecipients = p.Value<string>("to_recipients");
            string ccRecipients = p.Value<string>("cc_recipients");

            if (string.IsNullOrWhiteSpace(replyText))
                return Task.FromResult<object>(new { type = "text", text = "Error: reply_text is required." });

            var emailData = _cache.GetByNumber(emailNumber);
            if (emailData == null)
                return Task.FromResult<object>(new { type = "text", text = $"Invalid email number: {emailNumber}" });

            // Get the original mail item from Outlook
            var session = _outlookApp.Session;
            Outlook.MailItem original;
            try
            {
                original = session.GetItemFromID(emailData.EntryId) as Outlook.MailItem;
            }
            catch (Exception ex)
            {
                return Task.FromResult<object>(new { type = "text", text = $"Error finding email: {ex.Message}" });
            }

            if (original == null)
                return Task.FromResult<object>(new { type = "text", text = "Error: Could not retrieve original email." });

            Outlook.MailItem reply;

            if (toRecipients == null && ccRecipients == null)
            {
                // ReplyAll - preserves original recipients
                reply = original.ReplyAll();
            }
            else
            {
                // Reply with custom recipients
                reply = original.Reply();
                reply.To = "";
                reply.CC = "";

                if (!string.IsNullOrWhiteSpace(toRecipients))
                    reply.To = toRecipients;
                if (!string.IsNullOrWhiteSpace(ccRecipients))
                    reply.CC = ccRecipients;
            }

            // Prepend reply text
            reply.Body = replyText + "\n\n" + reply.Body;
            reply.Send();

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Reply sent successfully to: {reply.To}" +
                       (string.IsNullOrEmpty(reply.CC) ? "" : $" (CC: {reply.CC})")
            });
        }
    }

    // ===== Tool 11: compose_email =====
    public class ComposeEmailTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        public string Name => "compose_email";

        public ComposeEmailTool(Outlook.Application app) { _outlookApp = app; }

        public Task<object> ExecuteAsync(JObject p)
        {
            string recipientEmail = p.Value<string>("recipient_email");
            string subject = p.Value<string>("subject");
            string body = p.Value<string>("body");
            string ccEmail = p.Value<string>("cc_email");

            if (string.IsNullOrWhiteSpace(recipientEmail))
                return Task.FromResult<object>(new { type = "text", text = "Error: recipient_email is required." });
            if (string.IsNullOrWhiteSpace(subject))
                return Task.FromResult<object>(new { type = "text", text = "Error: subject is required." });

            var mail = _outlookApp.CreateItem(Outlook.OlItemType.olMailItem) as Outlook.MailItem;
            mail.To = recipientEmail;
            mail.Subject = subject;
            mail.Body = body ?? "";

            if (!string.IsNullOrWhiteSpace(ccEmail))
                mail.CC = ccEmail;

            mail.Send();

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Email sent successfully to: {recipientEmail}" +
                       (string.IsNullOrEmpty(ccEmail) ? "" : $" (CC: {ccEmail})")
            });
        }
    }

    // ===== Tool 12: move_email =====
    public class MoveEmailTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly EmailCache _cache;
        private readonly FolderNavigator _folderNav;
        public string Name => "move_email";

        public MoveEmailTool(Outlook.Application app, EmailCache cache, FolderNavigator nav)
        {
            _outlookApp = app;
            _cache = cache;
            _folderNav = nav;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            int emailNumber = p.Value<int>("email_number");
            string targetFolderName = p.Value<string>("target_folder_name");

            if (string.IsNullOrWhiteSpace(targetFolderName))
                return Task.FromResult<object>(new { type = "text", text = "Error: target_folder_name is required." });

            var emailData = _cache.GetByNumber(emailNumber);
            if (emailData == null)
                return Task.FromResult<object>(new { type = "text", text = $"Invalid email number: {emailNumber}" });

            var session = _outlookApp.Session;
            var mail = session.GetItemFromID(emailData.EntryId) as Outlook.MailItem;
            if (mail == null)
                return Task.FromResult<object>(new { type = "text", text = "Error: Could not retrieve email." });

            var targetFolder = _folderNav.GetFolder(targetFolderName);
            mail.Move(targetFolder);

            // Clear cache after move (positions changed)
            _cache.Clear();

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Email moved successfully to '{targetFolderName}'. Cache cleared - reload emails if needed."
            });
        }
    }

    // ===== Tool 13: delete_email =====
    public class DeleteEmailTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly EmailCache _cache;
        public string Name => "delete_email";

        public DeleteEmailTool(Outlook.Application app, EmailCache cache)
        {
            _outlookApp = app;
            _cache = cache;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            int emailNumber = p.Value<int>("email_number");

            var emailData = _cache.GetByNumber(emailNumber);
            if (emailData == null)
                return Task.FromResult<object>(new { type = "text", text = $"Invalid email number: {emailNumber}" });

            var session = _outlookApp.Session;
            var mail = session.GetItemFromID(emailData.EntryId) as Outlook.MailItem;
            if (mail == null)
                return Task.FromResult<object>(new { type = "text", text = "Error: Could not retrieve email." });

            // Move to Deleted Items (not permanent delete)
            var deletedItems = session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderDeletedItems);
            mail.Move(deletedItems);

            _cache.Clear();

            return Task.FromResult<object>(new
            {
                type = "text",
                text = "Email moved to Deleted Items successfully. Cache cleared."
            });
        }
    }

    // ===== Tool 19: batch_forward_email =====
    public class BatchForwardEmailTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly EmailCache _cache;
        public string Name => "batch_forward_email";

        public BatchForwardEmailTool(Outlook.Application app, EmailCache cache)
        {
            _outlookApp = app;
            _cache = cache;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            int emailNumber = p.Value<int>("email_number");
            string csvPath = p.Value<string>("csv_path");
            string customText = p.Value<string>("custom_text") ?? "";

            var emailData = _cache.GetByNumber(emailNumber);
            if (emailData == null)
                return Task.FromResult<object>(new { type = "text", text = $"Invalid email number: {emailNumber}" });

            if (!File.Exists(csvPath))
                return Task.FromResult<object>(new { type = "text", text = $"CSV file not found: {csvPath}" });

            // Read CSV and extract email column
            var lines = File.ReadAllLines(csvPath);
            if (lines.Length < 2)
                return Task.FromResult<object>(new { type = "text", text = "CSV file is empty or has no data rows." });

            var headers = lines[0].Split(',').Select(h => h.Trim().ToLowerInvariant()).ToList();
            int emailCol = headers.IndexOf("email");
            if (emailCol < 0)
                return Task.FromResult<object>(new { type = "text", text = "CSV must have an 'email' column." });

            var recipients = new List<string>();
            for (int i = 1; i < lines.Length; i++)
            {
                var cols = lines[i].Split(',');
                if (cols.Length > emailCol)
                {
                    var addr = cols[emailCol].Trim().Trim('"');
                    if (addr.Contains("@"))
                        recipients.Add(addr);
                }
            }

            if (recipients.Count == 0)
                return Task.FromResult<object>(new { type = "text", text = "No valid email addresses found in CSV." });

            // Get original email
            var session = _outlookApp.Session;
            var original = session.GetItemFromID(emailData.EntryId) as Outlook.MailItem;
            if (original == null)
                return Task.FromResult<object>(new { type = "text", text = "Error: Could not retrieve email." });

            // Batch forward (max 500 per batch = Outlook BCC limit)
            const int batchSize = 500;
            int batchCount = 0;
            int totalSent = 0;

            for (int i = 0; i < recipients.Count; i += batchSize)
            {
                batchCount++;
                var batch = recipients.Skip(i).Take(batchSize);

                var forward = original.Forward();
                forward.BCC = string.Join(";", batch);
                forward.To = "";

                if (!string.IsNullOrWhiteSpace(customText))
                    forward.Body = customText + "\n\n" + forward.Body;

                forward.Send();
                totalSent += batch.Count();
            }

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Batch sending completed for {totalSent} recipients in {batchCount} batch(es)."
            });
        }
    }
}

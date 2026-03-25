using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Core
{
    /// <summary>
    /// Navigates Outlook folder hierarchy.
    /// Handles paths like "user@company.com/Inbox/SubFolder" or just "Inbox".
    /// </summary>
    public class FolderNavigator
    {
        private readonly Outlook.Application _outlookApp;

        public FolderNavigator(Outlook.Application outlookApp)
        {
            _outlookApp = outlookApp;
        }

        /// <summary>
        /// Get folder by path. Supports:
        /// - "Inbox" (default store)
        /// - "user@company.com/Inbox/SubFolder" (specific store)
        /// </summary>
        public Outlook.MAPIFolder GetFolder(string folderPath)
        {
            if (string.IsNullOrWhiteSpace(folderPath))
                folderPath = "Inbox";

            var session = _outlookApp.Session;
            var parts = folderPath.Split(new[] { '/' }, StringSplitOptions.RemoveEmptyEntries);

            // Try to find the store by first part (email address or store name)
            Outlook.MAPIFolder root = null;
            int startIndex = 0;

            foreach (Outlook.Store store in session.Stores)
            {
                if (string.Equals(store.DisplayName, parts[0], StringComparison.OrdinalIgnoreCase))
                {
                    root = store.GetRootFolder() as Outlook.MAPIFolder;
                    startIndex = 1;
                    break;
                }
            }

            // If no store matched, try as a default folder name
            if (root == null)
            {
                // Try default folder lookup for common names
                var defaultFolder = TryGetDefaultFolder(parts[0]);
                if (defaultFolder != null)
                {
                    if (parts.Length == 1) return defaultFolder;
                    root = defaultFolder;
                    startIndex = 1;
                }
                else
                {
                    // Use default store
                    root = session.DefaultStore.GetRootFolder() as Outlook.MAPIFolder;
                    startIndex = 0;
                }
            }

            // Navigate remaining path parts
            var current = root;
            for (int i = startIndex; i < parts.Length; i++)
            {
                bool found = false;
                foreach (Outlook.MAPIFolder subfolder in current.Folders)
                {
                    if (string.Equals(subfolder.Name, parts[i], StringComparison.OrdinalIgnoreCase))
                    {
                        current = subfolder;
                        found = true;
                        break;
                    }
                }
                if (!found)
                {
                    throw new ArgumentException($"Folder not found: '{parts[i]}' in path '{folderPath}'");
                }
            }

            return current;
        }

        /// <summary>
        /// Get hierarchical folder list for all stores.
        /// </summary>
        public string GetFolderTree()
        {
            var sb = new StringBuilder();
            var session = _outlookApp.Session;

            foreach (Outlook.Store store in session.Stores)
            {
                sb.AppendLine($"[{store.DisplayName}]");
                var rootFolder = store.GetRootFolder() as Outlook.MAPIFolder;
                if (rootFolder != null)
                {
                    BuildFolderTree(rootFolder.Folders, sb, "  ");
                }
                sb.AppendLine();
            }

            return sb.ToString();
        }

        /// <summary>
        /// List direct subfolders of a given folder path.
        /// </summary>
        public List<string> GetSubfolders(string folderPath)
        {
            var folder = GetFolder(folderPath);
            var result = new List<string>();
            foreach (Outlook.MAPIFolder subfolder in folder.Folders)
            {
                result.Add(subfolder.Name);
            }
            return result;
        }

        private void BuildFolderTree(Outlook.Folders folders, StringBuilder sb, string indent)
        {
            foreach (Outlook.MAPIFolder folder in folders)
            {
                int itemCount = 0;
                try { itemCount = folder.Items.Count; } catch { }
                sb.AppendLine($"{indent}{folder.Name} ({itemCount} items)");

                if (folder.Folders.Count > 0)
                {
                    BuildFolderTree(folder.Folders, sb, indent + "  ");
                }
            }
        }

        private Outlook.MAPIFolder TryGetDefaultFolder(string name)
        {
            try
            {
                var session = _outlookApp.Session;
                switch (name.ToLowerInvariant())
                {
                    case "inbox":
                    case "posteingang":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderInbox);
                    case "sent items":
                    case "sent":
                    case "gesendete elemente":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderSentMail);
                    case "deleted items":
                    case "trash":
                    case "gelöschte elemente":
                    case "papierkorb":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderDeletedItems);
                    case "drafts":
                    case "entwürfe":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderDrafts);
                    case "junk":
                    case "junk-e-mail":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderJunk);
                    case "outbox":
                    case "postausgang":
                        return session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderOutbox);
                    default:
                        return null;
                }
            }
            catch
            {
                return null;
            }
        }
    }
}

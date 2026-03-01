using System;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Tools.FolderTools
{
    // ===== Tool 14: get_folder_list =====
    public class GetFolderListTool : IOutlookTool
    {
        private readonly FolderNavigator _folderNav;
        public string Name => "get_folder_list";

        public GetFolderListTool(FolderNavigator nav) { _folderNav = nav; }

        public Task<object> ExecuteAsync(JObject p)
        {
            string tree = _folderNav.GetFolderTree();
            return Task.FromResult<object>(new { type = "text", text = tree });
        }
    }

    // ===== Tool 15: list_subfolders =====
    public class ListSubfoldersTool : IOutlookTool
    {
        private readonly FolderNavigator _folderNav;
        public string Name => "list_subfolders";

        public ListSubfoldersTool(FolderNavigator nav) { _folderNav = nav; }

        public Task<object> ExecuteAsync(JObject p)
        {
            string folderPath = p.Value<string>("folder_path");
            if (string.IsNullOrWhiteSpace(folderPath))
                return Task.FromResult<object>(new { type = "text", text = "Error: folder_path is required." });

            var subfolders = _folderNav.GetSubfolders(folderPath);
            if (subfolders.Count == 0)
                return Task.FromResult<object>(new { type = "text", text = $"No subfolders in '{folderPath}'." });

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Subfolders: {string.Join(", ", subfolders)}"
            });
        }
    }

    // ===== Tool 16: create_folder =====
    public class CreateFolderTool : IOutlookTool
    {
        private readonly Outlook.Application _outlookApp;
        private readonly FolderNavigator _folderNav;
        public string Name => "create_folder";

        public CreateFolderTool(Outlook.Application app, FolderNavigator nav)
        {
            _outlookApp = app;
            _folderNav = nav;
        }

        public Task<object> ExecuteAsync(JObject p)
        {
            string folderName = p.Value<string>("folder_name");
            string parentFolderName = p.Value<string>("parent_folder_name");

            if (string.IsNullOrWhiteSpace(folderName))
                return Task.FromResult<object>(new { type = "text", text = "Error: folder_name is required." });

            Outlook.MAPIFolder parentFolder;
            if (string.IsNullOrWhiteSpace(parentFolderName))
            {
                parentFolder = _outlookApp.Session.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderInbox);
            }
            else
            {
                parentFolder = _folderNav.GetFolder(parentFolderName);
            }

            parentFolder.Folders.Add(folderName);

            string fullPath = string.IsNullOrWhiteSpace(parentFolderName)
                ? $"Inbox/{folderName}"
                : $"{parentFolderName}/{folderName}";

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Folder created successfully: {fullPath}"
            });
        }
    }

    // ===== Tool 17: remove_folder =====
    public class RemoveFolderTool : IOutlookTool
    {
        private readonly FolderNavigator _folderNav;
        public string Name => "remove_folder";

        public RemoveFolderTool(FolderNavigator nav) { _folderNav = nav; }

        public Task<object> ExecuteAsync(JObject p)
        {
            string folderName = p.Value<string>("folder_name");
            if (string.IsNullOrWhiteSpace(folderName))
                return Task.FromResult<object>(new { type = "text", text = "Error: folder_name is required." });

            var folder = _folderNav.GetFolder(folderName);
            folder.Delete();

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Folder removed successfully: {folderName}"
            });
        }
    }

    // ===== Tool 18: move_folder =====
    public class MoveFolderTool : IOutlookTool
    {
        private readonly FolderNavigator _folderNav;
        public string Name => "move_folder";

        public MoveFolderTool(FolderNavigator nav) { _folderNav = nav; }

        public Task<object> ExecuteAsync(JObject p)
        {
            string sourcePath = p.Value<string>("source_folder_path");
            string targetParentPath = p.Value<string>("target_parent_path");

            if (string.IsNullOrWhiteSpace(sourcePath))
                return Task.FromResult<object>(new { type = "text", text = "Error: source_folder_path is required." });
            if (string.IsNullOrWhiteSpace(targetParentPath))
                return Task.FromResult<object>(new { type = "text", text = "Error: target_parent_path is required." });

            var sourceFolder = _folderNav.GetFolder(sourcePath);
            var targetParent = _folderNav.GetFolder(targetParentPath);

            int emailCount = 0;
            try { emailCount = sourceFolder.Items.Count; } catch { }

            sourceFolder.MoveTo(targetParent);

            return Task.FromResult<object>(new
            {
                type = "text",
                text = $"Folder moved successfully from '{sourcePath}' to '{targetParentPath}' ({emailCount} emails moved)"
            });
        }
    }
}

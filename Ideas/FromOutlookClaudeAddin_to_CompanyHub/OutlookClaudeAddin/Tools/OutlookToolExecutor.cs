using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OutlookClaudeAddin.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin.Tools
{
    /// <summary>
    /// Dispatches Claude tool_use calls to the correct tool implementation.
    /// All 19 tools are registered here.
    /// </summary>
    public class OutlookToolExecutor
    {
        private readonly Dictionary<string, IOutlookTool> _tools = new Dictionary<string, IOutlookTool>();
        private readonly EmailCache _emailCache;
        private readonly FolderNavigator _folderNav;
        private readonly Outlook.Application _outlookApp;

        public OutlookToolExecutor(Outlook.Application outlookApp)
        {
            _outlookApp = outlookApp;
            _emailCache = new EmailCache();
            _folderNav = new FolderNavigator(outlookApp);

            RegisterAllTools();
        }

        private void RegisterAllTools()
        {
            // Search Tools (5)
            Register(new SearchTools.ListRecentEmailsTool(_outlookApp, _emailCache, _folderNav));
            Register(new SearchTools.SearchBySubjectTool(_outlookApp, _emailCache, _folderNav));
            Register(new SearchTools.SearchBySenderTool(_outlookApp, _emailCache, _folderNav));
            Register(new SearchTools.SearchByRecipientTool(_outlookApp, _emailCache, _folderNav));
            // SearchByBodyTool REMOVED - privacy: no body access

            // Viewing Tools (4)
            Register(new ViewingTools.ViewEmailCacheTool(_emailCache));
            Register(new ViewingTools.GetEmailByNumberTool(_emailCache));
            Register(new ViewingTools.LoadEmailsByFolderTool(_outlookApp, _emailCache, _folderNav));
            Register(new ViewingTools.ClearEmailCacheTool(_emailCache));

            // Email Operation Tools (4)
            Register(new EmailOperationTools.ReplyToEmailTool(_outlookApp, _emailCache));
            Register(new EmailOperationTools.ComposeEmailTool(_outlookApp));
            Register(new EmailOperationTools.MoveEmailTool(_outlookApp, _emailCache, _folderNav));
            Register(new EmailOperationTools.DeleteEmailTool(_outlookApp, _emailCache));

            // Folder Tools (5)
            Register(new FolderTools.GetFolderListTool(_folderNav));
            Register(new FolderTools.ListSubfoldersTool(_folderNav));
            Register(new FolderTools.CreateFolderTool(_outlookApp, _folderNav));
            Register(new FolderTools.RemoveFolderTool(_folderNav));
            Register(new FolderTools.MoveFolderTool(_folderNav));

            // Batch (1)
            Register(new EmailOperationTools.BatchForwardEmailTool(_outlookApp, _emailCache));
        }

        private void Register(IOutlookTool tool)
        {
            _tools[tool.Name] = tool;
        }

        /// <summary>
        /// Execute a tool by name with given parameters. Returns JSON string result.
        /// </summary>
        public async Task<string> ExecuteToolAsync(string toolName, JObject parameters)
        {
            if (!_tools.TryGetValue(toolName, out var tool))
            {
                return JsonConvert.SerializeObject(new { error = $"Unknown tool: {toolName}" });
            }

            try
            {
                var result = await tool.ExecuteAsync(parameters ?? new JObject());
                return JsonConvert.SerializeObject(result);
            }
            catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new
                {
                    error = ex.Message,
                    tool = toolName,
                    type = ex.GetType().Name
                });
            }
        }
    }
}

using System;
using Microsoft.Office.Tools;
using OutlookClaudeAddin.Services;
using OutlookClaudeAddin.Tools;
using OutlookClaudeAddin.UI;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookClaudeAddin
{
    public partial class ThisAddIn
    {
        private CustomTaskPane _chatTaskPane;
        private ClaudeService _claudeService;
        private OutlookToolExecutor _toolExecutor;

        private void ThisAddIn_Startup(object sender, EventArgs e)
        {
            try
            {
                // Get API key (prompt if not stored)
                string apiKey = GetApiKey();
                if (string.IsNullOrEmpty(apiKey))
                {
                    // User cancelled - don't show task pane
                    return;
                }

                // Initialize services
                _claudeService = new ClaudeService(apiKey);
                _toolExecutor = new OutlookToolExecutor(Application);

                // Create the task pane
                var host = new TaskPaneHost();
                var viewModel = new ChatViewModel(_claudeService, _toolExecutor);
                host.ChatView.DataContext = viewModel;

                // Wire up scroll-to-bottom
                viewModel.ScrollToBottomRequested += () =>
                {
                    try { host.ChatView.ScrollToBottom(); } catch { }
                };

                // Add custom task pane
                _chatTaskPane = CustomTaskPanes.Add(host, "Claude Email Assistant");
                _chatTaskPane.DockPosition = Microsoft.Office.Core.MsoCTPDockPosition.msoCTPDockPositionRight;
                _chatTaskPane.Width = 380;
                _chatTaskPane.Visible = true;
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show(
                    $"Fehler beim Laden des Claude Add-Ins:\n{ex.Message}",
                    "Claude Email Assistant",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.Error);
            }
        }

        private void ThisAddIn_Shutdown(object sender, EventArgs e)
        {
            // Cleanup
        }

        private string GetApiKey()
        {
            // Try to load from user settings
            string apiKey = Properties.Settings.Default.AnthropicApiKey;

            if (string.IsNullOrWhiteSpace(apiKey))
            {
                // Prompt user
                var dialog = new ApiKeyDialog();
                if (dialog.ShowDialog() == true)
                {
                    apiKey = dialog.ApiKey;
                    Properties.Settings.Default.AnthropicApiKey = apiKey;
                    Properties.Settings.Default.Save();
                }
                else
                {
                    return null;
                }
            }

            return apiKey;
        }

        #region VSTO generated code

        /// <summary>
        /// Required method for Designer support.
        /// </summary>
        partial void InternalStartup()
        {
            this.Startup += new EventHandler(ThisAddIn_Startup);
            this.Shutdown += new EventHandler(ThisAddIn_Shutdown);
        }

        #endregion
    }
}

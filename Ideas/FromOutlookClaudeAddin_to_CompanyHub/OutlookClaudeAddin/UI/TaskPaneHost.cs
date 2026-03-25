using System.Windows.Forms;
using System.Windows.Forms.Integration;

namespace OutlookClaudeAddin.UI
{
    /// <summary>
    /// WinForms UserControl that hosts the WPF ChatView via ElementHost.
    /// VSTO Custom Task Panes require a WinForms control.
    /// </summary>
    public class TaskPaneHost : UserControl
    {
        private readonly ElementHost _elementHost;
        private readonly ChatView _chatView;

        public ChatView ChatView => _chatView;

        public TaskPaneHost()
        {
            _chatView = new ChatView();

            _elementHost = new ElementHost
            {
                Dock = DockStyle.Fill,
                Child = _chatView
            };

            Controls.Add(_elementHost);
        }
    }
}

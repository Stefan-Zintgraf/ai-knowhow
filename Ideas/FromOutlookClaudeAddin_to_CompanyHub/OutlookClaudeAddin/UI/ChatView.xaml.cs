using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace OutlookClaudeAddin.UI
{
    public partial class ChatView : UserControl
    {
        public ChatView()
        {
            // Register BoolToVisibility converter in resources before InitializeComponent
            Resources.Add("BoolToVisConverter", new BooleanToVisibilityConverter());
            InitializeComponent();
        }

        /// <summary>
        /// Auto-scroll to bottom when new messages arrive.
        /// Call this from ViewModel via event or binding.
        /// </summary>
        public void ScrollToBottom()
        {
            MessageScrollViewer?.ScrollToEnd();
        }
    }
}

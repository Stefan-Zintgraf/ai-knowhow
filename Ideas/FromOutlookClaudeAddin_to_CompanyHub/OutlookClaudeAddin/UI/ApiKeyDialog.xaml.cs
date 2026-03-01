using System.Diagnostics;
using System.Windows;

namespace OutlookClaudeAddin.UI
{
    public partial class ApiKeyDialog : Window
    {
        public string ApiKey { get; private set; }

        public ApiKeyDialog()
        {
            InitializeComponent();
            ApiKeyTextBox.Focus();
        }

        public ApiKeyDialog(string existingKey) : this()
        {
            if (!string.IsNullOrEmpty(existingKey))
                ApiKeyTextBox.Text = existingKey;
        }

        private void OkButton_Click(object sender, RoutedEventArgs e)
        {
            var key = ApiKeyTextBox.Text?.Trim();
            if (string.IsNullOrWhiteSpace(key))
            {
                MessageBox.Show("Bitte gib einen API Key ein.", "Fehler",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!key.StartsWith("sk-"))
            {
                MessageBox.Show("Der API Key sollte mit 'sk-' beginnen.", "Fehler",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            ApiKey = key;
            DialogResult = true;
            Close();
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        private void ConsoleLink_Click(object sender, RoutedEventArgs e)
        {
            Process.Start("https://console.anthropic.com");
        }

        private void KeysLink_Click(object sender, RoutedEventArgs e)
        {
            Process.Start("https://console.anthropic.com/settings/keys");
        }
    }
}

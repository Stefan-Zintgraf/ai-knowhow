using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Threading;
using OutlookClaudeAddin.Services;
using OutlookClaudeAddin.Tools;

namespace OutlookClaudeAddin.UI
{
    public class ChatViewModel : INotifyPropertyChanged
    {
        private readonly ClaudeService _claudeService;
        private readonly OutlookToolExecutor _toolExecutor;
        private readonly Dispatcher _uiDispatcher;
        private string _inputText;
        private bool _isLoading;

        public ObservableCollection<ChatMessage> Messages { get; } = new ObservableCollection<ChatMessage>();

        public string InputText
        {
            get => _inputText;
            set { _inputText = value; OnPropertyChanged(); }
        }

        public bool IsLoading
        {
            get => _isLoading;
            set { _isLoading = value; OnPropertyChanged(); }
        }

        public ICommand SendMessageCommand { get; }
        public ICommand NewChatCommand { get; }

        /// <summary>
        /// Event to notify the View to scroll to bottom.
        /// </summary>
        public event Action ScrollToBottomRequested;

        public ChatViewModel(ClaudeService claudeService, OutlookToolExecutor toolExecutor)
        {
            _claudeService = claudeService;
            _toolExecutor = toolExecutor;
            _uiDispatcher = Dispatcher.CurrentDispatcher;

            SendMessageCommand = new RelayCommand(async _ => await SendMessageAsync(), _ => !IsLoading && !string.IsNullOrWhiteSpace(InputText));
            NewChatCommand = new RelayCommand(_ => StartNewChat());

            Messages.Add(new ChatMessage("system",
                "Willkommen! Ich bin dein E-Mail-Assistent. Sag mir was du brauchst, z.B.:\n" +
                "• \"Suche Emails von Max der letzten 7 Tage\"\n" +
                "• \"Zeig mir alle Ordner\"\n" +
                "• \"Verschiebe Email 1 nach Archiv\""));
        }

        private async Task SendMessageAsync()
        {
            string userText = InputText?.Trim();
            if (string.IsNullOrEmpty(userText)) return;

            // Add user message to chat
            AddMessage("user", userText);
            InputText = "";
            IsLoading = true;

            try
            {
                string response = await _claudeService.SendMessageAsync(userText, _toolExecutor);
                AddMessage("assistant", response);
            }
            catch (Exception ex)
            {
                AddMessage("system", $"Fehler: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void StartNewChat()
        {
            Messages.Clear();
            _claudeService.ClearHistory();
            Messages.Add(new ChatMessage("system", "Neuer Chat gestartet. Wie kann ich helfen?"));
        }

        private void AddMessage(string role, string content)
        {
            // Must run on UI thread - use stored dispatcher (Application.Current is null in VSTO)
            if (!_uiDispatcher.CheckAccess())
            {
                _uiDispatcher.Invoke(() => AddMessage(role, content));
                return;
            }

            Messages.Add(new ChatMessage(role, content));
            ScrollToBottomRequested?.Invoke();
        }

        #region INotifyPropertyChanged

        public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            if (!_uiDispatcher.CheckAccess())
            {
                _uiDispatcher.Invoke(() => OnPropertyChanged(name));
                return;
            }
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        #endregion
    }

    /// <summary>
    /// Simple ICommand implementation for MVVM.
    /// </summary>
    public class RelayCommand : ICommand
    {
        private readonly Func<object, Task> _executeAsync;
        private readonly Action<object> _execute;
        private readonly Predicate<object> _canExecute;

        public RelayCommand(Func<object, Task> executeAsync, Predicate<object> canExecute = null)
        {
            _executeAsync = executeAsync;
            _canExecute = canExecute;
        }

        public RelayCommand(Action<object> execute, Predicate<object> canExecute = null)
        {
            _execute = execute;
            _canExecute = canExecute;
        }

        public bool CanExecute(object parameter) => _canExecute?.Invoke(parameter) ?? true;

        public async void Execute(object parameter)
        {
            if (_executeAsync != null)
                await _executeAsync(parameter);
            else
                _execute?.Invoke(parameter);
        }

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
    }
}

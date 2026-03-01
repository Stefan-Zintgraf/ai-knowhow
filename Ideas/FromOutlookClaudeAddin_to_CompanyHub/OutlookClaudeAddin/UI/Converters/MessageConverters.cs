using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;

namespace OutlookClaudeAddin.UI.Converters
{
    /// <summary>
    /// Aligns user messages right, assistant messages left.
    /// </summary>
    public class MessageAlignmentConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            return (value as string) == "user"
                ? HorizontalAlignment.Right
                : HorizontalAlignment.Left;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }

    /// <summary>
    /// User = blue background, Assistant = dark gray, System = red.
    /// </summary>
    public class MessageBackgroundConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            switch (value as string)
            {
                case "user":
                    return new SolidColorBrush(Color.FromRgb(0, 120, 212)); // Outlook blue
                case "assistant":
                    return new SolidColorBrush(Color.FromRgb(50, 50, 50));  // Dark gray
                case "system":
                    return new SolidColorBrush(Color.FromRgb(120, 30, 30)); // Dark red
                default:
                    return new SolidColorBrush(Color.FromRgb(50, 50, 50));
            }
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }

    /// <summary>
    /// All messages use white foreground text.
    /// </summary>
    public class MessageForegroundConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            return Brushes.White;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }
}

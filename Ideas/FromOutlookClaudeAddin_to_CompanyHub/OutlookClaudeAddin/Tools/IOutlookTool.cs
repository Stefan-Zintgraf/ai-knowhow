using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace OutlookClaudeAddin.Tools
{
    /// <summary>
    /// Interface for all Outlook tools that Claude can invoke.
    /// </summary>
    public interface IOutlookTool
    {
        string Name { get; }
        Task<object> ExecuteAsync(JObject parameters);
    }
}

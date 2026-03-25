using System;
using System.Collections.Generic;
using System.Linq;

namespace OutlookClaudeAddin.Core
{
    /// <summary>
    /// Thread-safe in-memory email cache.
    /// Mirrors the Python MCP server's email_cache + email_cache_order pattern.
    /// Emails are stored newest-first by ReceivedTime.
    /// </summary>
    public class EmailCache
    {
        private readonly Dictionary<string, EmailData> _cache = new Dictionary<string, EmailData>();
        private readonly List<string> _order = new List<string>(); // newest first
        private readonly object _lock = new object();

        public int Count
        {
            get { lock (_lock) { return _order.Count; } }
        }

        /// <summary>
        /// Add an email to the cache, maintaining newest-first sort order.
        /// Duplicate EntryIds are skipped.
        /// </summary>
        public void Add(EmailData email)
        {
            if (email == null || string.IsNullOrEmpty(email.EntryId)) return;

            lock (_lock)
            {
                if (_cache.ContainsKey(email.EntryId)) return;

                _cache[email.EntryId] = email;

                // Insert in sorted position (newest first = descending by ReceivedTime)
                if (_order.Count == 0)
                {
                    _order.Add(email.EntryId);
                }
                else
                {
                    int insertIndex = FindInsertIndex(email.ReceivedTime);
                    _order.Insert(insertIndex, email.EntryId);
                }
            }
        }

        /// <summary>
        /// Add multiple emails at once (more efficient for bulk loading).
        /// </summary>
        public void AddRange(IEnumerable<EmailData> emails)
        {
            foreach (var email in emails)
            {
                Add(email);
            }
        }

        /// <summary>
        /// Get email by 1-based cache number.
        /// </summary>
        public EmailData GetByNumber(int number)
        {
            lock (_lock)
            {
                if (number < 1 || number > _order.Count)
                    return null;

                var id = _order[number - 1];
                return _cache.TryGetValue(id, out var email) ? email : null;
            }
        }

        /// <summary>
        /// Get a page of email summaries (5 per page, 1-based page number).
        /// </summary>
        public (List<Dictionary<string, object>> emails, int totalPages, int totalEmails) GetPage(int page = 1, int pageSize = 5)
        {
            lock (_lock)
            {
                int totalEmails = _order.Count;
                int totalPages = Math.Max(1, (int)Math.Ceiling((double)totalEmails / pageSize));
                page = Math.Max(1, Math.Min(page, totalPages));

                var result = new List<Dictionary<string, object>>();
                int startIndex = (page - 1) * pageSize;
                int endIndex = Math.Min(startIndex + pageSize, totalEmails);

                for (int i = startIndex; i < endIndex; i++)
                {
                    var id = _order[i];
                    if (_cache.TryGetValue(id, out var email))
                    {
                        result.Add(email.ToSummary(i + 1)); // 1-based number
                    }
                }

                return (result, totalPages, totalEmails);
            }
        }

        /// <summary>
        /// Clear all cached emails.
        /// </summary>
        public void Clear()
        {
            lock (_lock)
            {
                _cache.Clear();
                _order.Clear();
            }
        }

        /// <summary>
        /// Binary search for insert position (newest first = descending order).
        /// </summary>
        private int FindInsertIndex(DateTime receivedTime)
        {
            int lo = 0, hi = _order.Count;
            while (lo < hi)
            {
                int mid = (lo + hi) / 2;
                var midTime = _cache[_order[mid]].ReceivedTime;
                if (midTime >= receivedTime)
                    lo = mid + 1;
                else
                    hi = mid;
            }
            return lo;
        }
    }
}

--remode

Current WI: plan/42_add-csv-export/
Current mode: mini
Current phase: aln

During alignment grilling, we discovered that the CSV export feature needs to handle concurrent file generation requests — multiple users can trigger exports simultaneously, and we need to prevent duplicate processing and manage a job queue. The original brief only mentioned "add CSV export to the reports page." The grilling surfaced concurrency as a real concern that was not visible at triage time.

Reason for re-triage: concurrency is a tripwire surface (3.29 list). Scope grew beyond what mini mode covers.

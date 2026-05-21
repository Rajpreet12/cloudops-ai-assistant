from config import invoke_claude
from datetime import datetime

def run(monitor_result, diagnosis, remediation):
    prompt = f"""Generate a concise incident report:

## Incident report — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

**Alarms triggered:**
{monitor_result.get('summary', 'N/A')}

**Root cause:**
{diagnosis}

**Remediation steps:**
{remediation}

**Status:** [Open / Mitigated / Resolved]

Keep it under 300 words."""

    return invoke_claude(prompt, system="You are a technical writer producing incident reports.") 

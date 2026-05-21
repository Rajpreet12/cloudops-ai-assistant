from config import cw, invoke_claude

def run(alarm_name=None):
    if alarm_name:
        alarms = cw.describe_alarms(AlarmNames=[alarm_name])
    else:
        alarms = cw.describe_alarms(StateValue="ALARM", MaxRecords=5)

    items = alarms["MetricAlarms"]
    if not items:
        return {"status": "ok", "alarms": []}

    summary = "\n".join([
        f"- {a['AlarmName']}: {a['StateReason']} (metric: {a['MetricName']})"
        for a in items
    ])

    analysis = invoke_claude(
        f"Summarise these CloudWatch alarms for a DevOps engineer:\n{summary}",
        system="You are a CloudOps monitoring expert. Be concise and precise."
    )

    return {"status": "alarm", "raw": items, "summary": analysis} 

from config import bedrock_agent, invoke_claude, KB_ID

def run(alarm_summary):
    context = ""

    if KB_ID:
        response = bedrock_agent.retrieve(
            knowledgeBaseId=KB_ID,
            retrievalQuery={"text": alarm_summary},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 3}}
        )
        docs = response.get("retrievalResults", [])
        context = "\n\n".join([d["content"]["text"] for d in docs])

    prompt = f"""You are diagnosing a cloud incident.

Alarm summary:
{alarm_summary}

Relevant runbook context:
{context or 'No runbook context available — use general AWS best practices.'}

Provide:
1. Most likely root cause
2. Severity (P1/P2/P3)
3. Affected services
4. Confidence level (high/medium/low)"""

    return invoke_claude(prompt, system="You are a senior SRE diagnosing AWS incidents.")

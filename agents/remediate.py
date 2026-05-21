from config import invoke_claude

SAFE_ACTIONS = [
    "scale_out_asg",
    "restart_ecs_service",
    "clear_cache",
    "notify_team"
]

def run(diagnosis):
    prompt = f"""Based on this diagnosis:
{diagnosis}

Suggest 2-3 remediation steps. For each step specify:
- Action name (use one of: {', '.join(SAFE_ACTIONS)} if applicable)
- Command or AWS console path
- Expected outcome
- Risk level (low/medium/high)

Only recommend high-risk actions as a last resort."""

    return invoke_claude(
        prompt,
        system="You are a CloudOps automation engineer. Prioritise safe, reversible actions."
    )

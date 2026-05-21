from agents import monitor, diagnose, remediate, reporter

def handle_incident(alarm_name=None):
    print("\n[1/4] Monitor agent — scanning alarms...")
    mon = monitor.run(alarm_name)

    if mon["status"] == "ok":
        print("  No active alarms. System healthy.")
        return

    print("[2/4] Diagnose agent — analysing root cause...")
    diag = diagnose.run(mon["summary"])
    print(f"  Diagnosis:\n{diag}\n")

    print("[3/4] Remediate agent — generating fix recommendations...")
    remed = remediate.run(diag)
    print(f"  Recommendations:\n{remed}\n")

    print("[4/4] Reporter agent — drafting incident report...")
    report = reporter.run(mon, diag, remed)
    print(f"\n{'='*60}\n{report}\n{'='*60}")

    return report

if __name__ == "__main__":
    handle_incident()

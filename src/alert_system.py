def send_alert(risk):
    if risk == "High":
        return "🚨 HIGH RISK ALERT: Immediate action required!"
    elif risk == "Medium":
        return "⚠️ MEDIUM RISK: Monitor conditions closely."
    else:
        return "✅ LOW RISK: Crop conditions are stable."
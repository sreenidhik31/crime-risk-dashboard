def calculate_risk_score(crime_count, max_crime_count):
    if max_crime_count == 0:
        return 0

    return crime_count / max_crime_count


def patrol_recommendation(risk_score):
    if risk_score >= 0.70:
        return "Increase Patrol"
    elif risk_score >= 0.40:
        return "Monitor Area"
    else:
        return "No Immediate Action"
def analyze_lead(lead):

    score = 75

    return {
        "company": lead["company"],
        "country": lead["country"],
        "industry": lead["industry"],
        "opportunity_score": score,
        "recommendation": "Contact company with growth proposal"
    }
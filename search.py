def search_businesses(countries, businesses):

    leads = []

    for country in countries:

        for business in businesses:

            leads.append({
                "company": f"{business} Example",
                "country": country,
                "industry": business
            })


    return leads
    return leads
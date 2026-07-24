import json


def create_report(leads):

    with open(
        "outputs/reports/leads_report.json",
        "w"
    ) as file:

        json.dump(
            leads,
            file,
            indent=4
        )


    print("📄 Report created")
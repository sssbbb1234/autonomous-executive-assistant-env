ALL_TASKS = {

    "easy": {
        "emails": [
            {
                "id": "e1",
                "sender": "promo@shopping.com",
                "subject": "Big Sale Today!",
                "body": "Get 50% off on all items.",
                "processed": False
            }
        ],
        "ground_truth": {
            "e1": {
                "label": "spam"
            }
        }
    },

    "medium": {
        "emails": [
            {
                "id": "e2",
                "sender": "manager@company.com",
                "subject": "Submit report",
                "body": "Please submit the report by today evening.",
                "processed": False
            }
        ],
        "ground_truth": {
            "e2": {
                "label": "actionable",
                "task": "submit report"
            }
        }
    },

    "hard": {
        "emails": [
            {
                "id": "e3",
                "sender": "jane.doe@corp.com",
                "subject": "Project Sync",
                "body": "Can we meet Tuesday at 2 PM in Blue Room?",
                "processed": False
            }
        ],
        "ground_truth": {
            "e3": {
                "label": "actionable",
                "task": "schedule meeting",
                "time": "Tuesday 2 PM",
                "reply_required": True
            }
        }
    }

}
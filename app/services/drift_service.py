import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict

# Initialize Firebase if it hasn't been set up yet
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

db = firestore.client()

_COLLECTION = "drift_logs"


def log_cohort_drift(user_id: str, month: str, value: float) -> Dict:
    """Log or update the user's drift value in Firestore."""
    doc_id = f"{user_id}_{month}"
    doc_ref = db.collection(_COLLECTION).document(doc_id)

    doc_ref.set({
        "user_id": user_id,
        "month": month,
        "value": value
    })

    return {"status": "ok", "message": "Drift logged successfully"}


def get_cohort_drift(user_id: str, month: str) -> Dict:
    """Return drift for the given month along with user history."""
    # Current month record
    doc_id = f"{user_id}_{month}"
    current_doc = db.collection(_COLLECTION).document(doc_id).get()
    drift_value = current_doc.to_dict().get("value", 0.0) if current_doc.exists else 0.0

    # Fetch the user's entire drift history
    query = db.collection(_COLLECTION).where("user_id", "==", user_id).stream()
    history = [{"month": doc.to_dict()["month"], "value": doc.to_dict()["value"]} for doc in query]

    return {
        "user_id": user_id,
        "month": month,
        "drift_value": drift_value,
        "history": sorted(history, key=lambda x: x["month"])
    }

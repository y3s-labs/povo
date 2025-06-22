from app.src.classifier import Classifier

if __name__ == "__main__":
    classifier = Classifier()

    test_messages = [
        "I feel completely overwhelmed and don’t know what to do.",
        "What are your office hours?",
        "I'm just not feeling like myself lately.",
        "Can I reschedule my appointment?",
    ]

    for msg in test_messages:
        result = classifier.classify(msg)
        print(f"Message: {msg}\n→ Predicted intent: {result.intent}\n")

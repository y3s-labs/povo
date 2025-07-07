from src.services.classifier import Classifier

if __name__ == "__main__":
    classifier = Classifier()

    test_messages = [
        "I love pizza",
        "I love pizza with mushrooms",
        "I love pizza with mushrooms and pepperoni",
        "I hate pizza",
        "medium pizza with mushrooms and pepperoni",
        "medium",
        "medium pizza"
    ]

    for msg in test_messages:
        result = classifier.classify(msg)
        print(f"Message: {msg}\n→ Predicted intent: {result}\n")

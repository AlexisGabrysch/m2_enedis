from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier

class Model:
    def __init__(self, model):
        self.model = model

    def train(self, X, y, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self):
        predictions = self.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        conf_matrix = confusion_matrix(self.y_test, predictions)
        class_report = classification_report(self.y_test, predictions)
        return {
            'accuracy': accuracy,
            'confusion_matrix': conf_matrix,
            'classification_report': class_report
        }

# Example usage
if __name__ == "__main__":
    # Assuming you have your data in variables X and y
    model = Model(DecisionTreeClassifier())
    model.train(X, y)
    evaluation = model.evaluate()
    print(evaluation)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class Model:
    def __init__(self):
        self.model = joblib.load('model/model.pkl')
        self.features = joblib.load('model/features.pkl')  # Load the features used during training
        # self.scaler = joblib.load('model/scaler.pkl')
        self.etiquette = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def train(self, df, test_size=0.2):
        df = df.dropna()
        
        X = df.drop(columns=['Conso_5_usages_é_finale', 'Etiquette_DPE'])
        y = df[['Conso_5_usages_é_finale', 'Etiquette_DPE']]

        X = pd.get_dummies(X, drop_first=True)

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
       
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        self.model = MultiOutputRegressor(RandomForestRegressor(n_estimators=10, random_state=0))

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        y_pred_conso = y_pred[:, 0]
        y_pred_etiquette = y_pred[:, 1].round().astype(int)  # Arrondir et convertir en entier pour les étiquettes
        self.X_test = X_test
        self.y_test = y_test

        # Évaluer le modèle pour Conso_5_usages_é_finale
        print("Mean Squared Error (Conso_5_usages_é_finale):", mean_squared_error(y_test['Conso_5_usages_é_finale'], y_pred_conso))
        print("R2 Score (Conso_5_usages_é_finale):", r2_score(y_test['Conso_5_usages_é_finale'], y_pred_conso))

        # Évaluer le modèle pour Etiquette_DPE
        print("Accuracy (Etiquette_DPE):", accuracy_score(y_test['Etiquette_DPE'], y_pred_etiquette))
        print("Classification Report (Etiquette_DPE):\n", classification_report(y_test['Etiquette_DPE'], y_pred_etiquette, labels=range(len(label_encoder.classes_)), target_names=label_encoder.classes_))

        joblib.dump(label_encoder.classes_, 'model/features.pkl', compress=1)
        joblib.dump(self.model, 'model/model.pkl', compress=9)
        joblib.dump(scaler, 'model/scaler.pkl', compress=9)

    def prediction(self, df, categorical_columns):
        X = pd.get_dummies(df, columns=categorical_columns)
        X = X.reindex(columns=self.features, fill_value=0)  # Ensure all columns are present

        # X = self.scaler.transform(X)
      
        predictions = self.model.predict(X)
        predictions_conso = predictions[:, 0].round(2)
        predictions_etiquette = predictions[:, 1].round().astype(int)
        predictions_etiquette = [self.etiquette[i] for i in predictions_etiquette]
        return predictions_conso, predictions_etiquette

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

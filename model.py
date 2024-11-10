from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import numpy as np

class Model:
    def __init__(self):
        self.model = joblib.load('model/model.pkl')
        self.features = joblib.load('model/feature_names.pkl')  # Load the features used during training
        self.scaler = joblib.load('model/scaler.pkl')

        self.etiquette = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
    def Prepare_data(self, df):
       
        df_final = df.drop(df.loc[df[["Qualité_isolation_plancher_haut_toit_terrase", "Qualité_isolation_plancher_haut_comble_aménagé", "Qualité_isolation_plancher_haut_comble_perdu"]].notnull().sum(axis=1) > 1].index)
                   # Créer la nouvelle colonne
     
        df_final['Type_isolation_plancher_haut'] = df_final.apply(
            lambda row: 'terrasse' if pd.notnull(row['Qualité_isolation_plancher_haut_toit_terrase']) else
                        'comble_aménagé' if pd.notnull(row['Qualité_isolation_plancher_haut_comble_aménagé']) else
                        'comble_perdu' if pd.notnull(row['Qualité_isolation_plancher_haut_comble_perdu']) else
                        np.nan,
            axis=1
        )

        df_final["Climatisation"] = df_final["Type_énergie_climatisation"].apply(lambda x: True if pd.notnull(x) else False)
        df_final = df_final.drop(columns=["Type_énergie_climatisation" , "Qualité_isolation_plancher_haut_toit_terrase", "Qualité_isolation_plancher_haut_comble_aménagé", "Qualité_isolation_plancher_haut_comble_perdu" , 
                                          "Conso_éclairage_é_finale",  "Conso_refroidissement_é_finale", "Conso_auxiliaires_é_finale", "Nom__commune_(BAN)", "Code_INSEE_(BAN)", "Coordonnée_cartographique_X_(BAN)", 
                                          "Coordonnée_cartographique_Y_(BAN)", "Coût_total_5_usages", "N°_département_(BAN)", "Conso_ECS_é_finale" , "N°DPE" , "Date_réception_DPE"])
       
        df_final = df_final.dropna().reset_index(drop=True) 
       
        return df_final

    def fine_tuning(self, df):
        scaler = StandardScaler()
        label_encoder = LabelEncoder()
        
        df_final = self.Prepare_data(df)
      
        X = df_final.drop(columns=['Conso_5_usages_é_finale', 'Etiquette_DPE'])
        y = df_final[['Conso_5_usages_é_finale', 'Etiquette_DPE']]
        # Encoder les étiquettes de la cible
        X = pd.get_dummies(X, drop_first=True)
        X = X.reindex(columns=self.features, fill_value=0)  # Ensure all columns are present
        X = pd.DataFrame(scaler.fit_transform(X) ,columns=X.columns)
        y['Etiquette_DPE'] = label_encoder.fit_transform(y['Etiquette_DPE'])
        # Entraîner le modèle
        self.model.fit(X, y)

        # Sauvegarder le modèle
        joblib.dump(self.model, 'model/model.pkl', compress=9)
        joblib.dump(scaler, 'model/scaler.pkl', compress=1)


        
        return  
        
        
    

    def train(self, df, test_size=0.2):
        df = df.dropna()
        
        X = df.drop(columns=['Conso_5_usages_é_finale', 'Etiquette_DPE'])
        y = df[['Conso_5_usages_é_finale', 'Etiquette_DPE']]

        X = pd.get_dummies(X, drop_first=True)
        X = X.reindex(columns=self.features, fill_value=0)  # Ensure all columns are present

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


        joblib.dump(self.model, 'model/model.pkl', compress=9)
        joblib.dump(scaler, 'model/scaler.pkl', compress=9)
        # Save the feature names after training
        joblib.dump(X.columns.tolist(), 'model/features_names.pkl', compress=1)




    def prediction(self, df, categorical_columns):
     
        
       
        X = pd.get_dummies(df, columns=categorical_columns)
      
        X = X.reindex(columns=self.features, fill_value=0)  # Ensure all columns are present
      
        X = self.scaler.transform(X)
      
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

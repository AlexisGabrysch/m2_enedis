import pandas as pd
import requests


class API:

    def __init__(self):

        self.df = pd.read_csv("assets/enedis_69.csv")

    def get_data(self):
        return self.df


    def refresher(self):
    
            # Call API to get IDs and DPE reception dates for department 69
        id_date_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q=69&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=Date_r%C3%A9ception_DPE%2CN%C2%B0DPE"
        id_date_data = []
        while True:
                response = requests.get(id_date_url)
                if response.status_code != 200:
                    print("Erreur lors de la requête")
                    break

                content = response.json()
                results = content['results']

                if not results:
                    print("Fin de la pagination")
                    print(len(id_date_data))
                    break
                id_date_data.extend(results)
                if content.get("next") is None:
                    print("Fin de la pagination None")
                    print(len(id_date_data))
                    break
                else:
                    id_date_url = content["next"]
  
        id_date_df = pd.DataFrame(id_date_data)
        id_date_df.drop(columns=["_score"])
        
        # Determine the maximum date
        max_date = self.df["Date_réception_DPE"].max()
        print(max_date)
        print(id_date_df["Date_réception_DPE"].max())
        new_data = id_date_df[id_date_df["Date_réception_DPE"] > max_date]

        if new_data.empty:
            print("No new data")
            return None, 0
        else:
            print("Fetching data")
            print(len(new_data))
            ids = new_data["N°DPE"].tolist()
        
            new_data = []
       
            for i in range(0, len(ids),200):
             
                batch_ids = '%2C'.join(map(str, ids[i:i+200]))
          
                try:
                    j = requests.get(url = f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={batch_ids}&q_fields=N%C2%B0DPE&select=Etiquette_DPE%2CType_b%C3%A2timent%2CP%C3%A9riode_construction%2CSurface_habitable_logement%2CHauteur_sous-plafond%2CN%C2%B0_%C3%A9tage_appartement%2CN%C2%B0_d%C3%A9partement_%28BAN%29%2CNombre_niveau_logement%2CQualit%C3%A9_isolation_plancher_haut_toit_terrase%2CQualit%C3%A9_isolation_plancher_haut_comble_am%C3%A9nag%C3%A9%2CQualit%C3%A9_isolation_plancher_haut_comble_perdu%2CQualit%C3%A9_isolation_plancher_bas%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CType_%C3%A9nergie_climatisation%2CNom__commune_%28BAN%29%2CCode_INSEE_%28BAN%29%2CCoordonn%C3%A9e_cartographique_X_%28BAN%29%2CCoordonn%C3%A9e_cartographique_Y_%28BAN%29%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_%C3%A9clairage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CConso_refroidissement_%C3%A9_finale%2CConso_auxiliaires_%C3%A9_finale%2CCo%C3%BBt_total_5_usages%2CDate_r%C3%A9ception_DPE%2CN%C2%B0DPE")
                #https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q=69&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=Date_r%C3%A9ception_DPE%2C_id"
# https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?select=Etiquette_DPE%2CType_b%C3%A2timent%2CP%C3%A9riode_construction%2CSurface_habitable_logement%2CHauteur_sous-plafond%2CN%C2%B0_%C3%A9tage_appartement%2CN%C2%B0_d%C3%A9partement_%28BAN%29%2CNombre_niveau_logement%2CQualit%C3%A9_isolation_plancher_haut_toit_terrase%2CQualit%C3%A9_isolation_plancher_haut_comble_am%C3%A9nag%C3%A9%2CQualit%C3%A9_isolation_plancher_haut_comble_perdu%2CQualit%C3%A9_isolation_plancher_bas%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CType_%C3%A9nergie_climatisation%2CNom__commune_%28BAN%29%2CCode_INSEE_%28BAN%29%2CCoordonn%C3%A9e_cartographique_X_%28BAN%29%2CCoordonn%C3%A9e_cartographique_Y_%28BAN%29%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_%C3%A9clairage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CConso_refroidissement_%C3%A9_finale%2CConso_auxiliaires_%C3%A9_finale%2CCo%C3%BBt_total_5_usages%2C_id%2CDate_r%C3%A9ception_DPE


                    res = j.json()
                    new_data.extend(res["results"])
                except:
                    print("Error")
                    return

            new_data = pd.DataFrame(new_data)

            new_data = new_data.drop(columns=["_score"])
            self.df = pd.concat([self.df, new_data], ignore_index=True, axis=0)
            self.df.to_csv("assets/enedis_69.csv", index=False , encoding="utf-8")
            nl = len(new_data)
        return self.df , nl

    def processing_data(self):
        # Drop columns that are not needed
        print("Processing data")
        return

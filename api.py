import pandas as pd
import requests
from tqdm import tqdm

class API:
    def __init__(self, base_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines", query = "69" , size=10000, fields="N%C2%B0_d%C3%A9partement_%28BAN%29", select="P%C3%A9riode_construction%2C%2C_id"):
        self.base_url = base_url
        self.query = query
        self.size = size
        self.fields = fields
        self.select = select
        self.df = pd.DataFrame()
        self.after = None

    def fetch_data(self):
        url = self.construct_url()
        response = requests.get(url)
        total = response.json()["total"]
        pbar = tqdm(total=total)
        pbar.set_description(f"Fetching data for {self.query}")
        
        while True:

            response = requests.get(url)

            if response.status_code != 200:
                print("Erreur lors de la requête")
                break

            content = response.json()
            results = content['results']
            pbar.update(len(results))

            if not results:
                pbar.close()
                print("Fin de la pagination")
                break
            self.df = pd.concat([self.df, pd.DataFrame(results)], ignore_index=True, axis=0)
            if content.get("next") is None:
                pbar.close()
                print("Fin de la pagination None")
                break
            else:
                self.after = content["next"]
                print(self.after)
                url = self.after

    def construct_url(self):
        url = f"{self.base_url}?q={self.query}&size={self.size}&q_fields={self.fields}&select={self.select}"
        return url


   
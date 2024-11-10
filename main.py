from UI import DashApp
from api import API
import pandas as pd

def start_app():
    api = API()
    df = api.get_data()
    app_instance = DashApp(df)
    app_instance.run()


if __name__ == "__main__":
    start_app()



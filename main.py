from UI import DashApp
from api import API

def start_app():
    api = API(query="09")
    api.fetch_data()
    df = api.df
    app_instance = DashApp(df)
    app_instance.run()


if __name__ == "__main__":
    start_app()
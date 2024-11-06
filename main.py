from UI import DashApp
from api import API
def main():
    """
    Initializes and starts the Dash application.
    This function creates an instance of the DashApp class and runs the application.
    """
    api = API(query="09")
    api.fetch_data()
    df = api.df
    interface = DashApp(df)
    interface.run()


if __name__ == "__main__":
    main()
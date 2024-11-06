from UI import DashApp
from api import API

api = API(query="09")
api.fetch_data()
df = api.df
app_instance = DashApp(df)

# Expose the server attribute
server = app_instance.server


if __name__ == "__main__":
    app_instance.app.run_server(debug=False)
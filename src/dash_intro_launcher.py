import setup_data as sd
from help_functions import save_properties
from dash_intro_app import run_dash_app

if __name__ == "__main__":
    sd.setup_all_data()
    save_properties()
    run_dash_app()

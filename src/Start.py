import setup_data as sd
from help_functions import save_properties
from intro_window import IntroWindow

if __name__ == '__main__':
    sd.setup_all_data()
    save_properties()
    IntroWindow()
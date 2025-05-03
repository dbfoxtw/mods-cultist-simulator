import customtkinter as ctk
from main_model import MainModel
from main_view import MainView
from main_presenter import MainPresenter

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    model = MainModel()
    presenter = MainPresenter(model, None)
    view = MainView(root, presenter)
    presenter.view = view
    presenter.load_app_settings()
    root.mainloop()

if __name__ == "__main__":
    main()

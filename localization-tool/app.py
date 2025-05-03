import tkinter as tk
from model import MainModel
from view import MainView
from presenter import MainPresenter

def main():
    root = tk.Tk()
    model = MainModel()
    presenter = MainPresenter(model, None)  # 先建 presenter，再綁 view
    view = MainView(root, presenter)
    presenter.view = view  # 反向注入 view（避免循環依賴）
    root.mainloop()

if __name__ == "__main__":
    main()

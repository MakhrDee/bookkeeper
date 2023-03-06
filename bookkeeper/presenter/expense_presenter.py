class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_data = exp_repo.get_all()
        self.cat_data = cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def show(self):
        self.view.show()
        self.view.set_expense_table(self.exp_data)
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self):
        print(123)

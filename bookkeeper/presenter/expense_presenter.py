from bookkeeper.models.expense import Expense
from typing import Any


class ExpensePresenter:

    def __init__(self, model: Any, view: Any, cat_repo: Any, exp_repo: Any) -> None:
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = None
        self.cat_data = cat_repo.get_all()
        # implement update_cat_data()
        # similar to update_expense_data()
        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked)
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked)
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked)

    def update_expense_data(self) -> None:
        self.exp_data = self.exp_repo.get_all()
        for e in self.exp_data:
            for c in self.cat_data:
                if c.pk == e.category:
                    e.category = c.name
                    break
        self.view.set_expense_table(self.exp_data)

    def show(self) -> None:
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        exp = Expense(amount=int(round(amount)), category=cat_pk, comment=str(comment))
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_expense_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_expenses()
        if selected:
            for e in selected:
                self.exp_repo.delete(e)
            self.update_expense_data()

    def handle_category_edit_button_clicked(self) -> None:
        self.view.show_cats_dialog(self.cat_data)

from pysuperfaktura.exceptions import SFAPIException

class SFExpenseItem:
    """

    """

    def __init__(self, params):
        """

        """
        self.params = params


class SFExpense:
    def __init__(self, client, params, items=None):
        self.client = client
        self.params = params
        self.items = items

    def add_item(self, item):
        """
        @param item:SFExpenseItem instance
        """
        if not isinstance(SFExpenseItem, item):
            raise SFAPIException('Passed object is not a SFExpenseItem instance')

        if self.items:
            self.items.append(item)
        else:
            self.items = [item]


class SFExpenseClient:
    def __init__(self, params):
        self.params = params
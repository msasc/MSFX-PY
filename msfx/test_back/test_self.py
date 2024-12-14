
class Column:
    def __init__(self):
        self.table = None

    def set_table(self, table):
        self.table = table

class Table:
    def __init__(self):
        self.columns = []
    def add_column(self, column):
        column.set_table(self)
        self.columns.append(column)

col = Column()
tab = Table()
tab.add_column(col)
print(tab.columns)

class TextElement:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def __str__(self):
        return f"Text: '{self.text}'\nFont: {self.font}"
    
    def set_text(self, text):
        self.text = text
        
    def set_font(self, font):
        self.font = font


class ImageElement(TextElement):
    pass


class TableElement:
    def __init__(self, data=None):
        if data is None:
            self.data = []
        else:
            self.data = data
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0]) if self.data else 0

    def __str__(self):
        table_str = ""
        for row in self.data:
            row_str = "| " + " | ".join(str(item) for item in row) + " |"
            table_str += row_str + "\n"
        return table_str

    def add_row(self, row):
        if len(row) != self.num_cols and self.num_cols != 0:
            raise ValueError("Row length does not match the number of columns in the table.")
        self.data.append(row)
        self.num_rows += 1
        if self.num_cols == 0:  # This handles adding the first row to an empty table.
            self.num_cols = len(row)

    def add_column(self, column):
        if len(column) != self.num_rows:
            raise ValueError("Column length must match the number of rows in the table.")
        for i in range(self.num_rows):
            self.data[i].append(column[i])

    def get_value(self, row, col):
        if row >= self.num_rows or col >= self.num_cols:
            raise IndexError("Row or column index out of bounds.")
        return self.data[row][col]

    def set_value(self, row, col, value):
        if row >= self.num_rows or col >= self.num_cols:
            raise IndexError("Row or column index out of bounds.")
        self.data[row][col] = value

    def insert_row(self, index, row):
        if len(row) != self.num_cols:
            raise ValueError("Row length does not match the number of columns.")
        self.data.insert(index, row)
        self.num_rows += 1

    def insert_column(self, index, column):
        if len(column) != self.num_rows:
            raise ValueError("Column length must match the number of rows.")
        for i in range(self.num_rows):
            self.data[i].insert(index, column[i])
        self.num_cols += 1

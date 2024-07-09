from prettytable import PrettyTable

# Create a PrettyTable object
table = PrettyTable()

# Define the column names
table.field_names = ["Name", "Age", "City"]

# Add rows to the table
table.add_row(["Alice", 30, "New York"])
table.add_row(["Bob", 25, "Los Angeles"])
table.add_row(["Charlie", 35, "Chicago"])

# Print the table
print(table)

print("Welcome to the Inventory Management System")

# Menu function
def menu():
    while True:
        print("Select Menu:")
        print("1: Product Management")
        print("2: Order Processing")
        print("3: Generating Reports")
        print("4: Exit")  # Option to exit the menu
        
        try:
            select_menu = int(input("Enter number for the menu (1, 2, 3, or 4): "))
            
            # Debugging statement to check what input is being received
            print(f"DEBUG: You entered '{select_menu}'")
            
            if select_menu == 1:
                print("Welcome to Product Management System")
                product_management()
            elif select_menu == 2:
                print("Welcome to Order Processing System")
                order_processing()
            elif select_menu == 3:
                print("Welcome to Generating Report System")
                orders = [
                {'product_name': 'Product A', 'sales_amount': 100, 'units_sold': 5, 'date': '2024-07-01'},
                {'product_name': 'Product B', 'sales_amount': 150, 'units_sold': 3, 'date': '2024-07-02'},
                {'product_name': 'Product A', 'sales_amount': 120, 'units_sold': 4, 'date': '2024-07-03'}
]

                generating_reports(orders, '2024-07-01', '2024-07-03') 
            elif select_menu == 4:
                print("Exiting the menu. Goodbye!")
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, 3, or 4).")

products = []

def add_product(p_id, name, price, stock):
    product = {
        'p_id': p_id,
        'name': name,
        'price': price,
        'stock': stock
    }
    products.append(product)
    print(f"Product {name} added successfully.")

def update_product(p_id, price=None, stock=None):
    for product in products:
        if product['p_id'] == p_id:
            if price is not None:
                product['price'] = price      
            if stock is not None:
                product['stock'] = stock
            print(f"Product ID {p_id} updated successfully.")
            return
    print("Product ID not found.")

def display_products():
    if not products:
        print("No products available.")
    else:
        for product in products:
            print(f"Product ID: {product['p_id']}")
            print(f"Name: {product['name']}") 
            print(f"Price: {product['price']}") 
            print(f"Stock: {product['stock']}")  
            print("------")

def product_management():
    while True:
        print("\nProduct Management Menu")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Display Products")
        print("4. Exit")
        
        choice = input("Select from the above menu: ")
        
        if choice == "1":
            p_id = int(input("Enter the product ID: "))
            name = input("Enter the product name: ")
            price = float(input("Enter the product price: "))
            stock = int(input("Enter the product stock: "))
            add_product(p_id, name, price, stock)
        elif choice == "2":
            p_id = int(input("Enter the product ID to update: "))        
            price = input("Enter new product price (or leave blank to keep previous price): ")
            stock = input("Enter new product stock (or leave blank to keep previous stock): ")
            update_product(p_id, float(price) if price else None, int(stock) if stock else None)
        elif choice == "3":
            display_products()
        elif choice == "4":
            print("Exiting Product Management...")
            break
        else:
            print("Invalid choice. Please try again.")


# order processing
def order_processing():
   
    p_id=int(input("Enter product ID: "))
    quantity=int(input("Enter product Quantity"))

    for product in products:
        if product['p_id']==p_id:
            if product['stock'] >= quantity:
               product['stock']-=quantity
               print("Your order is confirmed")
               Total=quantity*product['price']
               print(f"Order summary is: Your order for {quantity} {product['name']} per product ${product['price']} with the total amount of {Total} is confirmed")           


            else:
                print("insufficient stock")
        
    
def generating_reports(orders, s_date, e_date):
    print("Generating Sales Report....")
    total_sale=0
    total_units=0
    product_counts={}
    for order in orders:
        total_sale+=order['sales_amount']
        total_units+=order['units_sold']
        order_date=order['date']
        if s_date<=order_date<=e_date:
            product_name=order['product_name']
            if product_name in product_counts:
                product_counts[product_name]+=1
            else:
                product_counts[product_name]=1
    print(f"Total sales{total_sale}")
    print(f"Total units sold: {total_units}") 
              

    
# Call the menu function
menu()

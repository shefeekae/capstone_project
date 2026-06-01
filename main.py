from fastapi import FastAPI
from models import Product

app = FastAPI() 


@app.get("/")
def greet():
    return "Welcome to Python Shefeek"


products = [
    Product(id =1,name ="Phone",description = "Budget Phone",price = 99.99,quantity = 10),
    Product(id =2,name ="Laptop",description = "Gaming Laptop",price = 199.99,quantity = 5),
    Product(id =3,name ="Keyboard",description = "Mechanical keyboard",price = 49.99,quantity = 2),
]

@app.get("/products")
def get_all_products():
    return products


@app.get("/product/{id}")
def get_product_by_id(id:int):
    
    for product in products:
        if product.id == id:
            return product
    
    return "Product not found" 

@app.post("/product")
def add_product(product : Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id:int, product:Product):
    for i in range(len(products)):
        if(products[i].id == id):
            products[i] = product
            return "Product Added Successfully" 
    return "No Product found"    

@app.delete("/product")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id ==id:
            del products[i]
            return "Product deleted"
        
    return "Product not found"
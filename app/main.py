from fastapi import Depends, FastAPI
from app.models.models import Product
from app.database.database import session,engine
import app.models.database_models as database_models
from sqlalchemy.orm import Session
import logging

logging.basicConfig(
    filename="app.log",   # log file name
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI() 

database_models.Base.metadata.create_all(bind = engine)
logger.info("Database tables created")



products = [
    Product(id =1,name ="Phone",description = "Budget Phone",price = 99.99,quantity = 10),
    Product(id =2,name ="Laptop",description = "Gaming Laptop",price = 199.99,quantity = 5),
    Product(id =3,name ="Keyboard",description = "Mechanical keyboard",price = 49.99,quantity = 2),
]


def get_db():
    db = session()
    try:
        logger.info("Database session opened")
        yield db
    finally:
        logger.info("Database session closed")
        db.close()    


def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        logger.info("Initializing default products")

        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    
        db.commit()
        logger.info("Products inserted successfully")
    else:
        logger.info("Products already exist")

init_db() 

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    logger.info("Fetching all products")

    db_products = db.query(database_models.Product).all()

    logger.info(f"{len(db_products)} products retrieved")

    return db_products


@app.get("/product/{id}")
def get_product_by_id(id:int,db: Session = Depends(get_db)):

    logger.info(f"Searching for product ID {id}")

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
            logger.info(f"Product found: {db_product.name}")   
            return db_product
    
    logger.warning(f"Product ID {id} not found")
    return "Product not found" 

@app.post("/product")
def add_product(product : Product,db: Session = Depends(get_db)):

    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product")
def update_product(id:int, product:Product,db: Session = Depends(get_db)):
   
   logger.info(f"Updating product ID {id}")

   db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
   if db_product:
      db_product.name = product.name
      db_product.description = product.description
      db_product.price = product.price
      db_product.quantity = product.quantity
      db.commit()
      logger.info(f"Product ID {id} updated") 
      return "Product Updated Successfully" 
   else:
    logger.warning(f"Product ID {id} not found for update") 
    return "No Product found"    

@app.delete("/product")
def delete_product(id:int,db: Session = Depends(get_db)):
  logger.info(f"Deleting product ID {id}")

  db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
  if db_product:
     db.delete(db_product)
     db.commit()
     logger.info(f"Product ID {id} deleted")
     return "Product deleted"
  else:
    logger.warning(f"Product ID {id} not found for deletion")
    return "Product not found"
from fastapi import FastAPI
import uvicorn
import models.models as models
from router import product_route, seller_route, login_route
from database.database import engine

app = FastAPI(
    title = "Products API",
    description = "Get details of products and sellers on our website",
    terms_of_service = "https://www.google.com",
    contact = {
        "Developer name" : "Pravin Yadav",
        "Website" : "https://www.google.com",
        "Email" : "pravinyadav5959@gmail.com"
    },
    license_info = {
        "name" : "MIT@L234",
        "url" : "https://www.google.com"
    }
)

models.Base.metadata.create_all(engine)

app.include_router(product_route.router)
app.include_router(seller_route.router)
app.include_router(login_route.router)

@app.get('/', tags = ["Home"])
def home_page():
    return {"Welcome to Product Seller Home-Page"}

if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port = 8000)
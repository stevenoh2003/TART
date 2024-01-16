from api_util import delete_product, add_product

# URL of your Flask API endpoint
api_url = "http://127.0.0.1:5000/"

# Example product data
product_data = [

    {
        "name": "Vinegar",
        "location_x": 1,
        "location_y": 1,
        "price": 300.0,
        "expiration_date": "2026-12-31"

    },

    {
        "name": "Chicken",
        "location_x": 1,
        "location_y": 2,
        "price": 400.0,
        "expiration_date": "2024-1-31"

    },

    {
        "name": "Beef",
        "location_x": 2,
        "location_y": 1,
        "price": 800.0,
        "expiration_date": "2024-1-27"

    }


]


for product in product_data:
    add_product(api_url, product)

# delete_product(api_url, "test")
import requests

BASE_URL = "http://localhost:5000/api/products"  # Update this if your URL is different

def test_get_product_by_id():
    response = requests.get(f"{BASE_URL}/1")  # Assuming you want to get the product with ID 1
    assert response.status_code == 200
    print("GET by ID test passed")

def test_get_product_by_name():
    response = requests.get(f"{BASE_URL}/name/product_name")  # Replace 'product_name' with a valid name
    assert response.status_code == 200
    print("GET by name test passed")

def test_get_price_by_name():
    response = requests.get(f"{BASE_URL}/price/product_name")  # Replace 'product_name'
    assert response.status_code == 200
    print("GET price by name test passed")

def test_update_product():
    data = {'price': 20.99}  # Example data to update
    response = requests.put(f"{BASE_URL}/update/product_name", json=data)  # Replace 'product_name'
    assert response.status_code == 200
    print("Update product test passed")

def test_delete_product():
    response = requests.delete(f"{BASE_URL}/delete/product_name")  # Replace 'product_name'
    assert response.status_code == 200
    print("Delete product test passed")

def test_get_location_by_name():
    response = requests.get(f"{BASE_URL}/location/product_name")  # Replace 'product_name'
    assert response.status_code == 200
    print("GET location by name test passed")

if __name__ == "__main__":
    test_get_product_by_id()
    test_get_product_by_name()
    test_get_price_by_name()
    test_update_product()
    test_delete_product()
    test_get_location_by_name()

import requests
import json

def delete_product(api_url, product_name):
    url = f"{api_url}/delete/{product_name}"
    response = requests.delete(url)

    if response.status_code == 200:
        print(f"Product '{product_name}' deleted successfully.")
    elif response.status_code == 404:
        print(f"Product '{product_name}' not found.")
    else:
        print(f"Failed to delete product. Status code: {response.status_code}")
        print("Response:", response.text)

def add_product(url, product_data):
    url += "add"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(product_data), headers=headers)

    try:
        response_data = response.json()
    except json.decoder.JSONDecodeError:
        response_data = response.text

    if response.status_code == 201:
        print("Product added successfully.")
    else:
        print("Failed to add product. Status code:", response.status_code)
        print("Response:", response_data)



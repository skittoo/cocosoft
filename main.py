from flask import Flask, request, jsonify
from system_db import CarHiringSystemDatabase

app = Flask(__name__)

db_client = CarHiringSystemDatabase(
                db="car-hire",
                host="127.0.0.1",
                port= 5432, 
                user="postgres",
                password="root"
            )

# Endpoint for adding a new customer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    db_client.add_customer(name, phone_number, email)
    new_customer_id = db_client.get_latest_customer_id()
    return jsonify({'customer_id': new_customer_id}), 201

# Endpoint for updating an existing customer
@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    db_client.update_customer(customer_id, name, phone_number, email)
    return '', 204

# Endpoint for deleting an existing customer
@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db_client.delete_customer(customer_id)
    return '', 204

# Endpoint for getting an existing customer
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db_client.get_customer(customer_id)
    if customer:
        return jsonify({
            "customer_id": customer_id,
            "name": customer[0],
            "phone_number": customer[1],
            "email": customer[2]
        })
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Run the application
if __name__ == '__main__':
    db_client.create_all_tables()
    app.run(debug=True)

import os
import psycopg2
import requests
from dotenv import load_dotenv 
from flask import Flask, request, jsonify
from models import Destination, Itinerary, Expense
from flask_swagger_ui import get_swaggerui_blueprint
# Load environment variables from a .env file
load_dotenv()

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json' 
app = Flask(__name__)
url = os.getenv("DBURL")
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


# Connect to the PostgreSQL database
connection = psycopg2.connect(url)
 

# Define the route to get weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')  # Get the location from the request

    # Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key
    api_key = '9889d1c207146349f199645bad7f13c6'

    # Define the OpenWeatherMap API URL with the location and API key
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    try:
        # Make the API request to get weather data
        response = requests.get(weather_url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            # Extract relevant weather information from the response
            weather_data = {
                'location': location,
                'temperature': data['main']['temp'],
                'condition': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }

            return jsonify(weather_data), 200
        else:
            return jsonify({'error': 'Weather data not found'}), 404

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching weather data'}), 500




@app.route('/')
def hello():
    return "Welcome to the Wanderlust Travel Planner API!"
# Define a route for adding destinations
@app.route('/destinations', methods=['POST'])
def create_destination():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO destinations (name, description, location) VALUES (%s, %s, %s) RETURNING id;",
                           (name, description, location))
            destination_id = cursor.fetchone()[0]

    return jsonify({'message': 'Destination added successfully', 'id': destination_id}), 201
# Define a route for getting all destinations
@app.route('/destinations', methods=['GET'])
def get_destinations():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM destinations")
            destinations = cursor.fetchall()

    destination_list = [Destination(dest[0], dest[1], dest[2], dest[3]) for dest in destinations]

    return jsonify([destination.__dict__ for destination in destination_list])

@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM destinations WHERE id = %s;", (destination_id,))
            destination = cursor.fetchone()

    if not destination:
        return jsonify({'message': 'Destination not found'}), 404

    destination_obj = Destination(destination[0], destination[1], destination[2], destination[3])
    return jsonify(destination_obj.__dict__)

@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination(destination_id, data.get('name'), data.get('description'), data.get('location'))

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE destinations SET name = %s, description = %s, location = %s WHERE id = %s;",
                           (destination.name, destination.description, destination.location, destination_id))

    return jsonify({'message': 'Destination updated successfully'})

@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM destinations WHERE id = %s;", (destination_id,))

    return jsonify({'message': 'Destination deleted successfully'})








# Create an itinerary (POST `/itineraries`)
@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.get_json()
    destination_id = data.get('destination_id')
    activity = data.get('activity')

    # Check if the destination_id exists in the destinations table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM destinations WHERE id = %s;", (destination_id,))
            existing_destination = cursor.fetchone()

    if not existing_destination:
        return jsonify({'error': 'Destination not found'}), 404

    # If the destination exists, proceed to create the itinerary
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO itineraries (destination_id, activity) VALUES (%s, %s) RETURNING id;",
                           (destination_id, activity))
            itinerary_id = cursor.fetchone()[0]

    return jsonify({'message': 'Itinerary added successfully', 'id': itinerary_id}), 201


# Get all itineraries for a specific destination (GET `/itineraries/destination/<int:destination_id>`)
@app.route('/itineraries/destination/<int:destination_id>', methods=['GET'])
def get_itineraries(destination_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM itineraries WHERE destination_id = %s;", (destination_id,))
            itineraries = cursor.fetchall()

    itinerary_list = [Itinerary(itin[0], itin[1], itin[2]) for itin in itineraries]

    return jsonify([itinerary.__dict__ for itinerary in itinerary_list])

# Get a specific itinerary (GET `/itineraries/<int:itinerary_id>`)
@app.route('/itineraries/<int:itinerary_id>', methods=['GET'])
def get_itinerary(itinerary_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM itineraries WHERE id = %s;", (itinerary_id,))
            itinerary = cursor.fetchone()

    if not itinerary:
        return jsonify({'message': 'Itinerary not found'}), 404

    itinerary_obj = Itinerary(itinerary[0], itinerary[1], itinerary[2])
    return jsonify(itinerary_obj.__dict__)

# Update a specific itinerary (PUT `/itineraries/<int:itinerary_id>`)
@app.route('/itineraries/<int:itinerary_id>', methods=['PUT'])
def update_itinerary(itinerary_id):
    data = request.get_json()
    itinerary = Itinerary(itinerary_id, data.get('destination_id'), data.get('activity'))

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE itineraries SET destination_id = %s, activity = %s WHERE id = %s;",
                           (itinerary.destination_id, itinerary.activity, itinerary_id))

    return jsonify({'message': 'Itinerary updated successfully'})

# Delete a specific itinerary (DELETE `/itineraries/<int:itinerary_id>`)
@app.route('/itineraries/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM itineraries WHERE id = %s;", (itinerary_id,))

    return jsonify({'message': 'Itinerary deleted successfully'})
















@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    destination_id = data.get('destination_id')
    expense_category = data.get('expense_category')
    amount = data.get('amount')

    # Check if the destination_id exists in the destinations table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM destinations WHERE id = %s;", (destination_id,))
            existing_destination = cursor.fetchone()

    if not existing_destination:
        return jsonify({'error': 'Destination not found'}), 404

    # If the destination exists, proceed to create the expense
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO expenses (destination_id, expense_category, amount) VALUES (%s, %s, %s) RETURNING id;",
                           (destination_id, expense_category, amount))
            expense_id = cursor.fetchone()[0]

    return jsonify({'message': 'Expense added successfully', 'id': expense_id}), 201

# Get all expenses for a specific destination (GET `/expenses/<int:destination_id>`)
# Get all expenses for a specific destination (GET `/expenses/destination/<int:destination_id>`)
@app.route('/expenses/destination/<int:destination_id>', methods=['GET'])
def get_expenses_by_destination(destination_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE destination_id = %s;", (destination_id,))
            expenses = cursor.fetchall()

    expense_list = [Expense(expense[0], expense[1], expense[2], expense[3]) for expense in expenses]

    return jsonify([expense.__dict__ for expense in expense_list])

# Get a specific expense (GET `/expenses/<int:expense_id>`)
@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense_by_id(expense_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE id = %s;", (expense_id,))
            expense = cursor.fetchone()

    if not expense:
        return jsonify({'error': 'Expense not found'}), 404

    expense_obj = Expense(expense[0], expense[1], expense[2], expense[3])
    return jsonify(expense_obj.__dict__)


# Update a specific expense (PUT `/expenses/<int:expense_id>`)
@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense(expense_id, data.get('destination_id'), data.get('expense_category'), data.get('amount'))

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE expenses SET destination_id = %s, expense_category = %s, amount = %s WHERE id = %s;",
                           (expense.destination_id, expense.expense_category, expense.amount, expense_id))

    return jsonify({'message': 'Expense updated successfully'})

# Delete a specific expense (DELETE `/expenses/<int:expense_id>`)
@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM expenses WHERE id = %s;", (expense_id,))

    return jsonify({'message': 'Expense deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)

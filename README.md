#  Wanderlust Travel Planner API [ Flask ][![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
## Overview

Wanderlust Travel Planner is a web application for travelers to plan their trips more effectively. It provides features to create, manage, and track travel destinations, itineraries, and expenses for each trip. The application is built using Python and Flask for the backend, PostgreSQL for the database, and provides RESTful API endpoints for various actions.

### Backend Deploy
#-[Live Backend](https://wanderlust-travel-planne.vercel.app/)    

#-[Live Swagger API Documentation](https://wanderlust-travel-planne.vercel.app/api/docs/)

### API Documentation
## Viewing the Swagger API Documentation Local

After running the `app.py` file, you can access the Swagger API documentation by following these steps:

1. Make sure the application is running.

2. Open your web browser.

3. Visit the following URL:
4.  http://127.0.0.1:5000/api/docs/

## .env

Before running the application, make sure to set the following environment variables in a `.env` file in the project root directory:

```
DBURL=your_POSTGRES_connection_url
```
## Installation
   ```bash
  git clone https://github.com/bethimanideep/Wanderlust-Travel-Planne.git
  cd Wanderlust-Travel-Planne
  pip install -r requirements.txt
  python app.py
   ```

## Database Tables

The application uses three database tables to store data: `destinations`, `itineraries`, and `expenses`. Each table has its own structure.

### Destination Model

The `destinations` table stores information about travel destinations, including:

- `id` (Serial, Primary Key): The unique identifier for each destination.
- `name` (Text): The name of the destination.
- `description` (Text): A description or notes about the destination.
- `location` (Text): The location or address of the destination.

### Itinerary Model

The `itineraries` table stores itinerary items for each destination, including:

- `id` (Serial, Primary Key): The unique identifier for each itinerary item.
- `destination_id` (Integer): The ID of the associated destination.
- `activity` (Text): A description of the activity or plan for the day.

### Expense Model

The `expenses` table stores expense records for each destination, including:

- `id` (Serial, Primary Key): The unique identifier for each expense record.
- `destination_id` (Integer): The ID of the associated destination.
- `expense_category` (Text): The category or type of expense.
- `amount` (Float): The amount spent.


## Endpoints

### Destinations

- **POST /destinations:** Create a new destination.
- **GET /destinations:** Retrieve a list of all destinations.
- **GET /destinations/:destination_id:** Retrieve information about a specific destination.
- **PUT /destinations/:destination_id:** Update an existing destination.
- **DELETE /destinations/:destination_id:** Delete a destination.

### Itineraries

- **POST /itineraries:** Create a new itinerary item for a specific destination.
- **GET /itineraries/destination/:destination_id:** Retrieve all itinerary items for a specific destination.
- **GET /itineraries/:itinerary_id:** Retrieve information about a specific itinerary item.
- **PUT /itineraries/:itinerary_id:** Update an existing itinerary item.
- **DELETE /itineraries/:itinerary_id:** Delete an itinerary item.

### Expenses

- **POST /expenses:** Create a new expense record for a specific destination.
- **GET /expenses/:destination_id:** Retrieve all expense records for a specific destination.
- **GET /expenses/:expense_id:** Retrieve information about a specific expense record.
- **PUT /expenses/:expense_id:** Update an existing expense record.
- **DELETE /expenses/:expense_id:** Delete an expense record.


### Contact Information

For any queries and feedback, please contact me at [bethimanideep@gmail.com](mailto:bethimanideep@gmail.com).

---

<h1 align="center">✨Thank You✨</h1>

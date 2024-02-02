# Khakaton Weather Application

## Weather prediction server

Follow the steps below to set up and run the weather prediction server:

### Clone the Repository

Clone this repository to your local machine:

```
git clone <repository_url>
cd khakaton-weather
```

### Create an API Key

You will need your own API key from OpenWeatherMap with a Medium plan to access Historical APIs. Once you have the API key, create a .env file in the root directory of the project and add your API key to it. Here's an example of the .env file:

```
API_WEATHER="YOUR OPENWEATHER API KEY"
```

### Install Python Dependencies

Navigate to the backend directory and install the required Python libraries using pip:

```
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Server

To start the server, run the following command:

```
uvicorn app.main:app --reload
```

The server should now be running locally, and you can access it at the specified address (http://localhost:8000).

## Weather prediction client server

Follow the steps below to set up and run the weather prediction client server:

### Install Node.js packages

Navigate to the frontend directory and install the required Node.js packages by running:

```
cd frontend/
npm install
```

### Run the Client

Start the frontend development server:

```
npm run dev
```

### Create an API Key

Set .env file with GEOAPIFY API Key:

```
VITE_GEO_API="YOUR GEOAPIFY API KEY"
```

### Access the application

Open your browser and visit `http://localhost:5173/` to view the application.

## Integration Tests

To run integration tests, use the following command:

```
python tests\integration\test_weather_prediction_api.py
```

## Unit Tests

To run unit tests, execute the following command:

```
python -m unittest your-path\khakaton-weather\tests\unit\test_get_weather_prediction.py
```

## Made by Bees team.

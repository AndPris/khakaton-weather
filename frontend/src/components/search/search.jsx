import "@geoapify/geocoder-autocomplete/styles/minimal.css";
import {
  GeoapifyContext,
  GeoapifyGeocoderAutocomplete,
} from "@geoapify/react-geocoder-autocomplete";
import "bootstrap/dist/css/bootstrap.css";
import { useCallback, useEffect, useState } from "react";
import { Audio } from "react-loader-spinner";
import styles from "./search.module.css";

const API_KEY = import.meta.env.VITE_GEO_API;

const Search = () => {
  const [coords, setCoords] = useState([0, 0]);
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchWeatherData = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/get_weather_prediction?lon=${coords[0]}&lat=${coords[1]}`
      );
      if (!response.ok) throw new Error("Failed to fetch data");
      const jsonData = await response.json();
      setWeatherData(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  }, [coords]);

  const handlePlaceSelect = (value) => {
    if (value) setCoords(value.geometry.coordinates);
  };

  useEffect(() => {
    if (coords[0] !== 0 && coords[1] !== 0) {
      fetchWeatherData();
    }
  }, [coords, fetchWeatherData]);

  return (
    <div className="container w-75 text-center">
      <div className={styles.inner}>
        <GeoapifyContext apiKey={API_KEY}>
          <GeoapifyGeocoderAutocomplete
            placeholder="Enter address here"
            placeSelect={handlePlaceSelect}
          />
        </GeoapifyContext>
      </div>
      {isLoading ? (
        <div className="d-flex w-100 justify-content-center">
          <Audio
            height={80}
            width={80}
            radius={9}
            color="blue"
            ariaLabel="loading"
            wrapperStyle
            wrapperClass
          />
        </div>
      ) : weatherData ? (
        <WeatherTable weatherData={weatherData} />
      ) : (
        <h3>Enter your city</h3>
      )}
    </div>
  );
};

const WeatherTable = ({ weatherData }) => {
  return (
    <div className="d-flex gap-3">
      <table className="table table-primary table-striped w-25">
        <thead className="fw-bold">
          <tr>
            <td colSpan="2">Time of the Day</td>
          </tr>
        </thead>
        <tbody>
          <tr className="fw-medium">
            <td className="p-1">Time</td>
          </tr>
          <tr className="fw-medium">
            <td className="p-1">Temperature (°C)</td>
          </tr>
          <tr className="fw-medium">
            <td className="p-1">Feels Like (°C)</td>
          </tr>
          <tr className="fw-medium">
            <td className="p-1">Pressure (hPa)</td>
          </tr>
          <tr className="fw-medium">
            <td className="p-1">Wind Speed (m/s)</td>
          </tr>
          <tr className="fw-medium">
            <td className="p-1">Humidity (%)</td>
          </tr>
        </tbody>
      </table>
      <table className="table table-info table-striped w-100">
        <thead className="fw-bold">
          <tr>
            <td colSpan="2">🌃Night🌃</td>
            <td colSpan="2">🌅Morning🌅</td>
            <td colSpan="2">☀️Day☀️</td>
            <td colSpan="2">🌙Evening🌙</td>
          </tr>
        </thead>
        <tbody>
          <tr className="fw-medium">
            {weatherData.date.map((date, index) => (
              <td className="p-1" key={index}>
                {new Date(date).getHours()}:00
              </td>
            ))}
          </tr>
          <tr className="temperature fs-5">
            {weatherData.temp.map((temperature, index) => (
              <td className="p-1" key={index}>
                {Math.round(temperature)}°
              </td>
            ))}
          </tr>
          <tr className="temperature-feels text-secondary">
            {weatherData.feels_like.map((temperature, index) => (
              <td className="p-1" key={index}>
                {Math.round(temperature)}°
              </td>
            ))}
          </tr>
          <tr className="pressure text-secondary">
            {weatherData.pressure.map((pressure, index) => (
              <td className="p-1" key={index}>
                {Math.round(pressure)}
              </td>
            ))}
          </tr>
          <tr className="wind-speed">
            {weatherData.speed.map((speed, index) => (
              <td className="p-1" key={index}>
                {speed.toFixed(2)}
              </td>
            ))}
          </tr>
          <tr className="humidity">
            {weatherData.humidity.map((humidity, index) => (
              <td className="p-1" key={index}>
                {Math.round(humidity, 2)}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Search;

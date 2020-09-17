sample_city_ids = [3439525, 3439781, 3440645, 3442098, 688, 3442778]

# ID '688' does not exist, so we do not include it, simulating OpenWeather API behavior
sample_result = {
    "cnt": 5,
    "list": [
        {
            "coord": {
                "lon": -57.63,
                "lat": -32.68
            },
            "sys": {
                "country": "UY",
                "timezone": -10800,
                "sunrise": 1600249652,
                "sunset": 1600292585
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 21.67,
                "feels_like": 19.83,
                "temp_min": 21.67,
                "temp_max": 21.67,
                "pressure": 1016,
                "humidity": 40
            },
            "visibility": 10000,
            "wind": {
                "speed": 1.79,
                "deg": 225
            },
            "clouds": {
                "all": 0
            },
            "dt": 1600287170,
            "id": 3439525,
            "name": "Young"
        },
        {
            "coord": {
                "lon": -54.38,
                "lat": -33.23
            },
            "sys": {
                "country": "UY",
                "timezone": -10800,
                "sunrise": 1600248879,
                "sunset": 1600291798
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 18.72,
                "feels_like": 17.39,
                "temp_min": 18.72,
                "temp_max": 18.72,
                "pressure": 1014,
                "sea_level": 1014,
                "grnd_level": 1007,
                "humidity": 68
            },
            "visibility": 10000,
            "wind": {
                "speed": 3.09,
                "deg": 180
            },
            "clouds": {
                "all": 0
            },
            "dt": 1600287170,
            "id": 3439781,
            "name": "Treinta y Tres"
        },
        {
            "coord": {
                "lon": -56.62,
                "lat": -34.45
            },
            "sys": {
                "country": "UY",
                "timezone": -10800,
                "sunrise": 1600249430,
                "sunset": 1600292322
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 16.75,
                "feels_like": 12.11,
                "temp_min": 15,
                "temp_max": 17.78,
                "pressure": 1016,
                "humidity": 59
            },
            "visibility": 10000,
            "wind": {
                "speed": 6.2,
                "deg": 180
            },
            "clouds": {
                "all": 9
            },
            "dt": 1600287170,
            "id": 3440645,
            "name": "Departamento de San José"
        },
        {
            "coord": {
                "lon": -56.22,
                "lat": -34.76
            },
            "sys": {
                "country": "UY",
                "timezone": -10800,
                "sunrise": 1600249338,
                "sunset": 1600292222
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 16.33,
                "feels_like": 11.6,
                "temp_min": 15,
                "temp_max": 17.78,
                "pressure": 1016,
                "humidity": 59
            },
            "visibility": 10000,
            "wind": {
                "speed": 6.2,
                "deg": 180
            },
            "clouds": {
                "all": 0
            },
            "dt": 1600287170,
            "id": 3442098,
            "name": "La Paz"
        },
        {
            "coord": {
                "lon": -56.39,
                "lat": -34.76
            },
            "sys": {
                "country": "UY",
                "timezone": -10800,
                "sunrise": 1600249379,
                "sunset": 1600292263
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 16.41,
                "feels_like": 11.7,
                "temp_min": 15,
                "temp_max": 17.78,
                "pressure": 1016,
                "humidity": 59
            },
            "visibility": 10000,
            "wind": {
                "speed": 6.2,
                "deg": 180
            },
            "clouds": {
                "all": 2
            },
            "dt": 1600287171,
            "id": 3442778,
            "name": "Delta del Tigre"
        }
    ]
}

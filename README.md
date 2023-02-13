# TRIPS API

## Introduction
Trips API is a public RESTful API that enables to load data from vehicle trips and perform some calculations over it.

# Project Support Features
* API endpoints to 
    - Load data from a remote CSV file
    - Get the average weekly trips in a specific region.
    - Get the average weekly trips in a specific area, delimited by its coordinates.
* Does not require authentication

## Installation Guide
* Clone this repository
* Run `docker compose up --build`

## API Endpoints
| HTTP Methods  | Endpoints                 | Action                                                                                    |
| ------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| POST          | /api/start_load           | Start the process to load the remote CSV file                                             |
| GET           | /api/status/{process_id}  | Get the status of the loading process                                                     |
| POST          | /api/trips                | Get the average weekly trips in a specific area, delimited by the specified coordinates   |
| GET           | /api/trips/{region}       | Get the average weekly trips in a specified region                                        |

## Examples
* Content type: "application/json". 
* Responses are JSON Objects. 

### Start Load Request
`POST http://localhost:5000/api/start_load`

### Request Body
```json
{
    "source": "S3",
    "url": "https://trips-api.s3.amazonaws.com/trips.csv"
}
```

### Response
```json
{
    "error": "",
    "message": "CSV file is being loaded into the database successfully.",
    "process_id": "bd28e6cf-5dec-4218-a641-1630c735640a",
    "status": "success"
}
```

### Status Request
`GET http://localhost:5000/api/status/bd28e6cf-5dec-4218-a641-1630c735640a`

### Response
```json
{
    "message": "CSV file is being loaded into the database successfully.",
    "process_id": "74c4bd28e6cf-5dec-4218-a641-1630c735640a",
    "ready": true,
    "successful": false
}
```

### Region Weekly Average Request
`GET http://localhost:5000/api/trips/Hamburg`

### Response
```json
{
    "error": "",
    "result": "5.6",
    "status": "success"
}
```

### Area Weekly Average Request
`POST http://localhost:5000/api/trips`

### Request Body
```json
{
    "min_lon": 14.1,
    "min_lat": 49.9,
    "max_lon": 14.9,
    "max_lat": 50.9
}
```

### Response
```json
{
    "error": "",
    "result": "6.8",
    "status": "success"
}
```


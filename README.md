# TraceAPI — API Reliability and Diagnostics Platform

TraceAPI is a Django REST Framework–based application for registering API endpoints, executing HTTP tests, recording test results, and analyzing API reliability through response metrics.

The project demonstrates REST API development, Django ORM operations, HTTP request handling, exception handling, database persistence, and a browser-based monitoring dashboard.

## Features

### Endpoint Management
- Register API endpoints with a name, path, and HTTP method.
- List and retrieve registered endpoints.
- Update or delete existing endpoints.
- Persist endpoint information using Django models and SQLite.

### API Testing
- Execute HTTP requests against registered endpoints.
- Measure request duration in milliseconds.
- Capture HTTP status codes and classify successful and failed requests.
- Handle connection failures where no HTTP response is received.
- Record test results for later analysis.

### Reliability Metrics
- Total number of test runs.
- Successful and failed run counts.
- Success rate as a percentage.
- Average response time in milliseconds.

### Demo Endpoints
TraceAPI includes controlled endpoints for testing different HTTP outcomes:

| Endpoint | Expected result |
|---|---|
| `/api/healthy/` | HTTP 200 — success |
| `/api/client-error/` | HTTP 400 — failure |
| `/api/server-error/` | HTTP 500 — failure |

Connection failures can also be tested internally to verify that errors are captured when a service cannot be reached.

### Web Dashboard
- View registered endpoints in a Bootstrap-styled table.
- Register endpoints through an HTML form.
- Use Django templates to render database records.

The dashboard is being developed alongside the REST API.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Django | Web framework and template rendering |
| Django REST Framework | REST API views and HTTP responses |
| Django ORM | Database queries and aggregation |
| SQLite | Persistent storage |
| Requests | Execute HTTP requests against test targets |
| Bootstrap 5 | Dashboard styling |
| HTML and Django Template Language | Dynamic dashboard interface |
| Git and GitHub | Version control and source hosting |

## Architecture

TraceAPI separates endpoint management, request execution, persistence, and presentation.

```text
Browser / API Client
        |
        v
Django URLs and Views
        |
        +-------------------+
        |                   |
        v                   v
Endpoint Management    Test Runner
        |                   |
        v                   v
   Endpoint Model       HTTP Request
        |                   |
        |                   v
        |             Test Result
        |                   |
        +---------+---------+
                  |
                  v
             SQLite DB
                  |
                  v
        Summary / Dashboard
```

### Core Components

- **Endpoint:** Stores endpoint name, path, HTTP method, and creation timestamp.
- **TestRun:** Stores the endpoint being tested, HTTP status code when available, success flag, response duration, error message, and creation timestamp.
- **EndpointSerializer:** Serializes and validates endpoint data for the REST API.
- **Test Runner:** Executes HTTP requests, measures elapsed time, catches request exceptions, and persists results.
- **Summary View:** Uses Django ORM aggregation to calculate reliability metrics.
- **Dashboard View:** Retrieves registered endpoints and renders them through a Django HTML template.

## Getting Started

### Prerequisites

- Python installed
- Git
- Internet access for loading Bootstrap from its CDN

### 1. Clone the repository

```bash
git clone https://github.com/k7n4l/Trace-API.git
cd Trace-API
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution-policy setting for your environment or activate the environment through your IDE.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install django djangorestframework requests
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

- Dashboard: http://127.0.0.1:8000/api/
- API root: http://127.0.0.1:8000/api/endpoints/

The dashboard route and API root are separate: `/api/` renders HTML, while `/api/endpoints/` provides the endpoint-management API.

## API Reference

The following routes are implemented in the project.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/endpoints/` | List registered endpoints |
| POST | `/api/endpoints/` | Register an endpoint |
| GET | `/api/endpoints/<id>/` | Retrieve an endpoint |
| PUT | `/api/endpoints/<id>/` | Replace an endpoint |
| PATCH | `/api/endpoints/<id>/` | Partially update an endpoint |
| DELETE | `/api/endpoints/<id>/` | Delete an endpoint |
| POST | `/api/endpoints/<id>/run/` | Execute a test and record the result |
| GET | `/api/endpoints/<id>/summary/` | Retrieve reliability metrics |
| GET | `/api/healthy/` | Simulate a successful response |
| GET | `/api/client-error/` | Simulate an HTTP 400 response |
| GET | `/api/server-error/` | Simulate an HTTP 500 response |

Replace `<id>` with the numeric ID of a registered endpoint.

### Register an endpoint

Example request body:

```json
{
  "name": "Healthy API",
  "path": "/api/healthy/",
  "method": "GET"
}
```

Send a `POST` request to `/api/endpoints/` with `Content-Type: application/json`.

### Run a test

Send a `POST` request to:

```text
/api/endpoints/1/run/
```

Example response:

```json
{
  "status_code": 200,
  "request_time_ms": 4.25,
  "success": true,
  "error_msg": ""
}
```

Response time varies by environment. Connection failures can return a `null` status code and a populated error message.

### Retrieve reliability metrics

Send a `GET` request to:

```text
/api/endpoints/1/summary/
```

Example response:

```json
{
  "endpoint_id": 1,
  "total_runs": 5,
  "successful_runs": 4,
  "failed_runs": 1,
  "success_rate": 80.0,
  "average_response_time_ms": 12.45
}
```

The values above are illustrative examples, not live measurements.

## How Reliability Metrics Are Calculated

**Success rate**

\[
\text{Success Rate} =
\frac{\text{Successful Runs}}{\text{Total Runs}} \times 100
\]

A run is classified as successful when the response status code is in the HTTP 200–299 range.

**Average response time**

The arithmetic mean of the recorded response times for an endpoint.

**Failure handling**

If a request raises a `requests` exception, TraceAPI records the failed run, elapsed time, and error message. When no HTTP response is received, the status code is stored as `null`.

## Database Models

### Endpoint

Stores the API endpoint configuration:

- `name`
- `path`
- `method`
- `created_at`

### TestRun

Stores the outcome of each test:

- `endpoint` — foreign key to `Endpoint`
- `status_code` — nullable integer
- `success` — Boolean
- `response_time_ms` — floating-point duration
- `error_msg` — error details when available
- `created_at`

The foreign key connects each test result to its endpoint. The `related_name="test_runs"` relationship also enables reverse access to an endpoint's test history.

## Testing Scenarios

| Scenario | Expected behavior |
|---|---|
| Successful request | Record a 2xx response and mark the run successful |
| Client error | Record HTTP 400 and mark the run failed |
| Server error | Record HTTP 500 and mark the run failed |
| Connection refused | Record no HTTP status code and capture the exception |
| Multiple test runs | Persist each result and update the summary metrics |

## Design Decisions

- **Django REST Framework generic views** reduce repetitive CRUD code.
- **Django ORM aggregation** calculates summary statistics in the database.
- **A separate test runner** keeps HTTP execution logic out of the API view.
- **SQLite** provides a lightweight database for local development.
- **Django templates and Bootstrap** provide a simple web interface without requiring a separate frontend application.

## Current Scope and Limitations

TraceAPI is an MVP intended to demonstrate API testing and reliability metrics.

- The project currently uses SQLite for local development.
- Request execution uses a configured local base URL and is intended for controlled local demo endpoints.
- Automated scheduling, background workers, notifications, and historical charts are not currently included.
- The current metrics endpoint provides aggregate statistics, while richer test-history presentation can be developed further.
- Production deployment would require additional security controls, configuration management, monitoring, and database setup.

## Future Improvements

- Scheduled endpoint checks.
- Configurable retry policies and timeouts.
- Response validation against expected payloads.
- Detailed test-history tables and charts.
- Endpoint health classification based on success rate and response time.
- Authentication and authorization for managing endpoints.
- MySQL support and production deployment.
- Strong URL validation and SSRF protection for any configurable test targets.

TraceAPI — making API behavior measurable through repeatable tests and reliability metrics.

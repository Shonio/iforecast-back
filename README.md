# Iforecast RESTFul API server

This project is a simple and user-friendly web application allowing users to securely log in and view their account information. The application uses JWT (JSON Web Token) authentication and provides secure access to users' account data. The backend is developed using Flask and Python 3.11. Data storage is managed using a MySQL database, and the application communicates with the frontend through RESTful API.

## Main Features

- Secure user authentication using JWT
- Access and refresh tokens for maintaining user sessions
- RESTful API for seamless frontend-backend communication
- Flask backend with MySQL database for data storage

## Installation

Follow these steps to install and run the project on your local machine:

### Prerequisites

- Python 3.11 or higher
- MySQL server

### Clone the Repository

```bash
git clone https://github.com/GreenTechCentre/iforecast-back.git
cd iforecast-back
```

### Backend Setup
1. Install a virtual environment for the Python project:
```bash
python3 -m venv venv
```
2. Activate the virtual environment:
```bash
source venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
4. Create a .env file in the root folder and add the following environment variables:
```bash
DATABASE_URL=mysql://username:password@localhost/database_name
JWT_SECRET_KEY=mysecretkey
```
Replace username, password, and database_name with your MySQL credentials and desired database name.
5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```
6. Run the application:
```bash
python run.py
```
The backend should now be running at http://localhost:5000.

## Testing

Run tests with:
```bash
pytest
```

## Linting

Run linting with:
```bash
pylint app
```

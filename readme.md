# E-commerce Platform Backend

This project is a backend for an e-commerce platform built using Django and Django Rest Framework (DRF). The backend supports user and admin functionalities, including authentication, product management, shopping cart, and order processing.

## Technology Stack

- Django
- Django Rest Framework (DRF)
- Celery
- Redis
- Docker
- MySQL
- Websockets

## Modules

1. Authentication
2. Products
3. Shopping Cart
4. Orders

## Project Setup Instructions

### Prerequisites

- Python 3.8+
- Docker
- Docker Compose
- Redis

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/anonymousip1234/ecommerce_with_drf.git
    cd ecommerce-backend
    ```

2. Set up a virtual environment and activate it:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a `.env` file in the project root directory and add the following environment variables:

    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost, 127.0.0.1

    DB_NAME=ecommerce
    DB_USER=root
    DB_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432

    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    ```

5. Run migration commands:
   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```

6. Run the Celery Worker:

    ```bash
    celery -A ecommerce worker -l info
    ```
7. Run the redis server:
    ```bash
    redis-server
    ```

#### Docker Setup Guide

1. Run the Docker containers:

    ```bash
    docker-compose up --build
    ```

2. Apply the database migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

3. Create a superuser:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

4. Run the development server:

    ```bash
    docker-compose exec web python manage.py runserver
    ```

The application should now be running at `http://localhost:8000`.

## API Documentation

### Authentication

- **Register a new user**: `POST /auth/register/`
    ```json
    {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    ```

- **Obtain a token**: `POST /auth/login/`
    ```json
    {
        "username": "testuser",
        "password": "testpassword"
    }
    ```
    Response:
    ```json
    {
        "access_token" : "access token",
    }
    ```

- **Refresh a token**: `POST /auth/token/refresh/`
    ```json
    {
        "refresh": "your-refresh-token"
    }
    ```

### Products

- **List all products**: `GET /api/products/`
- **Retrieve a product**: `GET /api/products/{id}/`
- **Create a new product**: `POST /api/products/` (Admin only)
- **Update a product**: `PUT /api/products/{id}/` (Admin only)
- **Delete a product**: `DELETE /api/products/{id}/` (Admin only)
- **Bulk upload products using celery**: `POST /api/bulk_upload/`
- **Websocket For live SKU calculation**: `r'ws/sold_skus/$'`
- **Search and filter products**: Use query parameters for filtering, searching, and ordering


### Shopping Cart

- **Add an item to the cart**: `POST /api/cart-items/`
    ```json
    {
        "product_id": 1,
        "quantity": 2
    }
    ```
- **Remove an item from the cart**: `DELETE /api/cart-items/{id}/`
- **Update an item in the cart**: `PUT /api/cart-items/{id}/`
    ```json
    {
        "quantity": 3
    }
    ```


### Orders

- **List all orders**: `GET /api/orders/`
- **Retrieve an order**: `GET /api/orders/{id}/`
- **Create a new order**: `POST /api/orders/`
    ```json
    {
        "cart_items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    ```
- **Delete an order**: `DELETE /api/orders/{id}/`
- **Update an order**: `PUT /api/orders/{id}/` (Admin only)
    ```json
    {
        "status": "shipped"
    }
    ```
- **Place order From Cart**: `POST /api/orders/place_order_from_cart_item/`
    ```json
    {
        "user": <user_id>,
        "cart_item": <cart_item_id>
    }



## Additional Information

- The project uses Celery for handling background tasks such as bulk product uploads and sending email notifications.
- JWT (JSON Web Token) is used for authentication.
- The application uses PostgreSql as the database, but it can be configured to use other databases by updating the environment variables and settings.
- Websockets are set up for real-time notifications but need further implementation for specific use cases.
- Test cases are Also set up for most of the major functionalities,to run the test cases,
   ```bash
      python manage.py test
   ```

## Assumptions Made

- Users must register and obtain a token to access the protected endpoints.
- Admin users have additional privileges such as managing products and updating orders.
- The project is set up to run in a Docker environment, but it can also be run locally with the necessary adjustments to the settings.

---

# Serasa Orders Project

This is a Django project for the Serasa orders.

## **Setup**

1. Clone the repository:
```bash
git clone https://github.com/Alexvjunior/serasa_orders.git
```

2. Navigate to the project directory:
```bash
cd serasa_orders
```

3. Build the Docker images:
```bash
docker-compose build
```

4. Start the containers:
```bash
docker-compose up -d
or
make run  
```


## **Running the Tests**

To run the tests, use the following command:
```bash
docker-compose exec web python manage.py test 
or
make test
```


## **Code Quality and Security**

To ensure code quality and enhance security, the following tools are integrated into the project:

### isort

[isort](https://pycqa.github.io/isort/) is a Python utility that sorts imports alphabetically and automatically separates them into sections.

To run isort and automatically format your imports, use the following command:

```bash
isort 
or
make format
```


### flake8

flake8 is a code linter that checks Python code for style and programming errors.

To run flake8 and check your code, use the following command:
```bash
flake8 apps
or 
make lint
```

### safety

safety is a command-line tool that checks your Python dependencies for known security vulnerabilities.

To run safety and check for vulnerabilities, use the following command:
```bash
safety check
or
make security
```


## **Swagger API Documentation**

The project includes Swagger for API documentation. After starting the containers, you can access the Swagger UI at [http://localhost:8080/docs/](http://localhost:8080/docs/).

## **Available Makefile Commands**
The project includes a Makefile with several useful commands:

- make lint: Run flake8 for linting the code.
- make test: Run pytest for running tests.
- make security: Perform a security check on the project dependencies using Safety.
- make run: Run the application using docker compose.
- make run-postgres: Run the postgres application using docker
- make run-redis: Run the redis application using docker
- make clean: Clean up the project by removing the virtual environment and cached files.


## **API Endpoints**
Listed below are all endpoints available in the API, along with the required payloads and expected responses.

### Endpoint 1: `/order/`
#### Descrição:
This endpoint allows you to create a new order.
#### Método HTTP:
`POST`

### Payload
```json
"user_id": 0,
"item_description": "string",
"item_quantity": 0,
"item_price": 0,
"total_value": 0,
```

### Resposta
```json
"id": 1,
"created": "string",
"modified": "string",
"user_id": 0,
"item_description": "string",
"item_quantity": 0,
"item_price": 0,
"total_value": 0,
```

### Endpoint 2: `/order/{id}`
#### Descrição:
Returns a specific Order
#### Método HTTP:
`GET`

### Resposta
```json
"id": 1,
"created": "string",
"modified": "string",
"user_id": 0,
"item_description": "string",
"item_quantity": 0,
"item_price": 0,
"total_value": 0,
```

### Endpoint 3: `/order/?limit=&offset=&cpf=`
#### Descrição:
Returns a list of orders. You can user cpf filter too.
#### Método HTTP:
`GET`

### Resposta
```json
"count": 1,
"next": "string",
"previous": "string",
"results":[
    {
        "id": 1,
        "created": "string",
        "modified": "string",
        "user_id": 0,
        "item_description": "string",
        "item_quantity": 0,
        "item_price": 0,
        "total_value": 0,
    }
]
```

### Endpoint 4: `/order/{id}`
#### Descrição:
Delete Order.
#### Método HTTP:
`DELETE`


### Endpoint 5: `/order/{id}`
#### Descrição:
Update order.
#### Método HTTP:
`PATCH`

### Payload
```json
"user_id": 0,
"item_description": "string",
"item_quantity": 0,
"item_price": 0,
"total_value": 0,
```

### Resposta
```json
"id": 1,
"created": "string",
"modified": "string",
"user_id": 0,
"item_description": "string",
"item_quantity": 0,
"item_price": 0,
"total_value": 0,
```

### Endpoint 6: `/token/`
#### Descrição:
Get Token system User.
#### Método HTTP:
`POST`

### Payload
```json
"username": "string",
"password": "string",
```

### Resposta
```json
"token": "string",
```


## **License**

This project is licensed under the [MIT License](LICENSE).
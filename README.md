# Dashboard Management

## Guideline
- [Guideline](#guideline)
- [Goal](#goal)
- [Demo](#demo)
- [Installation](#installation)
- [Getting Started](#getting-started)
<!-- - [Database Schema](#database-schema) -->
<!-- - [Licence](#licence) -->

## Goal

This project provides a modern, API-based dashboard management system for Django projects as a reusable alternative to the traditional Django Admin.

Instead of using `django-admin`, you can easily clone this project, integrate its management APIs, and get a fully functional admin panel with JWT authentication, permissions, and a clean UI.

Developed by the **Fahim Web** team — feel free to fork and contribute!

## Demo

In the video below, you can see how to use jwt to log in and access the permissions granted by the access token. :

<p align="center">
    <video src="./docs/demo/demo.webm"></video>
</p>

## Getting Started

This project is fully containerized with Docker. Make sure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

1. Clone the repository:
    ```
    git clone https://github.com/your-username/dashboard-management.git
    cd dashboard-management
    ```

2. Start the containers:

    ```
        docker compose up --build -d

    ```

## Apply Database Migrations

To set up the database schema, run:

```

    docker compose exec backend python manage.py makemigrations
    docker compose exec backend python manage.py migrate

```

## Development: Collect Static Files & Compile Translations

To enable multiple languages ​​and static files in the development environment, you must use the following command:

```
    docker compose exec backend python manage.py collectstatic
    docker compose exec backend python manage.py compilemessages
```

## Create Superuser

To access the dashboard, create an admin user:

```
    docker compose exec backend python manage.py createsuperuser
‍‍‍‍‍‍
```
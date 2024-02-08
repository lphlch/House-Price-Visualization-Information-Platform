# House Price Visualization Information Platform

## Overview

The House Price Visualization Information Platform is a web application developed using Django and Docker that allows users to visualize and analyze house prices in Shanghai, China. 

## Prerequisites

Before you can run the House Price Visualization Information Platform, make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/) (Python 3.6 or higher)
- [Django](https://www.djangoproject.com/download/) (Django 3.0 or higher)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to set up and run the server:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/lphlch/DatabaseProjectDesign
   cd house-price-visualization

1. Create a `.env` file in the project root directory and configure the environment variables. You can use the provided `.env.example` file as a template.

   ```
   bashCopy code
   cp .env.example .env
   ```

   Edit the `.env` file to set your desired environment variables, such as the database settings and secret key.

2. Navigate to the `/CityPrice/` directory:

   ```
   bashCopy code
   cd CityPrice
   ```

3. Create a Python virtual environment (optional but recommended):

   ```
   bashCopy code
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```
     bashCopy code
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```
     bashCopy code
     source venv/bin/activate
     ```

5. Install the required Python packages from the `requirements.txt` file:

   ```
   bashCopy code
   pip install -r requirements.txt
   ```

6. Return to the project root directory:

   ```
   bashCopy code
   cd ..
   ```

7. Build and run the Docker containers using `docker-compose`:

   ```
   bashCopy code
   docker-compose up --build
   ```

   This command will start the Django web application, a PostgreSQL database, and any other services defined in the `docker-compose.yaml` file.

8. Once the containers are up and running, you can access the House Price Visualization Information Platform in your web browser.

## Usage

Here are some basic usage instructions for the House Price Visualization Information Platform:

- **Map:** After logging in, you will be directed to the map where you can search for house prices in Shanghai and view visualizations and analysis.
- **Tables:** Explore different charts to understand what will influence the house price trends in Shanghai.

## Maintenance

To stop and remove the Docker containers, use the following command:

```
bashCopy code
docker-compose down
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Contact

For any questions or support, please contact [lphlch@outlook.com](mailto:lphlch@outlook.com).


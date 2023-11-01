# Fake Data Generation for PostgreSQL Database

This repository is configured to solve the problem of generating fake data in a PostgreSQL database for use in testing your services. The code was written using the "Mimesis" library, which is a fake data generator. You can learn more about Mimesis at [Mimesis GitHub](https://github.com/lk-geimfari/mimesis).

## Getting Started

To configure the project on a Linux system, follow these steps:

1. Create a Python virtual environment:
	```bash
	$ python3 -m venv ./dev
	```
2. Activate the virtual environment:
        ```bash
        $ source ./dev/bin/activate
        ```
3. Install the required dependencies:
        ```bash
        $ pip install -r requirements.txt
        ```
## Usage

Before running the code, make sure to update the database credentials in the Mimesis code to match your PostgreSQL database.

4. Run the script to generate fake data:
        ```bash
        $ python3 mimesis.py
        ```

Now, you can use this fake data for testing your services.

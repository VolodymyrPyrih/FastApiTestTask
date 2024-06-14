# FastAPI Project

This project uses FastAPI to create an API with users and posts.

## Requirements

Before you begin, ensure you have the following installed:

- Python 3.12
- A virtual environment for Python (recommended)

## Installation

1. Clone this repository:

    ```bash
    git clone <URL_of_your_repository>
    cd <name_of_your_repository>
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use `venv\Scripts\activate`
    ```

3. Install dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

To run the project, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8081 --reload

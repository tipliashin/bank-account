# Bank Account API

A production-ready REST API for managing bank accounts, built with FastAPI and modern Python stack. Features user management, bank accounts with different types (savings, credit), background task processing, and comprehensive test coverage.

## Features

- **User management**: create, read, update, delete users
- **Bank accounts**: deposit, withdraw, balance operations
- **Account types**: savings accounts with interest rates, credit accounts with credit limits
- **Background tasks**: async email sending simulation via Celery + Redis
- **Database migrations**: Alembic for schema versioning
- **Auto-generated API documentation**: Swagger UI at `/docs`
- **Automated tests**: pytest with CI/CD via GitHub Actions

## Tech Stack

| Component    | Technology                          |
|-------------|-------------------------------------|
| Framework    | FastAPI (async)                     |
| Database     | PostgreSQL + SQLAlchemy (async ORM) |
| Migrations   | Alembic                             |
| Background   | Celery + Redis                      |
| Testing      | pytest, pytest-asyncio              |
| CI/CD        | GitHub Actions                      |
| Environment  | python-dotenv                       |
| Containerization | Docker (coming soon)            |

## Project Structure

\`\`\`
bank-account/
├── Bank_acc/               # Core bank account classes
│   ├── bank_account.py     # BankAccount, SavingsAccount, CreditAccount
│   └── test_bank_account.py # Unit tests
├── SQL/                    # Database and API examples
│   ├── bankapi/            # FastAPI async application
│   │   ├── main.py         # API endpoints
│   │   ├── celery_app.py   # Celery configuration
│   │   └── tasks.py        # Background tasks
│   └── ...                 # Learning SQL examples
├── .github/workflows/      # CI/CD configuration
│   └── tests.yml           # Automated test workflow
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
└── .gitignore
\`\`\`

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Redis 7+

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/tipliashin/bank-account.git
cd bank-account

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database settings
echo "DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/your_db" > .env
echo "CELERY_BROKER_URL=redis://localhost:6379/0" >> .env
echo "CELERY_RESULT_BACKEND=redis://localhost:6379/1" >> .env
\`\`\`

### Database Setup

\`\`\`bash
# Create the database in PostgreSQL, then apply migrations
alembic upgrade head
\`\`\`

### Running the Application

Start the API server:
\`\`\`bash
uvicorn SQL.bankapi.main:app --reload
\`\`\`

Start the Celery worker (in a separate terminal):
\`\`\`bash
celery -A SQL.bankapi.celery_app worker --loglevel=info --pool=solo
\`\`\`

Open http://localhost:8000/docs for interactive API documentation.

### Running Tests

\`\`\`bash
pytest
\`\`\`

## API Endpoints

| Method | Endpoint              | Description              |
|--------|----------------------|--------------------------|
| POST   | /users               | Create a new user        |
| GET    | /users               | List all users           |
| GET    | /users/{id}          | Get user with accounts   |
| PUT    | /users/{id}          | Update user phone        |
| DELETE | /users/{id}          | Delete user (cascade)    |
| POST   | /accounts            | Create a new account     |
| GET    | /accounts            | List all accounts        |
| GET    | /accounts/{id}       | Get account by ID        |
| PUT    | /accounts/{id}       | Update account balance   |
| DELETE | /accounts/{id}       | Delete account           |

## Author

**Andrey Tipliashin** — [GitHub Profile](https://github.com/tipliashin)

## License

This project is created for educational purposes as part of Python backend development learning path.
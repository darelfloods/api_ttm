# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Toc Toc Medoc Backend API** - FastAPI-based REST API for pharmacy reservation and payment system.

- **Framework**: FastAPI + SQLAlchemy + PostgreSQL + MongoDB
- **Authentication**: JWT tokens with OAuth2 password flow
- **Port**: 8000 (HTTP, SSL commented out in main.py:56-58)
- **Database**: PostgreSQL (primary) at 51.68.46.67:5432, MongoDB for product catalog
- **Deployment**: Docker containerization with docker-compose

## Commands

### Local Development
```bash
python main.py              # Start server on port 8000
python3 main.py             # Alternative for Python 3
```

### Docker Deployment
```bash
docker-compose up           # Start containerized app
docker-compose up --build   # Rebuild and start
docker-compose down         # Stop containers
```

### Database
No explicit migration commands - SQLAlchemy auto-creates tables on startup via:
```python
Migration.Base.metadata.create_all(bind=Connection.engine)
```

## Architecture

### Directory Structure
```
api_ttm/
├── main.py              # FastAPI application entry point
├── core/
│   └── config.py        # Settings, API keys, database URLs
├── app/
│   ├── Api/             # External API integrations (EPG, MyPayGa, SingPay)
│   ├── Router/          # FastAPI route definitions
│   ├── Controller/      # Business logic layer
│   ├── Schema/          # Pydantic models for validation
│   ├── Db/
│   │   ├── Model/       # SQLAlchemy ORM models
│   │   ├── Connection.py    # Database connections (PostgreSQL + MongoDB)
│   │   └── Migration.py     # Database metadata
│   └── Middleware/      # Auth and database session middleware
└── requirements.txt
```

### API Endpoints (main.py:35-43)

**Authentication** (`/auth`)
- `POST /auth/login` - User login (OAuth2)
- `POST /auth/login_admin` - Admin login with role verification

**User Management** (`/user`)
- User CRUD operations

**Account Management** (`/account`)
- `GET /account/all` - List all accounts
- `GET /account/get_by_user_id/{user_id}` - Get account by user
- `PUT /account/spent/{account_id}` - Deduct credits
- `PUT /account/subscribe_rate/{account_id}` - Subscribe to pricing plan
- `PUT /account/disable_account/{account_id}` - Deactivate account
- `PUT /account/enable_account/{account_id}` - Reactivate account

**Product API** (`/api_epg`)
- `GET /api_epg/all_products/{page}/{count}` - Fetch products from EPG Supervisor
- `GET /api_epg/produits/recherche_par_libelle/{libelle}` - Search products
- `POST /api_epg/disponibility_product` - Check product availability
- `POST /api_epg/reservation` - Create pharmacy reservation
- `GET /api_epg/all_products` - List all products from MongoDB
- `POST /api_epg/products` - Create product in MongoDB

**Payment Integration**
- `/my_pay_ga` - MyPayGa mobile money payment gateway
- `/sing_pay_api` - SingPay alternative payment provider

**Pricing & Events**
- `/rate` - Subscription pricing management
- `/price_list` - Product price lists
- `/event` - User activity logging

### Database Models

**PostgreSQL Tables** (SQLAlchemy ORM):
- `users` - User accounts (id, firstname, lastname, email, phone, role, password)
- `accounts` - Credit balances (credit, subscription_date, activate, user_id, rate_id)
- `rates` - Subscription plans
- `price_lists` - Product pricing
- `events` - Activity audit log

**MongoDB Collections**:
- `products` - Product catalog with async Motor driver

### Key Configuration (core/config.py)

```python
DATABASE_URL = "postgresql://root:root@51.68.46.67:5432/toctocmedoc_db"
MONGODB_URL = "mongodb://localhost:27017"
EPG_SUPERVISOR_ADDRESS = "https://51.68.46.67:5003"  # Product availability API
ADMIN_PANEL = "https://epharma-panel.srv557357.hstgr.cloud"  # Laravel admin
```

**Token Expiration**: Dynamic - tokens expire at end of day (config.py:7-17)

### Authentication Flow

1. Client sends `username` (email) and `password` to `/auth/login`
2. `AuthController.login()` verifies credentials with bcrypt
3. JWT token generated with email + role in payload
4. Token returned in format: `{"token": {"access_token": "...", "token_type": "bearer"}, "user": {...}}`
5. Protected routes use `IsAuthenticated.get_current_user` dependency

**Admin Login**: `/auth/login_admin` additionally checks `user.role != "USER"` (AuthController.py:90-95)

### External API Integration

**EPG Supervisor** (ProductApi.py:27-28)
- Product catalog and availability system
- Requires `X_API_KEY` header (fd188670-4871-4b16-92f4-cc30e1feab7b)
- Endpoints: `/api/produits`, `/open-api/disponibilite`, `/open-api/reservation`
- Timeout: 10 seconds with connection testing (ProductApi.py:44-66)

**MyPayGa** (config.py:33-42)
- Mobile money payment gateway for Gabon
- Production API key: `sprod_HVvbdtzUcZo8HwIs1XToRfW5GqALFLPwHARNAfI1yylESgiJNu`
- Callback URLs: `https://51.68.46.67:8000/my_pay_ga/{success,callback,fail}_url`

### CORS Configuration
Wide-open CORS policy (main.py:15-21):
- Origins: `["*"]`
- Methods: `["POST", "GET", "PUT", "DELETE"]`
- Credentials: True

### Database Session Management
Custom middleware (main.py:24-33) attaches `request.state.db` to every request and ensures cleanup in `finally` block.

## Development Notes

- **SSL Disabled**: SSL certificate configuration commented out in main.py:56-58
- **No Tests**: No test directory or test commands configured
- **Event Logging**: Most controller actions trigger event creation for audit trail
- **Password Hashing**: bcrypt via passlib (config.py:26)
- **MongoDB Async**: Uses Motor async driver with async/await patterns (Connection.py:1-10)
- **Error Handling**: ProductApi implements retry logic and connection testing before main requests

## Common Patterns

### Adding New Protected Endpoint
```python
from ..Middleware import IsAuthenticated
from typing import Annotated

@router.get("/example")
async def example(
    current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
    db: Session = Depends(DatabaseSession.get_db)
):
    # current_user contains authenticated user data
    return {"message": "Success"}
```

### Credit Deduction Flow
1. Check user authentication
2. Get account via `AccountController.get_by_user_id()`
3. Verify sufficient `account.credit`
4. Call `AccountController.spent()` to deduct credits
5. Log event via `EventController.add()`

### External API Call Pattern (ProductApi.py)
1. Test connection first (5s timeout)
2. Main request with 10s timeout
3. Catch `Timeout` and `ConnectionError` exceptions
4. Return HTTPException with appropriate status codes
5. Log actions with logger.info/error

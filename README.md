# README - Setup Instructions

## Prerequisites

1. Podman installed
2. Access to Keycloak admin console at https://cloak.gs.net-sec.ch/admin

## Setup

### 1. Get Keycloak Client Secret

1. Log into Keycloak admin console
2. Select "storganizer" realm
3. Go to Clients → "storganizer-dev"
4. Navigate to "Credentials" tab
5. Copy the "Client Secret"

### 2. Configure Keycloak Client

In the "Settings" tab of your client, ensure:
- **Client authentication:** ON
- **Standard flow:** Enabled
- **Valid redirect URIs:** 
  - `http://localhost:5000/auth`
  - `http://127.0.0.1:5000/auth`
  - `http://0.0.0.0:5000/auth`
  - `http://10.1.1.21:5000/auth`

### 3. Create .env File

```bash
cp .env.example .env
```

Edit `.env` and add your actual Keycloak client secret:

```bash
KEYCLOAK_CLIENT_SECRET=your-actual-secret-from-step-1
```

### 4. Install Python Dependencies (for local development without container)

```bash
pip install -r requirements.txt
```

## Running the Application

### With Container (Recommended)

1. Build the container:
```bash
./dev-build.sh
```

2. Start the containers (API + PostgreSQL):
```bash
./dev-start.sh
```

3. First-time setup - Create database tables:
```bash
podman exec -it storganizer-api ./db-create.py
```

4. Stop and remove containers:
```bash
./dev-stop.sh
```

### Without Container (Local Development)

```bash
# Load environment variables
export $(cat .env | xargs)

# Run the API
python api.py
```

## Environment Variables

The application reads configuration from environment variables:

- `SQLALCHEMY_CONNECTION_STRING` - Database connection string
- `KEYCLOAK_CLIENT_ID` - Keycloak OAuth client ID
- `KEYCLOAK_CLIENT_SECRET` - Keycloak OAuth client secret
- `KEYCLOAK_SERVER_METADATA_URL` - Keycloak OIDC discovery URL

These are passed to the container via `--env-file .env` in `dev-start.sh`.

## API Endpoints

### Authentication
- `GET /login` - Initiate OAuth/OIDC login flow
- `GET /auth` - OAuth callback endpoint (handled automatically by Keycloak)
- `GET /profile` - View user profile (requires login)
- `GET /user` - Check login status and get user info

### Locations
- `GET /locations` - List all locations
- `GET /location/<id>` - Get location by ID
- `POST /locations` - Create new location
- `PUT /location/<id>` - Update location
- `DELETE /location/<id>` - Delete location

### Location Types
- `GET /locationTypes` - List all location types
- `GET /locationType/<id>` - Get location type by ID
- `POST /locationTypes` - Create new location type
- `PUT /locationType/<id>` - Update location type
- `DELETE /locationType/<id>` - Delete location type

### Boxes
- `GET /boxes` - List all boxes
- `GET /box/<id>` - Get box by ID
- `POST /boxes` - Create new box
- `PUT /box/<id>` - Update box
- `DELETE /box/<id>` - Delete box

### Items
- `GET /items` - List all items
- `GET /item/<id>` - Get item by ID
- `POST /items` - Create new item
- `PUT /item/<id>` - Update item
- `DELETE /item/<id>` - Delete item

### Persons
- `GET /persons` - List all persons
- `GET /person/<id>` - Get person by ID
- `POST /persons` - Create new person
- `PUT /person/<id>` - Update person
- `DELETE /person/<id>` - Delete person

### Backup & Configuration
- `GET /backup` - Create database backup
- `POST /restore` - Restore database from backup
- `GET /config/default-images` - Get default image configuration

## Troubleshooting

### OAuth Error: "Invalid client credentials"

- Verify your `.env` file has the correct `KEYCLOAK_CLIENT_SECRET`
- Check that redirect URIs are configured in Keycloak
- Ensure the client is set to "confidential" type in Keycloak

### Container doesn't read .env file

- The `.env` file is passed using `--env-file .env` in `dev-start.sh`
- Verify the file exists in the api directory
- Check file permissions: `chmod 600 .env`

### Database connection errors

- Ensure PostgreSQL container is running: `podman ps`
- Wait a few seconds for PostgreSQL to initialize
- Check connection string in `.env`

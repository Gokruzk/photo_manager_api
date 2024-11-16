# REST API Photo Album

REST API made with FastAPI, PrismaORM and PostgreSQL for manage users' photos

## Installation and Configuration

### Step 1: Create a Virtual Environment

First, create a virtual environment to manage the project dependencies.

```bash
python -m venv venv
```

### 2. Activate the virtual environment

#### On Windows

```bash
.\venv\Scripts\activate.bat
```

#### On MacOS/Linux

```bash
source venv/bin/activate
```

### 3. Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

### 4. Generate Prisma client

```bash
prisma generate
```

### Step 4: Configure the .env file

Create an `.env` file in the root of the project with the following variables:

*Variables with text are fixed, depending on your case change the variables containing []*.

```plaintext
DB_URL="postgresql://[user]:[password]@[host]:5432/photo_manager"
# Generate a key with this command: openssl rand -hex 32
SECRET_KEY = [key]
API_EMAIL = [host]
```

### Step 5: Execution

```bash
python main.py
```

## Database

Schema: public  
Database: photo_manager  
<img src="https://github.com/Gokruzk/photo_manager_api/blob/main/db_diagram.png" height=500 width=700 alt="database model">

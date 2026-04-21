# La Tulipe 🌷

> Platforma online pentru o florarie moderna cu un catalog de flori, constructor de buchete personalizate si gestionarea comenzilor.

---

## 1. Descriere si Obiective

La Tulipe este o aplicatie web care permite clientilor sa cumpere flori online, sa construiasca buchete personalizate si sa urmareasca comenzile lor. Adminii pot gestiona catalogul de produse, stocurile si statusul comenzilor.

**Obiective principale:**

- Catalog de flori cu filtrare si cautare
- Constructor de buchete personalizate
- Sistem de autentificare (client / admin)
- Gestionare comenzi cu livrare la domiciliu

**Public tinta:** Clienti care vor sa cumpere flori online si sa personalizeze buchete.

---

## 2. Echipa si Roluri

| Nume Student          | Rol Principal      | GitHub Username    |
| --------------------- | ------------------ | ------------------ |
| Costea Denisa-Adelina | Backend Developer  | @AdelinaCostea6    |
| Lupu Daniela          | Frontend Developer | @LupuDaniela       |
| Lorincz Gabriella     | QA Engineer        | @Lorincz-Gabriella |
| Maxim Ernest-George   | DevOps Engineer    | @ErnestMaxim       |

> **Team Lead:** Lupu Daniela

---

## 3. Arhitectura si Tehnologii

```
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Frontend  │  HTTP  │   Backend   │  SQL   │  Database   │
│    React    │◄──────►│   FastAPI   │◄──────►│ PostgreSQL  │
│  Port 5173  │        │  Port 8000  │        │  Port 5432  │
└─────────────┘        └─────────────┘        └─────────────┘
```

| Layer          | Tehnologie                          |
| -------------- | ----------------------------------- |
| Frontend       | React 18, React Router, Context API |
| Backend        | Python 3.11, FastAPI, SQLAlchemy    |
| Baza de date   | PostgreSQL 15                       |
| Autentificare  | JWT (JSON Web Tokens) + bcrypt      |
| Infrastructure | Docker, Docker Compose              |
| CI/CD          | GitHub Actions                      |
| Cloud Deploy   | Render / Railway                    |
| Linter/Testing | Ruff, Pytest, Playwright            |

---

## 4. Setup Local

### Cerinte

- Docker Desktop instalat
- Git instalat

### Pasi

```bash
# 1. Cloneaza repository-ul
git clone https://github.com/UniTBv-MPI-TeamDAGE/La_Tulipe.git
cd La_Tulipe

# 2. Copiaza fisierele de variabile de mediu
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Porneste aplicatia
docker compose up --build
```

### Acces

| Serviciu     | URL                              |
| ------------ | -------------------------------- |
| Frontend     | http://localhost:5173            |
| Backend API  | http://localhost:8000            |
| Health Check | http://localhost:8000/api/health |

### Variabile de mediu

**backend/.env.example**

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/la_tulipe
SECRET_KEY=your-secret-key-here
JWT_EXPIRY=3600
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=la_tulipe
ADMIN_REGISTRATION_CODE=your-admin-code-here
```

**frontend/.env.example**

```
VITE_API_URL=http://localhost:8000
```

---

## 5. Structura Proiectului

```
La_Tulipe/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml           # Linting + Teste la fiecare PR
│   │   ├── cd.yml           # Deploy automat la merge pe main
│   │   └── playwright.yml   # Teste E2E la fiecare PR
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/
│   ├── alembic/             # Migratii baza de date
│   ├── app/
│   │   ├── core/            # Bootstrap, configurare
│   │   ├── database/        # Conexiune DB, sesiune
│   │   ├── middleware/      # JWT auth, admin check
│   │   ├── models/          # Modele SQLAlchemy
│   │   ├── routes/          # Endpoint-uri FastAPI
│   │   ├── schemas/         # Scheme Pydantic
│   │   ├── services/        # Logica de business
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/               # Teste unitare pytest
│   ├── .env.example
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── entrypoint.sh
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── shared/      # Navbar, Footer, ProductCard
│   │   ├── context/         # AuthContext, CartContext
│   │   ├── dtos/            # Tipuri de date
│   │   ├── hooks/           # Custom hooks
│   │   ├── pages/           # Pagini (Home, Cart, Checkout, Admin)
│   │   ├── services/        # Apeluri API
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tests/               # Teste E2E Playwright
│   ├── .env.example
│   ├── Dockerfile
│   └── Dockerfile.dev
├── features/                # Scenarii BDD Gherkin (.feature)
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 6. Conventii Git

### Branch Naming

```
feat/nume-functionalitate     # Functionalitate noua
fix/descriere-bug             # Rezolvare bug
docs/ce-documentatie          # Documentatie
chore/configurare             # Docker, CI, setup
qa/scenarii-testare           # Teste, BDD
```

### Commit Messages (Conventional Commits)

```
feat(auth): add login endpoint with JWT
fix(cart): resolve quantity calculation bug
docs(readme): update setup instructions
chore(docker): add docker-compose prod config
test(orders): add unit tests for order placement
```

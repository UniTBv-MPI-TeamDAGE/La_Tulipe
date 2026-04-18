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
│    React    │◄──────►│Flask (Python│◄──────►│ PostgreSQL  │
│  Port 3000  │        │  Port 8000  │        │  Port 5432  │
└─────────────┘        └─────────────┘        └─────────────┘
```

| Layer          | Tehnologie                          |
| -------------- | ----------------------------------- |
| Frontend       | React 18, React Router, Context API |
| Backend        | Python 3.11, Flask, SQLAlchemy      |
| Baza de date   | PostgreSQL 18                       |
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

# 2. Copiaza fisierul de variabile de mediu
cp .env.example .env

# 3. Porneste aplicatia
docker compose up --build
```

### Acces

| Serviciu     | URL                              |
| ------------ | -------------------------------- |
| Frontend     | http://localhost:3000            |
| Backend API  | http://localhost:8000            |
| Health Check | http://localhost:8000/api/health |

### Variabile de mediu (.env.example)

```
DATABASE_URL=postgresql://user:password@db:5432/latulipe_db
SECRET_KEY=your-secret-key-here
JWT_EXPIRY=3600
DB_USER=postgres
DB_PASSWORD=postgres
REACT_APP_API_URL=http://localhost:8000
```

---

## 5. Structura Proiectului

```
La_Tulipe/
├── backend/
│   ├── app/
│   │   ├── models/          # Modele SQLAlchemy (User, Product, Order)
│   │   ├── routes/          # Endpoint-uri Flask (auth, products, orders)
│   │   ├── middleware/       # JWT auth, admin check
│   │   └── __init__.py
│   ├── tests/               # Teste unitare pytest
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Componente reutilizabile (Navbar, Footer, etc.)
│   │   ├── pages/           # Pagini (Home, Cart, Checkout, Admin)
│   │   ├── context/         # AuthContext, CartContext
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
├── features/                # Scenarii BDD Gherkin (.feature)
├── e2e/                     # Teste E2E Playwright
├── .github/
│   ├── workflows/
│   │   ├── ci.yml           # Linting + Teste la fiecare PR
│   │   └── cd.yml           # Deploy automat la merge pe main
│   └── PULL_REQUEST_TEMPLATE.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
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

### Reguli

- **Nu se face push direct pe main** (branch protection activ)
- Orice modificare = branch nou + Pull Request
- PR trebuie aprobat de minim 1 coleg inainte de merge
- PR-ul trebuie sa fie legat de un Issue (`Closes #ID`)
- CI trebuie sa treaca inainte de merge

---

## 7. API Endpoints

| Method | Endpoint               | Descriere         | Auth     |
| ------ | ---------------------- | ----------------- | -------- |
| POST   | /api/auth/register     | Inregistrare cont | -        |
| POST   | /api/auth/login        | Autentificare     | -        |
| GET    | /api/products          | Lista produse     | -        |
| GET    | /api/products/:id      | Detalii produs    | -        |
| POST   | /api/orders            | Plasare comanda   | Customer |
| GET    | /api/orders/my-orders  | Comenzile mele    | Customer |
| GET    | /api/admin/orders      | Toate comenzile   | Admin    |
| PATCH  | /api/orders/:id/status | Schimbare status  | Admin    |
| POST   | /api/products          | Adaugare produs   | Admin    |
| PUT    | /api/products/:id      | Editare produs    | Admin    |
| DELETE | /api/products/:id      | Stergere produs   | Admin    |
| GET    | /api/health            | Health check      | -        |

---

## 8. Link-uri Utile

- **Productie:** [link-deploy]
- **GitHub Projects Board:** [link-board]
- **Documentatie API:** [link-api-docs]

---

## 9. Rulare Teste

### Teste unitare backend

```bash
docker compose exec backend pytest --cov=app tests/
```

### Linter backend

```bash
docker compose exec backend ruff check .
```

### Teste E2E Playwright (local)

#### Cerinte prealabile

- Aplicatia ruleaza local: `docker compose up --build`
- Node.js 20+ instalat

#### Instalare

```bash
cd e2e
npm install
npx playwright install --with-deps chromium
```

#### Rulare

```bash
# Toate testele (headless)
cd e2e
npx playwright test

# Cu browser vizibil
npx playwright test --headed

# Un singur test
npx playwright test tests/auth.spec.ts

# Raport HTML dupa rulare
npx playwright show-report
```

#### Variabile de mediu pentru E2E

| Variabila  | Default                 | Descriere    |
| ---------- | ----------------------- | ------------ |
| `BASE_URL` | `http://localhost:3000` | URL frontend |
| `API_URL`  | `http://localhost:8000` | URL backend  |

Pot fi suprascrise la rulare:

```bash
BASE_URL=http://localhost:3000 API_URL=http://localhost:8000 npx playwright test
```

#### Teste disponibile

| Test   | Fisier                          | Descriere                                      |
| ------ | ------------------------------- | ---------------------------------------------- |
| E2E #1 | `tests/auth.spec.ts`            | Inregistrare cont nou + login                  |
| E2E #2 | `tests/search-cart.spec.ts`     | Cautare floare + adaugare in cos               |
| E2E #3 | `tests/checkout.spec.ts`        | Checkout complet (cos → formular → confirmare) |
| E2E #4 | `tests/bouquet-builder.spec.ts` | Constructor buchet → adaugare in cos           |
| E2E #5 | `tests/admin.spec.ts`           | Admin login + schimbare status comanda         |

#### CI

Testele E2E ruleaza automat in GitHub Actions la fiecare Pull Request catre `main`, in job-ul `test-e2e`. Raportul Playwright este salvat ca artifact timp de 7 zile si poate fi descarcat din tab-ul **Actions** al oricarui PR.

---

_Proiect realizat in cadrul cursului Managementul Proiectelor Informatice_  
_Facultatea de Matematica si Informatica, Universitatea Transilvania din Brasov_  
_Anul III, Semestrul II, 2025-2026_

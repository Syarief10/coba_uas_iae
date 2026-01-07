# SpaceMaster - Microservices Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![GraphQL](https://img.shields.io/badge/GraphQL-Ariadne-E10098.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

**Platform manajemen venue, ruangan, dan jadwal berbasis arsitektur microservices dengan GraphQL API**

</div>

---

## 📑 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Arsitektur](#-arsitektur)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Menjalankan Project](#-menjalankan-project)
- [Struktur Database](#-struktur-database)
- [Dokumentasi API](#-dokumentasi-api)
- [Fitur Utama](#-fitur-utama)
- [Struktur Project](#-struktur-project)
- [Environment Variables](#-environment-variables)
- [Testing GraphQL](#-testing-graphql)
- [Troubleshooting](#-troubleshooting)
- [Pengembangan](#-pengembangan)

---

## 🎯 Tentang Project

**SpaceMaster** adalah platform manajemen komprehensif yang dirancang untuk mengelola venue (lokasi), ruangan, dan jadwal booking. Project ini dibangun menggunakan arsitektur microservices yang memisahkan setiap domain bisnis menjadi service independen yang berkomunikasi melalui GraphQL API.

### Keunggulan SpaceMaster:

- ✅ **Scalable**: Setiap service dapat di-scale secara independen
- ✅ **Modular**: Pemisahan concern yang jelas antar service
- ✅ **Flexible**: Mudah untuk menambahkan service baru
- ✅ **GraphQL First**: API yang powerful dan flexible
- ✅ **Production Ready**: Menggunakan Docker untuk deployment

---

## 🏗️ Arsitektur

Project ini menggunakan arsitektur microservices dengan 5 service utama:

```
┌─────────────────────────────────────────────────────────────┐
│                    SpaceMaster Gateway                       │
│                    (Port: 8004)                             │
│               [Unified GraphQL API]                         │
└──────────┬──────────────┬──────────────┬───────────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Venue   │   │   Room   │   │ Schedule │
    │ Service  │◄──┤ Service  │◄──┤ Service  │
    │  :8001   │   │  :8002   │   │  :8003   │
    └────┬─────┘   └────┬─────┘   └────┬─────┘
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Venue   │   │  Room   │   │Schedule │
    │   DB    │   │   DB    │   │   DB    │
    └─────────┘   └─────────┘   └─────────┘

    ┌──────────────────────────────────────┐
    │       Auth Service (Port: 8000)      │
    │     [Authentication & Authorization] │
    └────────────────┬─────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │   Auth DB   │
              └─────────────┘
```

### Penjelasan Arsitektur:

1. **SpaceMaster Gateway** - API Gateway yang menggabungkan semua service menjadi satu unified GraphQL endpoint
2. **Auth Service** - Menangani autentikasi, registrasi, dan manajemen user
3. **Venue Service** - Mengelola data venue (lokasi)
4. **Room Service** - Mengelola data ruangan di setiap venue
5. **Schedule Service** - Mengelola jadwal dan ketersediaan ruangan

---

## 🛠️ Teknologi yang Digunakan

### Backend Framework
- **FastAPI** - Modern, fast (high-performance) web framework
- **Ariadne** - Schema-first GraphQL library untuk Python
- **SQLAlchemy** - Python SQL toolkit dan ORM

### Database
- **PostgreSQL 15** - Relational database untuk setiap service

### Authentication & Security
- **python-jose** - JWT token handling
- **bcrypt** - Password hashing

### Containerization
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration

### API Protocol
- **GraphQL** - Query language untuk API

---

## 📋 Prasyarat

Sebelum menjalankan project ini, pastikan Anda telah menginstall:

- **Docker** (versi 20.10 atau lebih baru)
- **Docker Compose** (versi 2.0 atau lebih baru)
- **Git** (untuk cloning repository)

Untuk development lokal (optional):
- **Python 3.11+**
- **PostgreSQL 15+**

---

## 💾 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd SpaceMaster
```

### 2. Verifikasi Struktur Project

Pastikan struktur folder sebagai berikut:

```
SpaceMaster/
├── auth-service/
├── venue-service/
├── room-service/
├── schedule-service/
├── spacemaster-gateway/
├── docker-compose.yml
└── README.md
```

---

## 🚀 Menjalankan Project

### Menggunakan Docker Compose (Recommended)

#### 1. Build dan Jalankan Semua Services

```bash
docker-compose up --build
```

#### 2. Jalankan di Background

```bash
docker-compose up -d --build
```

#### 3. Lihat Logs

```bash
# Semua services
docker-compose logs -f

# Service tertentu
docker-compose logs -f auth-service
docker-compose logs -f venue-service
```

#### 4. Stop Services

```bash
docker-compose down
```

#### 5. Stop dan Hapus Volumes (Data Reset)

```bash
docker-compose down -v
```

### Menjalankan Service Secara Individual (Development)

#### Auth Service

```bash
cd auth-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Venue Service

```bash
cd venue-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### Room Service

```bash
cd room-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

#### Schedule Service

```bash
cd schedule-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

#### Gateway

```bash
cd spacemaster-gateway
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```

---

## 📊 Struktur Database

### Auth Service Database

**Table: users**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| username | VARCHAR(100) | Username (unique) |
| password_hash | VARCHAR(255) | Hashed password |
| role | VARCHAR(50) | User role (admin/user) |

### Venue Service Database

**Table: venues**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| name | VARCHAR(150) | Venue name (unique) |
| address | TEXT | Venue address |
| city | VARCHAR(100) | City location |
| description | TEXT | Venue description (nullable) |

### Room Service Database

**Table: rooms**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| name | VARCHAR(150) | Room name |
| capacity | INTEGER | Room capacity |
| venue_id | INTEGER | Foreign key to venue |

### Schedule Service Database

**Table: schedules**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| room_id | INTEGER | Foreign key to room |
| start_time | DATETIME | Schedule start time |
| end_time | DATETIME | Schedule end time |
| status | ENUM | Status: AVAILABLE/BLOCKED/MAINTENANCE |

---

## 📡 Dokumentasi API

### Service Endpoints

| Service | Port | GraphQL Endpoint | GraphiQL UI |
|---------|------|------------------|-------------|
| **Gateway** | 8004 | http://localhost:8004/graphql | ✅ Tersedia |
| Auth Service | 8000 | http://localhost:8000/graphql | ✅ Tersedia |
| Venue Service | 8001 | http://localhost:8001/graphql | ✅ Tersedia |
| Room Service | 8002 | http://localhost:8002/graphql | ✅ Tersedia |
| Schedule Service | 8003 | http://localhost:8003/graphql | ✅ Tersedia |

> **💡 Tip**: Akses endpoint GraphQL melalui browser untuk membuka GraphiQL playground

---

### 🔐 Auth Service API

#### **Mutation: Register User**

```graphql
mutation {
  register(
    username: "john_doe"
    password: "securepassword123"
    role: "admin"
  ) {
    success
    message
  }
}
```

#### **Mutation: Login**

```graphql
mutation {
  login(
    username: "john_doe"
    password: "securepassword123"
  ) {
    success
    message
    access_token
    role
  }
}
```

#### **Query: Health Check**

```graphql
query {
  health
}
```

---

### 🏢 Venue Service API

#### **Query: Get All Venues**

```graphql
query {
  venues {
    id
    name
    city
    address
    description
  }
}
```

#### **Query: Get Single Venue**

```graphql
query {
  venue(id: "1") {
    id
    name
    city
    address
    description
  }
}
```

#### **Mutation: Create Venue**

```graphql
mutation {
  createVenue(data: {
    name: "Grand Hotel Jakarta"
    city: "Jakarta"
    address: "Jl. Sudirman No. 123"
    description: "Hotel mewah di pusat kota"
  }) {
    success
    message
    venue {
      id
      name
      city
    }
  }
}
```

#### **Mutation: Update Venue**

```graphql
mutation {
  updateVenue(id: "1", data: {
    name: "Grand Hotel Jakarta Updated"
    city: "Jakarta"
    address: "Jl. Sudirman No. 123"
    description: "Updated description"
  }) {
    success
    message
    venue {
      id
      name
    }
  }
}
```

#### **Mutation: Delete Venue**

```graphql
mutation {
  deleteVenue(id: "1") {
    success
    message
  }
}
```

---

### 🚪 Room Service API

#### **Query: Get Rooms by Venue**

```graphql
query {
  roomsByVenue(venueId: "1") {
    id
    name
    capacity
    venueId
  }
}
```

#### **Query: Get Single Room**

```graphql
query {
  room(id: "1") {
    id
    name
    capacity
    venueId
  }
}
```

#### **Mutation: Create Room**

```graphql
mutation {
  createRoom(data: {
    name: "Meeting Room A"
    capacity: 50
    venueId: "1"
  }) {
    id
    name
    capacity
    venueId
  }
}
```

---

### 📅 Schedule Service API

#### **Query: Get All Schedules**

```graphql
query {
  schedules {
    id
    roomId
    startTime
    endTime
    status
  }
}
```

#### **Query: Get Available Slots**

```graphql
query {
  availableSlots(
    roomId: 1
    startDate: "2025-01-01T00:00:00"
    endDate: "2025-01-31T23:59:59"
  ) {
    startTime
    endTime
  }
}
```

#### **Mutation: Create Schedule**

```graphql
mutation {
  createSchedule(data: {
    roomId: 1
    startTime: "2025-01-10T09:00:00"
    endTime: "2025-01-10T12:00:00"
    status: AVAILABLE
  }) {
    id
    roomId
    startTime
    endTime
    status
  }
}
```

#### **Mutation: Update Schedule**

```graphql
mutation {
  updateSchedule(id: "1", data: {
    status: BLOCKED
  }) {
    id
    status
  }
}
```

#### **Mutation: Block Schedule**

```graphql
mutation {
  blockSchedule(input: {
    roomId: 1
    startTime: "2025-01-15T09:00:00"
    endTime: "2025-01-15T17:00:00"
  }) {
    success
    message
  }
}
```

#### **Mutation: Delete Schedule**

```graphql
mutation {
  deleteSchedule(id: "1")
}
```

---

### 🌐 Gateway API (Unified)

Gateway menggabungkan semua service dengan relationship antar entity:

#### **Query: Venues with Rooms**

```graphql
query {
  venues {
    id
    name
    city
    rooms {
      id
      name
      capacity
    }
  }
}
```

#### **Query: Room with Venue and Schedules**

```graphql
query {
  room(id: "1") {
    id
    name
    capacity
    venue {
      name
      city
    }
    schedules {
      id
      startTime
      endTime
      status
    }
  }
}
```

#### **Query: Schedule with Room Details**

```graphql
query {
  schedules {
    id
    startTime
    endTime
    status
    room {
      name
      capacity
      venue {
        name
        city
      }
    }
  }
}
```

---

## ✨ Fitur Utama

### 1. Authentication & Authorization
- ✅ User registration dengan role-based
- ✅ Login dengan JWT token
- ✅ Password hashing menggunakan bcrypt
- ✅ Role management (admin/user)

### 2. Venue Management
- ✅ CRUD operations untuk venue
- ✅ Unique constraint pada nama venue
- ✅ Relasi dengan rooms
- ✅ Search dan filter venue

### 3. Room Management
- ✅ Create dan manage rooms per venue
- ✅ Capacity tracking
- ✅ Relasi dengan venue dan schedules
- ✅ Query rooms by venue

### 4. Schedule Management
- ✅ Create dan manage schedules
- ✅ Status tracking (AVAILABLE/BLOCKED/MAINTENANCE)
- ✅ Check available time slots
- ✅ Block/unblock schedules
- ✅ Prevent scheduling conflicts

### 5. API Gateway
- ✅ Unified GraphQL endpoint
- ✅ Service orchestration
- ✅ Cross-service relationships
- ✅ Data aggregation dari multiple services

---

## 📁 Struktur Project

```
SpaceMaster/
│
├── auth-service/                 # Authentication & Authorization Service
│   ├── app/
│   │   ├── schema/
│   │   │   ├── __init__.py
│   │   │   ├── mutation.py      # GraphQL mutations (register, login)
│   │   │   ├── query.py         # GraphQL queries
│   │   │   └── schema.graphql   # GraphQL schema definition
│   │   ├── auth.py              # JWT token handling
│   │   ├── database.py          # Database connection
│   │   ├── jwt_middleware.py    # JWT middleware
│   │   ├── main.py              # FastAPI application
│   │   └── models.py            # SQLAlchemy models (User)
│   ├── Dockerfile
│   └── requirements.txt
│
├── venue-service/                # Venue Management Service
│   ├── app/
│   │   ├── graphql/
│   │   │   ├── __init__.py
│   │   │   ├── mutation.py      # Venue mutations (CRUD)
│   │   │   ├── query.py         # Venue queries
│   │   │   └── schema.graphql   # GraphQL schema
│   │   ├── auth.py              # Auth middleware
│   │   ├── database.py          # Database connection
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Venue model
│   │   └── seed.py              # Database seeding
│   ├── Dockerfile
│   └── requirements.txt
│
├── room-service/                 # Room Management Service
│   ├── app/
│   │   ├── graphql/
│   │   │   ├── __init__.py
│   │   │   ├── mutation.py      # Room mutations
│   │   │   ├── query.py         # Room queries
│   │   │   ├── schema.graphql   # GraphQL schema
│   │   │   └── types.py         # GraphQL types
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── venue_client.py  # Venue service client
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py            # Room model
│   │   └── schema.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── schedule-service/             # Schedule Management Service
│   ├── app/
│   │   ├── graphql/
│   │   │   ├── mutation.py      # Schedule mutations
│   │   │   ├── query.py         # Schedule queries
│   │   │   └── schema.graphql   # GraphQL schema
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── integrations.py      # Service integrations
│   │   ├── main.py
│   │   ├── models.py            # Schedule model
│   │   └── room_client.py       # Room service client
│   ├── Dockerfile
│   └── requirements.txt
│
├── spacemaster-gateway/          # API Gateway (Unified GraphQL)
│   ├── app/
│   │   ├── graphql/
│   │   │   ├── resolvers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── room.py      # Room resolvers
│   │   │   │   ├── schedule.py  # Schedule resolvers
│   │   │   │   └── venue.py     # Venue resolvers
│   │   │   └── schema.graphql   # Unified GraphQL schema
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── room_client.py
│   │   │   ├── schedule_client.py
│   │   │   └── venue_client.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```

---

## 🔧 Environment Variables

### Auth Service
```env
DATABASE_URL=postgresql://postgres:postgres@auth-db:5432/auth_db
```

### Venue Service
```env
DATABASE_URL=postgresql://postgres:postgres@venue-db:5432/venue_db
```

### Room Service
```env
DATABASE_URL=postgresql://postgres:postgres@room-db:5432/room_db
```

### Schedule Service
```env
DATABASE_URL=postgresql://postgres:postgres@schedule-db:5432/schedule_db
```

### Gateway
```env
VENUE_SERVICE_URL=http://venue-service:8000/graphql
ROOM_SERVICE_URL=http://room-service:8000/graphql
SCHEDULE_SERVICE_URL=http://schedule-service:8000/graphql
```

---

## 🧪 Testing GraphQL

### Menggunakan GraphiQL (Browser)

1. **Buka GraphiQL Interface**
   - Gateway: http://localhost:8004/graphql
   - Auth: http://localhost:8000/graphql
   - Venue: http://localhost:8001/graphql
   - Room: http://localhost:8002/graphql
   - Schedule: http://localhost:8003/graphql

2. **Jalankan Query/Mutation**
   - Copy salah satu query/mutation dari dokumentasi API di atas
   - Paste ke GraphiQL editor
   - Klik tombol "Play" atau tekan Ctrl+Enter

### Menggunakan curl

#### Register User
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { register(username: \"admin\", password: \"admin123\", role: \"admin\") { success message } }"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { login(username: \"admin\", password: \"admin123\") { success message access_token role } }"
  }'
```

#### Get Venues
```bash
curl -X POST http://localhost:8004/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { venues { id name city address } }"
  }'
```

### Menggunakan Postman

1. **Setup Request**
   - Method: POST
   - URL: http://localhost:8004/graphql
   - Headers: Content-Type: application/json

2. **Body (GraphQL)**
   ```json
   {
     "query": "query { venues { id name city } }"
   }
   ```

---

## 🔍 Troubleshooting

### Problem: Service tidak bisa start

**Solution:**
```bash
# Check logs
docker-compose logs [service-name]

# Restart service
docker-compose restart [service-name]

# Rebuild service
docker-compose up --build [service-name]
```

### Problem: Database connection error

**Solution:**
```bash
# Wait for database to be ready
docker-compose ps

# Check database health
docker-compose exec auth-db pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up --build
```

### Problem: Port sudah digunakan

**Solution:**
```bash
# Check port usage
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Kill process or change port di docker-compose.yml
```

### Problem: GraphQL query error

**Solution:**
- Pastikan format query benar
- Check GraphQL schema di masing-masing service
- Gunakan GraphiQL untuk auto-completion
- Periksa logs untuk error detail

### Problem: Service tidak bisa komunikasi

**Solution:**
```bash
# Check network
docker network ls
docker network inspect spacemaster_spacemaster-net

# Ensure all services in same network
docker-compose ps
```

---

## 👨‍💻 Pengembangan

### Menambah Service Baru

1. **Buat folder service baru**
   ```bash
   mkdir new-service
   cd new-service
   ```

2. **Setup struktur**
   ```
   new-service/
   ├── app/
   │   ├── main.py
   │   ├── models.py
   │   ├── database.py
   │   └── graphql/
   │       ├── schema.graphql
   │       ├── query.py
   │       └── mutation.py
   ├── Dockerfile
   └── requirements.txt
   ```

3. **Tambahkan ke docker-compose.yml**
   ```yaml
   new-service:
     build: ./new-service
     environment:
       DATABASE_URL: postgresql://postgres:postgres@new-db:5432/new_db
     ports:
       - "8005:8000"
     networks:
       - spacemaster-net
   ```

### Best Practices

1. **Code Organization**
   - Pisahkan business logic dari resolvers
   - Gunakan service layer untuk inter-service communication
   - Keep models clean dan focused

2. **Error Handling**
   - Implement proper error handling di semua resolvers
   - Return meaningful error messages
   - Log errors untuk debugging

3. **Security**
   - Implement authentication untuk protected endpoints
   - Validate input data
   - Sanitize user inputs
   - Use environment variables untuk credentials

4. **Testing**
   - Write unit tests untuk business logic
   - Test GraphQL queries dan mutations
   - Integration testing antar services

5. **Documentation**
   - Document GraphQL schema dengan descriptions
   - Keep README up to date
   - Document API changes

### Database Migrations

Untuk production, gunakan Alembic untuk database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

---

## 📞 Support & Contribution

### Melaporkan Bug
Jika Anda menemukan bug, silakan buat issue dengan:
- Deskripsi bug
- Steps to reproduce
- Expected behavior
- Screenshots (jika ada)
- Environment details

### Feature Request
Untuk request fitur baru:
- Deskripsi fitur
- Use case
- Mockup/diagram (jika ada)

### Contributing
Pull requests are welcome! Untuk perubahan besar:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📄 License

Project ini dibuat untuk keperluan pembelajaran dan pengembangan.

---

## 🙏 Acknowledgments

- FastAPI Framework
- Ariadne GraphQL
- PostgreSQL
- Docker & Docker Compose
- Python Community

---

<div align="center">

**Made with ❤️ using Python & GraphQL**

**SpaceMaster - Your Space Management Solution**

</div>

# 🌤️ Weather Data Analytics Platform

A comprehensive, containerized weather data pipeline that orchestrates real-time weather data ingestion, transformation, and visualization using modern data engineering tools.

![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![Status](https://img.shields.io/badge/Status-Production_Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🏗️ Architecture Overview

This project implements a modern ELT (Extract, Load, Transform) data pipeline for weather data analytics with the following architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Weatherstack  │───▶│    Airflow      │───▶│   PostgreSQL    │───▶│   Apache        │
│      API        │    │  Orchestrator   │    │   Database      │    │  Superset       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │      dbt        │───▶│     Redis       │
                       │  Transformations│    │     Cache       │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Key Features

- **📊 Real-time Data Ingestion**: Automated weather data collection from Weatherstack API
- **🔄 Orchestrated Workflows**: Apache Airflow manages the entire data pipeline
- **🛠️ Data Transformation**: dbt handles data modeling and transformations
- **📈 Interactive Dashboards**: Apache Superset for data visualization and analytics
- **🐳 Containerized Architecture**: Fully dockerized for easy deployment and scaling
- **⚡ High Performance**: PostgreSQL database with Redis caching
- **🔍 Data Quality**: Built-in deduplication and data validation

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow 3.0.0 | Workflow management and scheduling |
| **Database** | PostgreSQL 14.17 | Primary data storage |
| **Transformation** | dbt (Data Build Tool) | Data modeling and transformations |
| **Visualization** | Apache Superset 3.0.0 | Business intelligence and dashboards |
| **Caching** | Redis 7 | Session management and caching |
| **Containerization** | Docker & Docker Compose | Service orchestration |
| **API Integration** | Weatherstack API | Weather data source |

## 📁 Project Structure

```
weather_data_project/
├── 🐳 docker-compose.yml          # Multi-service container orchestration
├── 📋 Makefile                    # Build and deployment automation
├── 
├── 🌊 airflow/                    # Workflow orchestration
│   └── dags/
│       └── orchestrator.py       # Main DAG for data pipeline
│
├── 🔌 api-request/                # Data ingestion module
│   ├── api_request.py            # Weatherstack API client
│   └── insert_records.py         # Database insertion logic
│
├── 🔧 dbt/                       # Data transformation layer
│   ├── profiles.yml              # Database connection profiles
│   └── weather_project/          # dbt project
│       ├── dbt_project.yml       # Project configuration
│       └── models/               # Data models
│           ├── sources/          # Source definitions
│           ├── staging/          # Staging transformations
│           └── mart/             # Business logic models
│
├── 🐘 postgres/                  # Database initialization
│   ├── airflow_init.sql          # Airflow database setup
│   └── superset_init.sql         # Superset database setup
│
└── 🐋 docker/                    # Container configurations
    ├── docker-bootstrap.sh       # Superset bootstrap script
    ├── docker-init.sh             # Superset initialization
    └── superset_config.py         # Superset configuration
```

## 🎯 Data Pipeline Flow

### 1. **Data Ingestion** 📥
- **Source**: Weatherstack API provides real-time weather data for Fez, Morocco
- **Frequency**: Every minute (configurable via Airflow DAG)
- **Format**: JSON response with location and current weather information
- **Storage**: Raw data stored in `dev.raw_weather_data` table

### 2. **Data Orchestration** 🎼
- **Tool**: Apache Airflow manages the entire pipeline
- **Schedule**: Automated execution every minute
- **Tasks**:
  - `ingest_data_task`: Fetches and stores raw weather data
  - `transform_data_task`: Triggers dbt transformations

### 3. **Data Transformation** 🔄
- **Staging Layer** (`stg_weather_data.sql`):
  - Deduplicates records based on timestamp
  - Converts timezone information
  - Cleans and standardizes data formats

- **Mart Layer**:
  - `daily_avg.sql`: Aggregates daily temperature and wind speed averages
  - `weather_report.sql`: Creates clean, analysis-ready weather reports

### 4. **Data Visualization** 📊
- **Tool**: Apache Superset provides interactive dashboards
- **Features**: Charts, filters, and real-time analytics
- **Access**: Web-based interface for business intelligence

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** (for local development and testing)
- Docker & Docker Compose
- WSL2 (for Windows users)
- **Weatherstack API key** (free account available at [weatherstack.com](https://weatherstack.com/))

### 1. **Environment Setup**

#### **Step 1: Get Your Weatherstack API Key** 🔑
1. Visit [https://weatherstack.com/](https://weatherstack.com/)
2. Sign up for a free account
3. Navigate to your dashboard and copy your API Access Key

#### **Step 2: Clone and Configure** 
```bash
# Clone the repository
git clone <repository-url>
cd weather_data_project

# Create environment file in the api-request directory
cd api-request
echo "API_Access_Key=your_actual_weatherstack_api_key" > .env

# Return to project root
cd ..
```

> ⚠️ **Important**: Make sure to replace `your_actual_weatherstack_api_key` with your real API key from Weatherstack!

#### **Step 3: Python Virtual Environment Setup** 🐍
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell/CMD):
venv\Scripts\activate

# On Linux/macOS:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

> 💡 **Note**: The virtual environment is needed for local development and testing of the API scripts. The main application runs in Docker containers.

### 2. **Launch the Platform**
```bash
# Start all services
make all

# Alternative: direct docker-compose
docker-compose up -d
```

### 3. **Access the Services**

| Service | URL | Credentials |
|---------|-----|-------------|
| **Airflow** | http://localhost:8000 | admin / admin |
| **Superset** | http://localhost:8088 | admin / admin |
| **PostgreSQL** | localhost:5000 | ipman / ipman42 |

### 4. **Verify the Pipeline**
1. Navigate to Airflow UI and enable the `weather-api-dbt-orchestrator` DAG
2. Monitor the pipeline execution in real-time
3. Check the transformed data in PostgreSQL
4. Create visualizations in Superset

## 🔧 Configuration

### Database Schema
```sql
-- Raw weather data structure
CREATE TABLE dev.raw_weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature FLOAT,
    weather_descriptions TEXT,
    wind_speed FLOAT,
    time TIMESTAMP,
    inserted_at TIMESTAMP DEFAULT NOW(),
    utc_offset TEXT
);
```

### dbt Models
- **Sources**: Define connections to raw data tables
- **Staging**: Data cleaning and standardization
- **Mart**: Business logic and analytics-ready tables

### Airflow Configuration
- **Schedule**: Configurable interval (default: 1 minute)
- **Retry Logic**: Built-in error handling and retries
- **Monitoring**: Real-time pipeline status and logs

## 📊 Data Models

### Staging Layer
- **`stg_weather_data`**: Deduplicated and cleaned weather records
- Handles timezone conversions and data quality issues

### Mart Layer
- **`daily_avg`**: Daily aggregations of temperature and wind speed
- **`weather_report`**: Current weather conditions for reporting

## 🔍 Monitoring & Observability

- **Airflow UI**: Pipeline execution monitoring and debugging
- **dbt Logs**: Transformation process tracking
- **PostgreSQL Logs**: Database performance and query analysis
- **Docker Logs**: Container health and resource utilization

## 🛠️ Local Development

### Python Dependencies 📦
The project includes a `requirements.txt` file with all necessary Python packages:

```txt
# Core Dependencies
requests==2.31.0          # HTTP requests for API calls
psycopg2-binary==2.9.7    # PostgreSQL database adapter
python-dotenv==1.0.0      # Environment variable management

# Optional Development Tools
pandas==2.1.0             # Data manipulation (if needed)
dbt-core==1.6.0           # Local dbt development
pytest==7.4.0             # Testing framework
```

### Local Testing 🧪
```bash
# Activate your virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Test API connection locally
cd api-request
python api_request.py

# Test database insertion (requires running PostgreSQL container)
python insert_records.py
```

### Development Workflow 🔄
1. **Make changes** to Python scripts in `api-request/`
2. **Test locally** using the virtual environment
3. **Rebuild containers** if needed: `docker-compose up --build`
4. **Monitor logs** through Airflow UI and container logs

## 🛠️ Advanced Development

### Adding New Data Sources
1. Create new API client in `api-request/`
2. Update `insert_records.py` for new data structure
3. Add new dbt sources and models
4. Update Airflow DAG for additional tasks

### Scaling Considerations
- **Horizontal Scaling**: Add more Airflow workers
- **Database Optimization**: Implement partitioning for large datasets
- **Caching Strategy**: Leverage Redis for frequently accessed data
- **Monitoring**: Add Prometheus/Grafana for advanced monitoring

## 🐳 Docker Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| PostgreSQL | `pg-db` | 5000 | Primary database |
| Airflow | `airflow_container` | 8000 | Workflow orchestration |
| dbt | `dbt_container` | - | Data transformations |
| Superset | `superset_app` | 8088 | Data visualization |
| Redis | `superset_cache` | 6379 | Caching layer |

## 🔒 Security Features

- Containerized environment isolation
- Environment variable management
- Database connection security
- Service-to-service authentication

## 📈 Performance Optimization

- **Database Indexing**: Optimized queries for large datasets
- **Connection Pooling**: Efficient database connections
- **Caching**: Redis for improved response times
- **Resource Management**: Docker resource limits and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request


## 🆘 Troubleshooting

### Common Issues

#### **API Key Problems** 🔑
- **Error**: "API request failed" or "Unauthorized"
- **Solution**: 
  1. Verify your `.env` file exists in the `api-request/` directory
  2. Check that your Weatherstack API key is correct
  3. Ensure you haven't exceeded your API rate limits (free tier: 1,000 calls/month)
  4. Test your API key directly: `curl "http://api.weatherstack.com/current?access_key=YOUR_KEY&query=London"`

#### **Container Issues** 🐳
- **Error**: "Port already in use"
- **Solution**: Stop conflicting services or change ports in `docker-compose.yml`

#### **Database Connection Issues** 🗄️
- **Error**: "Connection refused"
- **Solution**: Wait for PostgreSQL to fully initialize (may take 1-2 minutes on first run)

### Support Resources

For additional help:
- Check the [Issues](https://github.com/your-repo/issues) page
- Review Airflow and dbt logs for troubleshooting
- Consult the [Wiki](https://github.com/your-repo/wiki) for detailed documentation
- **Weatherstack API Documentation**: [https://weatherstack.com/documentation](https://weatherstack.com/documentation)

---

**Built By Mel-harc using modern data engineering practices**

*Transform weather data into actionable insights with enterprise-grade reliability and scalability.*

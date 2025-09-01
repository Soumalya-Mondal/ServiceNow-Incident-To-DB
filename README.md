# ServiceNow Incident Ticket Fetcher

This Python script connects to the **ServiceNow API**, retrieves **incident ticket data**, and stores it into a **PostgreSQL database**.  
It is designed to run efficiently by fetching **only new tickets** while maintaining an activity log for auditing and monitoring.

---

## 🚀 Features
- **Incremental Data Fetching**: Only new incident tickets are retrieved; old tickets are skipped automatically.  
- **PostgreSQL Integration**: Seamlessly inserts fetched data into a PostgreSQL database.  
- **Activity Logging**: Maintains detailed logs of API calls, database inserts, and errors for debugging and traceability.  

---

## ⚙️ Requirements
- Python 3.8+
- PostgreSQL server
- Dependencies managed with [uv](https://github.com/astral-sh/uv)

---

## 🔧 Setup

1. **Install dependencies**  
   If you have a `pyproject.toml`:
   ```bash
   uv sync
   ```

   Or install directly:
   ```bash
   uv add requests psycopg2-binary python-dotenv
   ```

2. **Environment Variables**  
   Create a `.env` file (or configure system environment variables) with the following keys:

   ```ini
   SNOW_ENDPOINT=https://your-instance.service-now.com
   SNOW_USERNAME=your-username
   SNOW_PASSWORD=your-password

   PG_HOST=localhost
   PG_DB_NAME=incidentdb
   PG_USERNAME=your-db-user
   PG_PASSWORD=your-db-password
   PG_PORT=5432
   ```

3. **Database Setup**  
   Ensure the PostgreSQL database and required tables exist.  
   Example schema:
   ```sql
   CREATE TABLE incident_data (
      id SERIAL PRIMARY KEY,
      ticket_type VARCHAR(50),
      company VARCHAR(50),
      sys_id VARCHAR(50) UNIQUE NOT NULL,
      number VARCHAR(50) NOT NULL,
      created_by VARCHAR(50),
      created_on TIMESTAMPTZ,
      opened_by VARCHAR(50),
      opened_at TIMESTAMPTZ,
      configuration_item VARCHAR(100),
      category VARCHAR(50),
      subcategory VARCHAR(50),
      priority VARCHAR(20),
      impact VARCHAR(20),
      urgency VARCHAR(20),
      severity VARCHAR(20),
      state VARCHAR(20),
      incident_state VARCHAR(20),
      assignment_group VARCHAR(50),
      assigned_to VARCHAR(50),
      parent_incident VARCHAR(50),
      business_process VARCHAR(100),
      vendor VARCHAR(100),
      environment VARCHAR(100),
      availability_group VARCHAR(100),
      short_description VARCHAR(100),
      description VARCHAR(1000),
      resolved_by VARCHAR(50),
      resolved_at TIMESTAMPTZ,
      close_code VARCHAR(50),
      close_notes VARCHAR(500),
      work_notes TEXT,
      CONSTRAINT sys_id_not_blank CHECK (btrim(sys_id) <> ''),
      CONSTRAINT number_not_blank CHECK (btrim(number) <> '')
   );
   ALTER TABLE incident_data OWNER TO <table-owner>;
   ```

---

## ▶️ Usage
Run the script with uv:
```bash
uv run main.py
```

- On the first run, it will fetch all available incident tickets.  
- On subsequent runs, it will **only fetch new tickets** that are not already present in the database.  

---

## 📜 Logs
Logs are stored in `activity.log` (configurable).  
They include:
- Successful API calls
- Number of tickets fetched
- Database insert/update results
- Errors (API or DB failures)

---

## 🛠 Future Enhancements
- Support for ticket updates (not just new ones)
- Configurable scheduling with `cron` or `APScheduler`
- Dockerization for deployment

---

## 📝 License
This project is licensed under the MIT License.

# UTP IoT Data Acquisition & Analytic System for Aircraft Monitoring (Perak Airspace)

## Project Overview
This project is an IoT-based aircraft monitoring and analytics system developed for academic purposes at Universiti Teknologi PETRONAS (UTP). The system collects live aircraft state data from the OpenSky Network API, stores the data in a local SQLite database, and visualizes the information through an interactive Streamlit dashboard.

The project demonstrates the concept of **IoT data acquisition, storage, processing, and analytics** by monitoring aircraft movement over the Perak region in real time.

---

## Objectives
- To acquire real-time aircraft data from an external aviation data source (OpenSky API)
- To store the collected aircraft data in a structured SQLite database
- To analyze aircraft movement data such as altitude, velocity, and country of origin
- To visualize aircraft activity in the Perak airspace using an interactive dashboard
- To demonstrate an IoT-style data acquisition and analytics workflow

---

## Features
- Real-time aircraft data collection using OpenSky Network API
- SQLite database for local data storage
- Interactive Streamlit dashboard
- KPI metrics for:
  - Total records collected
  - Unique aircraft detected
  - Countries detected
- Aircraft count by country (bar chart)
- Altitude vs velocity analysis (scatter plot)
- Live aircraft map visualization using Folium
- Data collection focused on the Perak airspace region

---

## System Architecture
1. **Data Source Layer**  
   OpenSky Network API provides real-time aircraft state vectors.

2. **Data Acquisition Layer**  
   `collector.py` sends API requests periodically and retrieves aircraft data within the Perak bounding box.

3. **Data Storage Layer**  
   The data is stored in a local SQLite database (`flights.db`).

4. **Data Analytics & Visualization Layer**  
   `app.py` reads the stored data and displays:
   - KPIs
   - Data tables
   - Charts
   - Interactive map

---

## Technology Stack
- **Programming Language:** Python
- **Data Source:** OpenSky Network API
- **Database:** SQLite
- **Dashboard Framework:** Streamlit
- **Visualization:** Plotly, Folium
- **Data Handling:** Pandas
- **HTTP Requests:** Requests

---

## Project Structure
```text
UTP-IoT-data-acquisition-analytic-system-aircraft-Project/
│
├── app.py
├── collector.py
├── flights.db
├── requirements.txt
├── .gitignore
└── README.md

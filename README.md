🏥 MedFinder — Pharmacy & Medicine Locator

This project is a full-stack Django web application that helps users find medicines and locate pharmacies with real-time mapping using Leaflet.js and OpenStreetMap. Pharmacy owners can manage their medicine inventory and update their pharmacy's location for accurate map display.


📌 Objective

To create a platform where:

Users can search for medicines and find nearby pharmacies.

Pharmacy Owners can:

Manage medicine inventory.

Update pharmacy location via an interactive map.

Be discoverable on a global/Nepal-focused pharmacy map.

This project demonstrates my skills in:

Django backend development

REST API creation

Map integration (Leaflet.js + OpenStreetMap)

Frontend with Tailwind CSS

Database-driven location mapping

🚀 What This Project Includes

Pharmacy Registration & Login

Medicine Inventory Management

Interactive Map View showing all pharmacies with location pins

Pharmacy Location Update Feature using draggable Leaflet marker

API endpoint for pharmacy data in JSON (consumed by Leaflet)

Tailwind CSS styling for a responsive UI

🏗️ Tech Stack
Purpose	Tool / Library
Backend	Django (Python)
Frontend	Tailwind CSS
Maps	Leaflet.js + OpenStreetMap
Database	SQLite (default, can be replaced with PostgreSQL)
API	Django REST Framework
Deployment	Compatible with PythonAnywhere / Heroku
📊 Key Features

Search Medicines by name.

Find Pharmacies that stock a particular medicine.

Interactive Map for all approved pharmacies.

Owner Dashboard for adding medicines & editing stock.

Location Update Tool for precise pharmacy positioning.

🗂️ Files Included
medfinder/
├── medfinder/                # Main Django project folder
├── pharmacy/                 # App handling pharmacy & medicine logic
│   ├── templates/            # HTML templates (dashboard, maps, etc.)
│   ├── static/                # Tailwind CSS, JS, images
│   ├── views.py               # Core backend logic
│   ├── urls.py                # App URL routes
│   └── models.py              # Database models
├── manage.py
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

🔧 How to Run Locally

Clone this repo:

git clone https://github.com/YOUR_USERNAME/medfinder.git
cd medfinder


👤 Author

Sabina Sangraula — Aspiring Full-Stack Developer

🤝 Why I Built This

To create a real-world health service tool that combines:

Django backend skills

Interactive mapping

API development

Clean UI/UX with Tailwind
📬 Let's Connect Feel free to reach out via GitHub or LinkedIn if you'd like to discuss this project or explore how I can contribute to your team.

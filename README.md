# Campus Event Management

A Python / Flask coursework project with a refreshed responsive web interface.
Explore campus events, manage registrations, and review participation from an
administrator dashboard. The web version uses SQLite; the separate console
version is not included in this folder.


## Run locally on Windows

Requires Python 3.10 or newer.

```powershell
cd Campus_Event_Management
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:5000**. Stop the server with `Ctrl+C`.
A sample `database.db` from the original project is included. Existing records
were retained. If using a fresh folder without a database, initialize it first:

```powershell
.venv\Scripts\python.exe init_db.py
```

The initializer stops if the database already exists; it does not reset data.
On macOS/Linux, use `python3 -m venv .venv` and `.venv/bin/python` in place of
`.venv\Scripts\python.exe`.

## Demo accounts

The original classroom sign-in flow uses a **User ID only**:

- `admin` — administrator
- `student1` / `student2` — student

You can also create a student account from **Create account**. This remains a
local classroom demonstration; password authentication was not added as part
of the visual redesign.

## Live Demo

🌐 [Open Campus Event Management](https://campus-event-management-web.onrender.com)

A responsive Flask and SQLite web application deployed on Render.
Browse campus events, register for activities, and manage registrations.

Note: The free demo may take about a minute to load after inactivity.

## Features

- Event catalogue with search by name or location and date status badges.
- Event details, registration availability, duplicate and capacity checks.
- Student registrations with cancellation.
- Administrator event creation, editing, and deletion.
- Statistics with registration comparisons, capacity bars, and recent activity.
- Responsive sidebar, mobile navigation, accessible labels, and keyboard focus.

## Interface changes

- Consistent forest-green / mint palette and local system fonts.
- New overview, event cards, forms, account screens, tables, and dashboard.
- Self-contained CSS, JavaScript, and SVG icons: no Bootstrap or Chart.js CDN
  requests are needed by the redesigned interface.
- CSS bar charts show actual database values and remain available offline.
- Administrator controls are hidden from student and visitor navigation.
- Success screens provide an explicit return link instead of a timed redirect.

Small supporting fixes make database paths independent of the current directory,
return named SQLite rows to templates, and make statistics queries compatible
with the provided database and `schema.sql`.

## Project structure

```text
Campus_Event_Management/
  app.py                 Flask routes and session flow
  database.py            SQLite queries
  database.db            Original sample data
  schema.sql             Schema for a fresh database
  init_db.py             Non-destructive first-time setup
  requirements.txt       Python dependency
  templates/             Jinja page templates and shared UI components
  static/css/style.css   Responsive design and layout
  static/js/app.js       Mobile menu and action confirmations
```

## Publishing the code on GitHub

Upload the files above, excluding `.venv`, `__pycache__`, temporary files, and any
private data. The included `.gitignore` handles common local artifacts. Screenshots
of the new interface can be added later under a `docs/` folder. This package does
not publish the website or push changes to any repository.

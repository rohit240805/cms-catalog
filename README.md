CMS + Public Catalog Platform

A production-ready CMS system for managing Programs → Terms → Lessons, supporting scheduled publishing and a public catalog API.
Deployed URLs

CMS Web App:
 https://chaishotsassignment.netlify.app

API Base URL:
 https://cms-catalog-api.onrender.com

API Docs (Swagger):
 https://cms-catalog-api.onrender.com/docs

Architecture:
<img width="1536" height="1024" alt="CMS Architecture" src="https://github.com/user-attachments/assets/4782b814-090a-48e3-bc7d-c2cae9c1fc18" />

Key Components:

Frontend: React + Vite (Netlify)
Backend: FastAPI (Render)
Auth: OAuth2 Password Flow + JWT
Database: PostgreSQL (Render)
Worker: Background process that auto-publishes scheduled lessons
Migrations: Alembic
Containers: Docker + Docker Compose

Local Setup
1️ Clone Repository
git clone https://github.com/rohit240805/cms-catalog
cd cms-catalog
2️ Run Locally with Docker
docker compose up --build

This starts:

Frontend
API
Worker
PostgreSQL

Database & Migrations:
  Migrations: Managed using Alembic
  Migration files live in: api/alembic/versions/
How migrations run
Automatically executed on container startup
Can be run manually: alembic upgrade head

Seed Script
Purpose : Creates sample users and data:
Admin
Editor
Viewer

How it runs
Automatically during API startup
Can be run manually: python app/seed.py

Default Users
admin@cms.com   / admin123
editor@cms.com  / editor123
viewer@cms.com  / viewer123

Worker / Scheduled Publishing
What the worker does: Runs continuously and Polls database every 30 seconds
Finds lessons where:
status = scheduled
publish_at <= current time 
Publishes them automatically

Deployment Note
Worker runs as a background thread inside the API process to avoid paid background services, while still guaranteeing scheduled publishing.

Demo Flow 
Step 1: Login as Editor
Email: editor@cms.com
Password: editor123

Step 2: Create Lesson
Create a program → term → lesson
Set lesson status to scheduled
Set publish_at to a future time

Step 3: Wait for Worker
Wait ~30 seconds after publish time

Step 4: Verify Published
Lesson status changes to published
Published lesson appears in Public Catalog

Features Summary:

JWT Authentication
Role-based access
Scheduled publishing
Public catalog API
Production deployments
Fully dockerized
Reproducible from scratch

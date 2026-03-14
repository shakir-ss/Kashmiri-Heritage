---
name: kashmiri-guide
description: Project-specific guide for the Kashmiri Dry Fruits e-commerce platform.
---

# Kashmiri Dry Fruits - Project Guide

This skill provides context and standards for the Kashmiri Dry Fruits e-commerce project.

## Project Vision
A premium, scalable, and high-performance e-commerce platform specializing in Kashmiri products (Dry Fruits & Handicrafts). The architecture focuses on performance, security, and organic aesthetics.

## Technical Standards
- **Frontend:** Vue.js 3 (Composition API), Vite, Pinia, Vanilla CSS (Premium/Organic aesthetic).
- **Backend:** Python (Flask), RESTful APIs.
- **Database:** MySQL 8.0+.
- **Authentication:** JWT-based auth with RBAC (Admin/Customer).
- **Messaging:** Twilio/WhatsApp Business API for order flow.
- **Payments:** Razorpay/Stripe (Clean API-first integration).

## Project Structure
- `backend/`: Flask application, models, routes, and migrations.
- `frontend/`: Vue.js application, components, stores, and views.
- `docs/`: Project documentation and guides.

## Workflows
- Always use TDD (Test-Driven Development) for new features.
- Ensure all API endpoints are tested with `Invoke-RestMethod` (PowerShell).
- Maintain clean code following the standards in `conductor/code_styleguides/`.

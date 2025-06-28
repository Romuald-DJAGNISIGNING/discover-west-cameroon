# Discover West Cameroon – Backend

A Django RESTful backend for the *Discover West Cameroon* project, integrating tourism, villages, festivals, reviews, quizzes, tutorials, bookings, payments, user management, notifications, support, and more.  
The platform aims to showcase, preserve, and celebrate the rich culture, languages, and natural wonders of the West Cameroon region through modern web technology.

---

## Features

- **Role-Based Dashboards**: Custom dashboards for Admin, Guide, Tutor, Learner, Visitor with deep analytics and actionable widgets.
- **Comprehensive API**: RESTful endpoints for villages, festivals, tourism, reviews, assignments, custom sessions, tutorials, quizzes, notifications, support, payments, bookings, reports, and more.
- **Payment Integration**: MTN Mobile Money, Orange Money, Stripe, PayPal – robust handling of transactions, bookings, payouts, receipts, and webhooks.
- **Widgets & Analytics**: Interactive statistics, featured content, maps, weather, reviews, leaderboards, assignments, session and payment summaries.
- **Public Pages**: Welcome, About, and Contact endpoints with featured regional content.
- **Internationalization (i18n)**: All user-facing text is translatable via Django’s `gettext`.
- **Role-Based Permissions**: Each user role only sees and can edit their relevant data; strict admin controls.
- **Fully Automated Testing**: Extensive API coverage in `tests.py`.

---

## Requirements

- Python 3.9+
- Django 4.x+
- Django REST Framework
- django-cors-headers (for frontend integration)
- Pillow (for image uploads)
- Stripe, PayPal, requests (for payment backends)
- [Other requirements as per `requirements.txt`]

---

## Installation

1. **Clone the repo**
    ```sh
    git clone https://github.com/Romuald-DJAGNISIGNING/discover-west-cameroon.git
    cd discover-west-cameroon/backend
    ```

2. **Create a virtual environment and install dependencies**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure environment variables**  
   Copy `.env.example` to `.env` and set all secrets (database, payment keys, etc).

4. **Run migrations**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**
    ```sh
    python manage.py createsuperuser
    ```

6. **Collect static files (for production)**
    ```sh
    python manage.py collectstatic
    ```

---

## Running

- **Development**
    ```sh
    python manage.py runserver
    ```
    Visit `http://localhost:8000/api/dashboard/public/welcome/` for API check.

- **Production**  
  Run with gunicorn/uvicorn and a WSGI/ASGI server (see deployment docs).

---

## API

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for a complete list of endpoints, sample payloads, authentication, and permissions.

---

## Project Structure

- `dashboard/` – All dashboards, widgets, stats, public endpoints
- `villages/`, `festivals/`, `tourism/`, `reviews/`, `quizzes/`, `tutorials/`, `assignments/`, `custom_sessions/`, `users/`, `payments/`, `reports/`, `notifications/`, `support/` – Core apps
- `manage.py`, `requirements.txt`, `README.md`, `API_DOCUMENTATION.md`

---

## Testing

Run all tests:
```sh
python manage.py test
```

---

## Internationalization

- All APIs and classic views use `gettext` for translation.
- To add a language:
    ```sh
    python manage.py makemessages -l fr
    python manage.py compilemessages
    ```

---

## Payments

- Configure payment providers (MTN, Orange, Stripe, PayPal) in your `.env` or settings.
- Webhooks: `/api/payments/webhooks/stripe/`, `/api/payments/webhooks/paypal/`, etc.

---

## Contribution

- Fork, branch, and PR with clear commit messages.
- Follow PEP8 and Black formatting.
- Please add/expand tests for new features.

---

## License

MIT or as per your organization’s policy.

---

## Credits

- Project lead: Romuald DJAGNISIGNING
- [Other contributors and collaborators]

---

## Contact

- Email: contact@discoverwestcameroon.com
- [See `/api/dashboard/public/contact/` for more]

---

*Discover West Cameroon – Building the bridge between heritage and technology.*
# Discover West Cameroon

🌍 **Project:** Discover West Cameroon  
A cultural and educational booking platform for exploring the traditions and heritage of the West Region of Cameroon.

---

## Features

- User, guide, tutor, admin, and visitor dashboards
- Cultural events, festivals, and tourism booking
- Online learning, quizzes, tutorials, assignments
- In-app payments (Orange Money, MTN MoMo, Credit Card, PayPal)
- Location APIs, notifications, support, analytics
- Full i18n (English, French)
- Modern Django REST backend, ready for frontend integration

---

## Getting Started

1. **Clone the repo:**
   ```sh
   git clone https://github.com/Romuald-DJAGNISIGNING/discover-west-cameroon.git
   cd discover-west-cameroon/backend
   ```

2. **Create a virtual environment and install dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env` and update values

4. **Apply migrations and create superuser:**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the admin:**
   - Visit [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Folder Structure

- `backend/` - Django project and apps
- `frontend/` - (to be added) React/Vue/Next.js frontend

---

# Dashboard App — Discover West Cameroon

This Django app provides a robust, extensible dashboard backend with:
- Modular, role-based dashboards (Admin, Visitor, Learner, Guide, Tutor, Welcome)
- Widgets, notifications, statistics, feedback, and booking analytics
- DRF API endpoints (for all dashboard features)
- Admin interface for all dashboard models
- Signals for real-time stats updating
- Translation-ready and production-quality code

## Directory Structure

```
dashboard/
  admin.py
  apps.py
  backends.py
  models.py
  serializers.py
  signals.py
  tests.py
  urls.py
  urls_role_dashboards.py
  views.py
  views_role_dashboards.py
  README.md
```

## Usage & Integration

- Plug this app into your Django project’s `INSTALLED_APPS`.
- Include `dashboard/urls.py` in your main `urls.py`.
- Extend dashboard logic by connecting to other apps (`payments`, `tourism`, `events`, etc.) in the role-based dashboards.
- Use the admin site for analytics and content/notification management.

## Customization

- Expand role dashboards (`views_role_dashboards.py`) with real data from your other apps.
- Add new widgets, stats, and integrations as your platform grows.
- Use signals for new types of stats and analytics.

## Testing

- Run `python manage.py test dashboard` to ensure all endpoints and logic are working.
- Add more tests as your business logic evolves.

## Next Steps

- Integrate with the payments app for real-time booking/payment stats and features.
- Integrate with the locations app for region-specific dashboards.
- Connect to tourism, events, and assignments for richer analytics.
- Add real widgets and notification types for user engagement.

## Internationalization

- Strings are wrapped in `gettext_lazy` for translation.
- Run `django-admin makemessages` and `compilemessages` for updates.

---

**You are ready to deploy and build a frontend on this API!**

## Contributing

Pull requests are welcome! Please open an issue for discussion first.

---
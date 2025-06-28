# Discover West Cameroon Platform – Full API Documentation

This document provides a comprehensive overview of **all REST API endpoints** for your backend, grouped by app and including authentication, permissions, and sample payloads.  
Endpoints follow the convention `/api/<app>/<resource>/` unless otherwise stated. Use the provided routers and role dashboards as entry points.

---

## Table of Contents

1. [Authentication & Users](#authentication--users)
2. [Dashboard](#dashboard)
3. [Assignments](#assignments)
4. [Custom Sessions](#custom-sessions)
5. [Festivals](#festivals)
6. [Notifications](#notifications)
7. [Payments](#payments)
8. [Quizzes](#quizzes)
9. [Reports](#reports)
10. [Reviews](#reviews)
11. [Support](#support)
12. [Tourism](#tourism)
13. [Tutorials](#tutorials)
14. [Villages](#villages)

---

## 1. Authentication & Users

### Authentication

- **POST /api/auth/login/**  
  `{"email": "...", "password": "..."}`  
  → `{"token": "..."}`

- **POST /api/auth/logout/**  
  → `204 No Content`

- **POST /api/auth/register/**  
  `{"email": "...", "password": "...", ...}`  
  → `201 Created`

### Users

- **GET /api/users/**  
  List users (admin only)

- **GET /api/users/me/**  
  Get your own profile

- **PATCH /api/users/me/**  
  Update your profile

- **GET /api/users/{id}/**  
  Retrieve a user (admin/staff)

- **PATCH /api/users/{id}/**  
  Update a user (admin/staff)

- **DELETE /api/users/{id}/**  
  Delete a user (admin/staff)

---

## 2. Dashboard

### General

- **GET /api/dashboard/role/admin/**  
  Admin dashboard (stats, widgets, recent, cross-app summaries)

- **GET /api/dashboard/role/visitor/**  
  Visitor dashboard (recommendations, activities, widgets)

- **GET /api/dashboard/role/learner/**  
  Learner dashboard (tutorials, quizzes, assignments, payments)

- **GET /api/dashboard/role/tutor/**  
  Tutor dashboard (my bookings, earnings, reviews, assignments)

- **GET /api/dashboard/role/guide/**  
  Guide dashboard (bookings, earnings, reviews, assignments)

- **GET /api/dashboard/public/welcome/**  
  Welcome page widgets & featured content

- **GET /api/dashboard/public/about/**  
  About Discover West Cameroon

- **GET /api/dashboard/public/contact/**  
  Contact page & support links

### Widgets, Stats, Logs

- **GET /api/dashboard/widgets/**  
  List/create widgets (role-based)

- **POST /api/dashboard/widgets/**  
  Create widget  
  `{"widget_type":"stat","config":{...}}`

- **GET /api/dashboard/widgets/my_widgets/**  
  List my widgets

- **GET /api/dashboard/activity-logs/**  
  List user or all activity logs

- **GET /api/dashboard/activity-logs/my_recent/**  
  10 latest logs for the user

- **GET /api/dashboard/daily-stats/**  
  (Admin only) Site statistics by day

- **GET /api/dashboard/dashboard-stats/**  
  (Admin only) List custom dashboard stats

- **GET /api/dashboard/dashboard-stats/summary/**  
  (Admin only) Key numbers (users, bookings, reviews, etc)

- **GET /api/dashboard/feedback-summaries/**  
  (Admin only) Feedback analytics

- **GET /api/dashboard/system-notifications/**  
  List/CRUD system-wide notifications

- **POST /api/dashboard/system-notifications/{id}/mark_read/**  
  Mark notification as read

---

## 3. Assignments

- **GET /api/assignments/**  
  List my assignments (role/permission-based)

- **POST /api/assignments/**  
  Create assignment  
  `{"user":1,"title":"...","due_date":"...","status":"pending"}`

- **GET /api/assignments/{id}/**  
  Retrieve assignment

- **PATCH /api/assignments/{id}/**  
  Update assignment

- **DELETE /api/assignments/{id}/**  
  Delete assignment

---

## 4. Custom Sessions

- **GET /api/custom_sessions/**  
  List sessions (role/permission-based)

- **POST /api/custom_sessions/**  
  Create session  
  `{"title":"...","date":"...","users":[1,2,3]}`

- **GET /api/custom_sessions/{id}/**  
  Retrieve session

- **PATCH /api/custom_sessions/{id}/**  
  Update session

- **DELETE /api/custom_sessions/{id}/**  
  Delete session

---

## 5. Festivals

- **GET /api/festivals/**  
  List/search all festivals

- **POST /api/festivals/**  
  (Admin) Create festival

- **GET /api/festivals/{id}/**  
  Retrieve festival

- **PATCH /api/festivals/{id}/**  
  Update festival

- **DELETE /api/festivals/{id}/**  
  Delete festival

- **GET /api/festivals/recent/**  
  Recent festivals

- **GET /api/festivals/{id}/reviews/**  
  Festival reviews

---

## 6. Notifications

- **GET /api/notifications/**  
  List my notifications

- **POST /api/notifications/mark_read/**  
  Mark all as read

- **GET /api/notifications/unread_count/**  
  Count unread notifications

---

## 7. Payments

### Methods

- **GET /api/payments/methods/**  
  List available payment methods

### Bookings

- **GET /api/payments/bookings/**  
  List my bookings

- **POST /api/payments/bookings/**  
  Create booking

### Transactions

- **GET /api/payments/transactions/**  
  List my transactions

- **POST /api/payments/transactions/**  
  Create transaction

- **POST /api/payments/initiate/{transaction_id}/**  
  Initiate payment for a transaction

- **GET /api/payments/check-status/{transaction_id}/**  
  Check transaction status

- **POST /api/payments/transactions/{id}/cancel/**  
  Cancel a transaction

### Receipts

- **GET /api/payments/receipts/**  
  List my receipts

### Payouts

- **GET /api/payments/payouts/**  
  List payouts (admin or myself)

- **POST /api/payments/payouts/**  
  (Admin) Create payout (marks as paid)

---

## 8. Quizzes

- **GET /api/quizzes/**  
  List quizzes

- **GET /api/quizzes/{id}/**  
  Retrieve quiz

- **POST /api/quizzes/{id}/submit/**  
  Submit answers

- **GET /api/quizzes/results/**  
  List my quiz results

- **GET /api/quizzes/results/{id}/**  
  Retrieve one result

---

## 9. Reports

- **GET /api/reports/**  
  List my reports

- **POST /api/reports/**  
  Create a report

- **GET /api/reports/{id}/**  
  Retrieve a report

- **PATCH /api/reports/{id}/**  
  Update (admin/owner)

- **DELETE /api/reports/{id}/**  
  Delete

---

## 10. Reviews

- **GET /api/reviews/**  
  List reviews

- **POST /api/reviews/**  
  Create review

- **GET /api/reviews/{id}/**  
  Retrieve review

- **PATCH /api/reviews/{id}/**  
  Update review

- **DELETE /api/reviews/{id}/**  
  Delete review

---

## 11. Support

- **GET /api/support/tickets/**  
  List my tickets

- **POST /api/support/tickets/**  
  Create ticket

- **GET /api/support/tickets/{id}/**  
  Retrieve ticket

- **PATCH /api/support/tickets/{id}/**  
  Update ticket

- **DELETE /api/support/tickets/{id}/**  
  Delete ticket

---

## 12. Tourism

- **GET /api/tourism/attractions/**  
  List/search all attractions

- **POST /api/tourism/attractions/**  
  (Admin/Guide) Create attraction

- **GET /api/tourism/attractions/{id}/**  
  Retrieve attraction

- **PATCH /api/tourism/attractions/{id}/**  
  Update attraction

- **DELETE /api/tourism/attractions/{id}/**  
  Delete attraction

---

## 13. Tutorials

- **GET /api/tutorials/**  
  List/search tutorials

- **POST /api/tutorials/**  
  (Tutor/Guide/Admin) Create tutorial

- **GET /api/tutorials/{id}/**  
  Retrieve tutorial

- **PATCH /api/tutorials/{id}/**  
  Update

- **DELETE /api/tutorials/{id}/**  
  Delete

- **POST /api/tutorials/{id}/add_comment/**  
  Add a comment

- **GET /api/tutorials/categories/**  
  List categories

---

## 14. Villages

- **GET /api/villages/**  
  List/search all villages

- **POST /api/villages/**  
  (Admin) Create village

- **GET /api/villages/{id}/**  
  Retrieve village

- **PATCH /api/villages/{id}/**  
  Update

- **DELETE /api/villages/{id}/**  
  Delete

---

## Permissions & Auth Notes

- Most endpoints require authentication (token or session).
- Some endpoints (e.g., `public/welcome`, `public/about`, `public/contact`) are public.
- Admin-only endpoints are marked above.
- Permissions are role-based: learners, guides, tutors, admin, visitor, etc.

---

## Pagination, Filtering, Ordering

- List endpoints support `?page=`, `?search=`, and ordering parameters (e.g., `?ordering=-created_at`).

---

## Typical Response Examples

### Successful List

```json
{
  "count": 2,
  "results": [
    {"id": 1, "title": "Ngouon", "description": "..."},
    {"id": 2, "title": "Mpoo", "description": "..."}
  ]
}
```

### Error

```json
{
  "detail": "Not authorized as a tutor."
}
```

---

## Webhooks

- **/api/payments/webhooks/stripe/**  
- **/api/payments/webhooks/paypal/**  
- **/api/payments/webhooks/mtn/**  
- **/api/payments/webhooks/orange/**  
_For payment provider integrations. POST only. No authentication required, only for provider callbacks._

---

## Classic Views

You may also have classic Django views for dashboards, support, etc., at `/dashboard/classic/`, `/support/classic/`, etc.

---

## Internationalization

All user-facing messages and fields support translation (`gettext`).

---

## Miscellaneous

- All endpoints return appropriate HTTP status codes.
- All APIs are RESTful and documented.
- All cross-app data is integrated in dashboards and widgets.

---

**For full OpenAPI/Swagger or Postman collection, you can auto-generate from your DRF routers.**
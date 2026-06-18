# Library Management System (Secure Web Application)

## 1. Project Description
A secure Django-based library management system implementing OWASP Top 10 
controls, RBAC, audit logging, and secure coding practices.

## 2. Installation Steps
1. Clone the repository: `git clone <repo-url>`
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your own SECRET_KEY
6. Run migrations: `python manage.py migrate`
7. Run server: `python manage.py runserver`

## 3. Security Features Summary
- Argon2 password hashing
- CSRF protection enabled
- Session timeout (30 min)
- RBAC (Admin / User roles)
- Audit logging (login attempts, CRUD actions)
- Input validation via Django Forms
- Custom error pages (400/403/404/500)
- Secure HTTP headers (X-Frame-Options, X-Content-Type-Options)

## 4. How to Run the App
python manage.py runserver
Then visit http://127.0.0.1:8000/

## 5. Dependencies
See `requirements.txt` for full list. Key packages:
- Django 5.0.1
- argon2-cffi
- whitenoise

## 6. Screenshots
<img width="1600" height="898" alt="image" src="https://github.com/user-attachments/assets/edacc284-2c8d-4b5f-9335-808989077a5b" />
Login page

<img width="1600" height="839" alt="9d2aaba8-d32b-4249-9192-90e7a2255a53" src="https://github.com/user-attachments/assets/38be0d64-c726-4d28-8f36-726209a23ed1" />
Login failed page

<img width="1600" height="798" alt="image" src="https://github.com/user-attachments/assets/65a23720-f6b1-406b-867b-e8b95ddcb97d" />
Dasbboard

<img width="1600" height="758" alt="image" src="https://github.com/user-attachments/assets/5379c9c9-1bef-42fe-a44e-0815f6876a1f" />
iventory list 

<img width="1600" height="799" alt="ec3a437c-8fee-42f7-b6bd-89aff04c0890" src="https://github.com/user-attachments/assets/3a6f860d-da41-4943-81e3-8a59951ca249" />
Iventory add item

<img width="1600" height="794" alt="9a3b2312-d162-46bd-ac82-8890072bb264" src="https://github.com/user-attachments/assets/f34c4ca8-a137-4402-a37d-ba8eacae1077" />
iventory edit item

<img width="1600" height="747" alt="1dc1e160-1bbc-4615-a867-9585dfe11f75" src="https://github.com/user-attachments/assets/a364cc79-6185-49dc-a998-7cc59ba2528b" />
Profile page

<img width="1600" height="822" alt="7e6a13c0-8468-403a-bb73-f97f67d8473a" src="https://github.com/user-attachments/assets/e757bb5b-42de-4c27-96cc-8965b4863587" />
Audit log page

<img width="1600" height="853" alt="image" src="https://github.com/user-attachments/assets/5f4703a0-d557-49a5-be52-60f7089a8907" />
404 page

<img width="1600" height="790" alt="64390508-48d6-4340-b302-18797879b985" src="https://github.com/user-attachments/assets/a54b1cce-3ab6-4d99-bb49-249b50d56491" />
Book module

<img width="1600" height="790" alt="e9b27a90-effd-44a3-b008-47fa3127ba19" src="https://github.com/user-attachments/assets/40e5a3b3-ba00-4a4d-8a88-4e1bae205aca" />
members module

Manual Render deployment checklist

1) On Render dashboard
   - New → Web Service → Connect to GitHub
   - Select repository: ChakraWarrior35/BHOJANLY, branch: main
   - Use `render.yaml` (recommended) or set:
     - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - Start command: `gunicorn Bhojanly.wsgi:application --bind 0.0.0.0:$PORT`

2) Environment variables (Service → Environment)
   - SECRET_KEY = <paste secure value generated earlier>
   - DEBUG = false
   - ALLOWED_HOSTS = your-app.onrender.com
   - If using Managed Postgres, attach DB and ensure `DATABASE_URL` is set
   - Optionally: SECURE_SSL_REDIRECT = true

3) Deploy & monitor
   - Click Deploy. Watch logs for build errors.

4) Post-deploy (run in Render Shell)
   - python manage.py migrate
   - python manage.py createsuperuser

5) Verify
   - Visit the URL, test admin and pages, confirm static assets load.

Notes
- Do not commit secrets. Use `env.sample` as reference.
- Prefer Postgres (Render Managed Postgres). Do not rely on SQLite in production.

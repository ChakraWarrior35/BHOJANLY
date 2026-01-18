Render deployment steps

1. Connect your GitHub repo to Render
   - Go to https://dashboard.render.com and create a new Web Service.
   - Choose your repo `ChakraWarrior35/BHOJANLY` and branch `main`.
   - Render will detect Python; set the build and start commands (or use `render.yaml`).

2. Set environment variables in Render (Settings → Environment):
   - `SECRET_KEY` = (generate a secure random value)
   - `DEBUG` = false
   - `ALLOWED_HOSTS` = your-app.onrender.com
   - If using Postgres, attach a Managed Postgres instance and Render will provide `DATABASE_URL`.
   - Optionally set `SECURE_SSL_REDIRECT=true`.

3. Build & Deploy
   - Render will run `pip install -r requirements.txt` and the `buildCommand` from `render.yaml`.
   - `collectstatic` runs during build (render.yaml configured it).

4. Post-deploy
   - Visit the service URL and verify the site is up.
   - If using the admin, create a superuser via Render Shell or locally and migrate the DB.

Local commands (for testing/development):

```powershell
# install pinned deps
& "D:/MY WORK/Bhojanly/.venv/Scripts/python.exe" -m pip install -r requirements.txt
# collect static locally
& "D:/MY WORK/Bhojanly/.venv/Scripts/python.exe" manage.py collectstatic --noinput
# run migrations
& "D:/MY WORK/Bhojanly/.venv/Scripts/python.exe" manage.py migrate
# create superuser
& "D:/MY WORK/Bhojanly/.venv/Scripts/python.exe" manage.py createsuperuser
# run dev server
& "D:/MY WORK/Bhojanly/.venv/Scripts/python.exe" manage.py runserver
```

Notes
- Do NOT commit real secrets. Use `env.sample` as reference only.
- If you want me to create the Render service using `render.yaml`, I can provide exact steps or a script, but I cannot perform the dashboard actions without your Render account access.

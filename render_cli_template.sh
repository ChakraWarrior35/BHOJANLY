#!/usr/bin/env bash
# Template: use Render CLI to create a web service for this repo.
# Prereqs:
#  - Install Render CLI: https://render.com/docs/cli
#  - Login: `render login` (or set RENDER_API_KEY env var)
# Usage: edit variables below and run: ./render_cli_template.sh

set -euo pipefail

SERVICE_NAME="Bhojanly-web"
REPO_URL="https://github.com/ChakraWarrior35/BHOJANLY"
BRANCH="main"
REGION="oregon"  # choose appropriate region
PLAN="free"

BUILD_COMMAND="pip install -r requirements.txt && python manage.py collectstatic --noinput"
START_COMMAND="gunicorn Bhojanly.wsgi:application --bind 0.0.0.0:$PORT"

# Create service (non-interactive). This command may prompt for confirmation.
# If your Render CLI supports `render services create web ...` use that; otherwise create via dashboard.

echo "Creating Render service (template)..."
render services create web --name "$SERVICE_NAME" --repo "$REPO_URL" --branch "$BRANCH" --region "$REGION" --plan "$PLAN" --build-command "$BUILD_COMMAND" --start-command "$START_COMMAND"

echo "Service create command finished. Check Render dashboard for service status."

echo "Once service is created, set environment variables (either in dashboard or with CLI):"
echo "  render services env set <SERVICE_ID> SECRET_KEY=your_secret_key"
echo "  render services env set <SERVICE_ID> DEBUG=false"
echo "  render services env set <SERVICE_ID> ALLOWED_HOSTS=your-app.onrender.com"
echo "If using Postgres, attach a Managed Postgres and set DATABASE_URL accordingly."

echo "After deploy, run migrations via Render Shell or CLI:"
echo "  render shell <SERVICE_ID> -- python manage.py migrate"
echo "  render shell <SERVICE_ID> -- python manage.py createsuperuser"

exit 0

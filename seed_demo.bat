@echo off
echo Applying migrations...
docker compose exec web python manage.py migrate

echo Seeding demo data...
docker compose exec web python manage.py seed_demo

echo Done!
pause

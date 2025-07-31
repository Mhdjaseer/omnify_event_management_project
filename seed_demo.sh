#!/bin/bash

#run this in bash for demo data creations
echo "Applying migrations..."
docker compose exec web python manage.py migrate

echo "Seeding demo data..."
docker compose exec web python manage.py seed_demo

echo "Done!"

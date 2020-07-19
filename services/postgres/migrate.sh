
# Run the migrations for each database schema

sleep 10 # postgres might not be responding yet

python /usr/src/app/shared_functions/run_migrations.py

python /usr/src/app/user/run_migrations.py
python /usr/src/app/authorizer/run_migrations.py # may have references to user someday 
python /usr/src/app/room/run_migrations.py # references to user

while :
do
  sleep 10
done

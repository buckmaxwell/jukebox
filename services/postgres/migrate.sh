
# Run the migrations for each database schema

sleep 10 # postgres might not be responding yet
python /usr/src/app/authorizer/run_migrations.py
while :
do
  sleep 10
done
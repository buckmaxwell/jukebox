
# Run the migrations for each database schema

sleep 10 # postgres might not be responding yet

python /usr/src/app/shared_functions/run_migrations.py


# TODO: some data in these tables references data in other schemas. In that
# case is a foreign key appropriate? If we use one, what are we losing?
#
# currently I am thinking that a single database should certainly suffice, so
# no need to worry about managing data across databases.
#
# I feel however that and that foreign keys across schemas are inappropriate to
# enforce.
#
# Take this example. There are two services, profile_writer and user_writer.
# The profile has a user. THe uuid gets generated for the user, and the
# profile_writer and user_writer both run asynchrously. The user id is set by
# uuid4 before either job. If an actuall constraint existed, the profile
# couldn't be written before the user existed.

# I believe certain services should, as a matter of policy, read only from schemas aside from theirs. 


python /usr/src/app/user/run_migrations.py
python /usr/src/app/authorizer/run_migrations.py # may have references to user someday 
python /usr/src/app/room/run_migrations.py # references to user... TODO: what is the rule for microservices on this
python /usr/src/app/player/run_migrations.py # references to room

while :
do
  sleep 10
done

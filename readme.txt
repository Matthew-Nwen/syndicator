Objective: Automate reposting of events onto websites

(Satisfied) Requirements:
1. admin panel to add rows to database
2. backend cron job to run publishing script every hour
3. Publish events to EventBrite

To run locally:
1. Install dependencies using virtualenv
2. Upload a credentials.py file with app keys in the syndicator folder!
2. Use the command "python manage.py runserver" to start a local instance
3. Navigate to the "localhost:8000/admin" to see the admin panel.

Notes:
While all of the framework of this web application is set up, I didn't have
enough time to actually get API keys to make posts onto the five websites I found.
That's entirely my fault--moving apartments took up too much of the time I wanted
to spend on finishing this project. Regardless, I had a fun time researching,
planning, and executing this project.

To speed up checking the expensive database query for all new events, I decided
to create another table which only gets populated on the creation of an event.
This table would probably be stored in memory for the backend process to quickly
find which entries to run on. One thing to note is that updating the reposts
would be tricky with this schema!

With my extension on the assignment, I had time to look into acquiring API keys
and interacting with external sites. What I discovered was that not every API is
built up to the same standard (especially older ones!), with ease of use being
dramatically different between different systems. Regardless, I managed to get
posting on eventbrite working! Real world coding runs into problems that don't
come up in an academic setting...

Objective: Automate reposting of events onto websites

(Satisfied) Requirements:
1. admin panel to add rows to database
2. backend cron job to run publishing script every hour

To run:
1. Install dependencies using virtualenv
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

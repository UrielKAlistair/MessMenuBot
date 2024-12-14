# MessMenuBot
A flask based web server to automatically send that day's mess menu, daily, at 6 AM.

The code is hosted here: https://replit.com/@arvindanuk/waserver
The server is pinged at a set frequency by uptimerobot, enabling the code to function in this form.

The initial version of the server was set to function automatically, without having to rely on pings to activate a check of the time and trigger a message send if it was due.
However, since replit automatically shut down repls that were not being pinged for about an hour, my server died and could not function.   

Further, Since web servers are multi threaded, it was not possible to use conventional coding strategies to accomplish this feat: Some variables had to be global, to ensure multiple threads don't do contradictory things, [Future Me here: haha you sweet summer child, you can disable that behaviour in flask easily; Now that I know this, am I going to rewrite this? hell no. It works so it works.] and the contents of the variables were very quickly lost due to replit shutting down my server, even when I tried to ping it every minute.   
I learnt that any data that was needed across server responses deserves a dedicated storage. I used a text file to store the variable I wanted.   


In the end, I had to settle for this ping based solution. It's rather optimal, dare I say. The only issue is the external reliance on pings.
[Honestly, not bad. This is kind of like a primitive version of celery beats.]

main.py has the core server hosting code. send_msg.py defines a function to send a request to WhatsApp's api.

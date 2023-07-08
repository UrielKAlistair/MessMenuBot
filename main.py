from flask import Flask, request, send_file
from send_msg import send_msg
import datetime as dt
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # The terminal is flooded with messages if the log priority is not altered.

app = Flask(__name__)

time_txt = open('last_sent.txt', 'r')
last_sent = eval(time_txt.readline())
time_txt.close()

last_pinged = last_sent

def LOG(string):

  print(string)
  f = open('server_log.txt', 'a')
  f.write(string + '\n')
  f.close()

@app.route("/")
def main():

  global last_sent
  global last_pinged

  ping_del_t = dt.datetime.now() - last_pinged
  send_del_t = dt.datetime.now() - last_sent
  last_pinged = dt.datetime.now()
  
  LOG(f'[{dt.datetime.now()}] ##### GOT PINGED WITH A {request.method} REQUEST #####')
  LOG(f"It\'s been {ping_del_t} since the last ping")
  LOG(f"It\'s been {send_del_t} since the last time messages were sent. DAYS:{send_del_t.days}")
  
  # If it is asked for an image by whatsapp's api. This is the action as the image server.
  args = request.args
  if args.__len__() == 3:

    LOG(f"[{dt.datetime.now()}] Whatsapp API is asking for the menu")
    try:
      day = args.get('day')
      days = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday'
      ]
      week = args.get('week')
      mess = args.get('mess')
      weeks = ['1', '2']

      if day in days and week in weeks:
        LOG("Responding with image.")
        return send_file(f"{mess}/{day}{week}.png", mimetype='image/png')
      else:
        return 'Invalid Day/Week'

    except:
      return "Something\'s messed up"

  elif send_del_t.days >= 1:

    # Last seen is always 6 am on some day. If the delta exceeds a day, the message is sent.

    now = dt.datetime.now()
    last_sent = dt.datetime(now.year, now.month, now.day, 0, 30, 0)

    time_txt = open('last_sent.txt', 'w')
    time_txt.write(f"dt.datetime({now.year},{now.month},{now.day},0,30,0)")
    time_txt.close()

    bot_no = os.environ['bot_ph_no_id_1']
    access_token = os.environ['access_token_1']

    # send_msg(access_token, bot_no, os.environ['ph_no_uk'],'Vindhya_North', double=True)
    # send_msg(access_token, bot_no, os.environ['ph_no_uk'],'Vindhya_South', double=True)

    send_msg(access_token, bot_no, os.environ['ph_no_uk'], 'SRR')
    send_msg(access_token, bot_no, os.environ['ph_no_amma'], 'SRR')
    send_msg(access_token, bot_no, os.environ['ph_no_arnav'], 'SRR')
    send_msg(access_token, bot_no, os.environ['ph_no_buv'], 'SRR')

    send_msg(access_token, bot_no, os.environ['ph_no_vk'], 'Vindhya_South')
    LOG("[{dt.datetime.now()}] ##### MESSAGES SENT #####")
    
    if now.day == 1:  # clear the log on the first of every month
      f = open('server_log.txt', 'w')
      f.close()
      LOG(f'Cleared Log on {now.date()}')

    return 'Message Sent'

  else:
    return 'Ping Successful'

LOG('!!!!! BOOTING SERVER !!!!!')
app.run(host='0.0.0.0', port=5000)

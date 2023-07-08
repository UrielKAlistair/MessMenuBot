import json
import requests
import datetime
import time


def send_msg(access_token,
             phone_number_id,
             recipient_phone_number,
             mess,
             double=False):
              
  url = f"https://graph.facebook.com/v15.0/{phone_number_id}/messages"
  headers = {
    "Authorization": f"Bearer {access_token}",
    'Content-Type': 'application/json'
  }

  days = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
    'Sunday'
  ]
  
  week = int(1 + ((time.time() - 1677364200) // 604800) % 4)  # Counts wrt Feb 26 2023, 4 AM, Sunday

  if double:
    text = f"{week}. Here's the {mess.split('_')[-1]} menu. Enjoy the prior knowledge"
  else:
    text = str(week)

  day = days[datetime.datetime.today().weekday()]

  data = {
    'messaging_product': 'whatsapp',
    'to': recipient_phone_number,
    'type': 'template',
    'template': {
      'name':
      'daily_information',
      'language': {
        'code': 'en'
      },
      "components": [{
        "type":
        "header",
        "parameters": [{
          "type": "image",
          "image": {
            "link":
            f"https://waserver.arvindanuk.repl.co?week={(week-1)%2+1}&day={day}&mess={mess}"
          }
        }]
      }, {
        "type": "body",
        "parameters": [{
          "type": "text",
          "text": text
        }]
      }]
    }
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))

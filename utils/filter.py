def message_filter(message):
      message_date = message.split('.')
      message_time = message.split(':')
      if message not in 'cancel' and 'next' and 'back':
            return True


def check_message(message):
      message_date = message.split('.')
      message_time = message.split(':')
      try:
            if len(message_date) == 3 and int(message_date[0]) < 13 and int(message_date[1]) < 13:
                  return True
            elif len(message_time) == 2 and int(message_time[0]) < 24 and int(message_time[1]) < 60:
                  return True
            else:
                  return False
      except Exception:
            return False


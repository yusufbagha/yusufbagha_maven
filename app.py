from flask import Flask
from flask import request, jsonify
from datetime import datetime

# define app
app = Flask(__name__)

# in memory data store
all_appointments = []


# Gets Calendar Date
# expects: epoch timestamp
# returns: string
def calendar_date(timestamp):
  date = datetime.fromtimestamp(int(timestamp))
  return '{}/{}/{}'.format(date.month, date.day, date.year)


# Finds appointments for user
# expects: user_id
# returns: list
def appointments_for_user(user_id):
  return filter(lambda appointment: appointment['user_id'] == user_id, all_appointments)


# Checks if appointment exists for calendar day
# expects: user_id, epoch timestamp
# returns: boolean
def appointment_exists(user_id, timestamp):
  appointments = appointments_for_user(user_id)

  for appointment in appointments:
    appointment_timestamp = appointment["timestamp"]
    if calendar_date(timestamp) == calendar_date(appointment_timestamp):
      return True
  
  return False


# Creates appointment
# expects: user_id, epoch timestamp
def add_appointment(user_id, timestamp):
  return all_appointments.append({
    "user_id": user_id,
    "timestamp": int(timestamp)
  })


# Endpoint returns all appointments for user
# expects: user_id
# returns: list
@app.route('/', methods = ['GET'])
def get_appointments():
  user_id = request.args["user_id"]

  if not user_id:
      return 'missing user_id', 400
  
  return jsonify(appointments_for_user(user_id))


# Endpoint creates appointment
# expects: user_id, UTC date
# returns: boolean
@app.route('/', methods = ['POST'])
def create_appointment():
    user_id = request.args["user_id"]
    timestamp = request.args["timestamp"]

    # checks if fields are available
    if not user_id or not timestamp:
      return 'Missing timestamp or user_id', 400

    # checks if timestamp is a number
    try:
      int(timestamp)
    except:
      return 'Timestamp is not a number', 400 

    # checking if appointment already exists for date
    if appointment_exists(user_id, timestamp):
      return 'You already have an appointment that day', 400

    add_appointment(user_id, timestamp)

    return 'Appointment Created', 200


# run dev server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
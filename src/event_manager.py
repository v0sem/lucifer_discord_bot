#Solana made this https://github.com/solanav
from datetime import datetime, date, timedelta

MAX_DAYS_SHOW = 14
SEPARATOR = " "
EVENTS_FILE = "database/events.txt"

def format_error_message(correct_format):
		return ('El formato es "' + correct_format + '" perro')

def get_uid():
	with open(EVENTS_FILE, "r") as f:
		last_line = f.read().split("\n")[-2]
		last_uid = last_line.split(SEPARATOR)[0]

	return int(last_uid) + 1

def read_events():
	with open(EVENTS_FILE, "r") as f:
		data = f.read()
		data = data.split("\n")
		data.pop(-1)
		data = '\n'.join(data)

	return data

def pretty_events():
	events = read_events()

	data = ""

	data += ("\n[%s]\n" % datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
	data += ("\nThis and next week's events:\n")

	today = date.today()

	t_day = int(today.day)
	t_month = int(today.month)
	t_year = int(today.year)

	for event in events.split("\n"):
		try:
			name	= str(event.split(SEPARATOR)[1])
			day	= int(event.split(SEPARATOR)[2])
			month	= int(event.split(SEPARATOR)[3])
			year	= int(event.split(SEPARATOR)[4])

			event_date	= date(year = year, month = month, day = day)
			event_date_end	= today + timedelta(days = MAX_DAYS_SHOW)

			diff = event_date - today

			if (diff.days > 0 and diff.days < MAX_DAYS_SHOW):
				data += ("\t- %s es el dia %s, faltan %d dias\n" % (name, event_date.day, diff.days))

		except Exception as e:
			continue

	return data


def search_events_day(day):
	result = []
	data = read_events()
	data = data.split("\n")

	data.pop(0)
	data.pop(-1)

	for line in data:
		if line.split(" ")[2] == str(day):
			result.append(line)

	return '\n'.join(result)

def search_events_month(month):
	result = []
	data = read_events()
	data = data.split("\n")

	data.pop(0)
	data.pop(-1)

	for line in data:
		if line.split(" ")[3] == str(month):
			result.append(line)

	return '\n'.join(result)

def search_events_year(year):
	result = []
	data = read_events()
	data = data.split("\n")

	data.pop(0)
	data.pop(-1)

	for line in data:
		if line.split(" ")[4] == str(year):
			result.append(line)

	return '\n'.join(result)

def search_events_name(name):
	result = []
	data = read_events()
	data = data.split("\n")

	data.pop(0)
	data.pop(-1)

	for line in data:
		if str(name).lower() in line.split(" ")[1].lower():
			result.append(line)

	return '\n'.join(result)


def add_event(name, day, month, year):
	with open(EVENTS_FILE, "a") as f:
		f.write(str(get_uid()) + SEPARATOR +
			str(name) + SEPARATOR +
			str(day) + SEPARATOR +
			str(month) + SEPARATOR +
			str(year) + "\n")

	return

def del_event(uid):
	old_data = read_events()
	new_file = open(EVENTS_FILE, "w")

	for line in old_data.split("\n"):
		current_uid = line.split(SEPARATOR)[0]
		if current_uid != str(uid):
			new_file.write(line + "\n")

	new_file.close()

	reasign_uid()

	return

def reasign_uid():
	old_uid_data = read_events()
	new_file = open(EVENTS_FILE, "w")
	new_uid = 0

	for line in old_uid_data.split("\n"):
		old_data = line.split(SEPARATOR)
		old_data.pop(0)
		new_file.write(str(new_uid) + " " + ' '.join(old_data) + "\n")
		new_uid += 1

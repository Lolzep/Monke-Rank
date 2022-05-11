import json
import threading
import os

# Used to make sure that files are not open at multiple times
# "open" statements must wait until the current "open" statement is finished
# Must add "global file_lock" to all definitions that use an "open" statement
file_lock = threading.Lock()

def new_json_file(filename, name: str):
	global file_lock
	file_lock.acquire()
	with open(filename, "w"):
		pass
	file_lock.release()	

# Create a new json array while keeping the file_lock
def new_json_objects(filename, name: str):
	global file_lock
	new_template = {name:[]}
	file_lock.acquire()
	with open(filename, "w") as f:
		json.dump(new_template, f, indent=2)
	file_lock.release()

# Dump the data into json while keeping the file_lock
def json_dump(data):
	global file_lock
	file_lock.acquire()
	with open("users.json", "w") as f:
		json.dump(data, f, indent=2)
	file_lock.release()	

# Read the data from a json file while keeping the file lock
def json_read(filename):
	global file_lock
	file_lock.acquire()
	with open(filename, "r") as f:
		data = json.load(f)
	file_lock.release()
	return data

# Used to append new users into the users.json file, keep file_lock
def write_json(new_data, filename, name: str):
	global file_lock
	file_lock.acquire()
	with open(filename, "r+") as f:
		file_data = json.load(f)
		file_data[name].append(new_data)
		f.seek(0)
		json.dump(file_data, f, indent=2)
	file_lock.release()

# Adds new users to the master json file
# Finds the current user in the json file from discord context (message, reactions, etc.)
# Returns data: New .json file with modifyed values or the .json values, user: the current user object in the json file by user_id
async def update_user(main_id, main_user, key : str, dump_file: bool):
	global file_lock
	template = {"user_id": main_id, "name": main_user, "xp": 0, "level": 0, "role_id": 0, "messages": 0, "reactionsadded": 0, "reactionsrecieved": 0, "images": 0, "embeds": 0, "voice_call_hours":0, "invites":0, "special_xp":0}
	
	# Check if missing or empty, if so, create new file and/or run new_json
	try:
		if os.stat("users.json").st_size == 0:
			new_json_objects("users.json", "users")
	except FileNotFoundError:
		new_json_file("users.json", "users")
		if os.stat("users.json").st_size == 0:
			new_json_objects("users.json", "users")

	# Load initial users.json
	file_lock.acquire()
	with open("users.json", "r+") as f:
		data = json.load(f)
	file_lock.release()

	# Get a list of all user ids, if current user not found, create a new json object
	user_ids = []
	for items in data["users"]:
		user_ids.append(items["user_id"])

	# Index the user id list, find the current user for use in updating
	# If the id is not in the list, make a new json object with empty values, then return this instead
	if main_id not in user_ids:
		new_user = template
		write_json(new_user, "users.json", "users")
		user_ids.append(new_user["user_id"])
		user_id_index = user_ids.index(main_id)
		# Load the appended json, then find the user id with the index
		file_lock.acquire()
		with open("users.json") as f:
			data = json.load(f)
			user = data["users"][user_id_index]
		file_lock.release()
	else:
		user_id_index = user_ids.index(main_id)
		user = data["users"][user_id_index]

	user[key] += 1

	# Using the dump_file boolean argument, should the current file be overwritten after completion?
	# If not, return data, user; to continue operation
	if dump_file == True:
		file_lock.acquire()
		with open("users.json", "w") as f:
			json.dump(data, f, indent=2)
		file_lock.release()
	else:
		return data, user;

# Create new levels with "level, xp and role_id" as the objects in a levels.json file
# For use in knowing the current levels and where each user's level currently stands
# TODO: roleid should be changed to actual roleids in Discord (probably need new definition)
def new_levels(level_factor: int):
	global file_lock
	# Create new levels key and a level object template starting at 0 for all
	i = 0
	new_data = {"level": 0, "level_xp": 0, "total_xp": 0, "role_id": 0}
	level_factor = 20
	level_template = {"levels": []}

	# If the levels.json already exists, remove it to redo all calculations. Create new levels.json with level_template
	if os.path.exists("levels.json"):
		os.remove("levels.json")

	file_lock.acquire()
	with open ("levels.json", "w") as f:
		json.dump(level_template, f, indent=2)
	file_lock.release()

	# While i <= total_levels, create a new level object for each level 0 - i and calculate each variable as needed
	while i <= 301:
		# Create the variables
		p_level = new_data["level"]
		n_level = new_data["level"] + 1

		p_level_xp = new_data["level_xp"]
		level_xp = p_level_xp + (p_level * level_factor) + 100

		total_xp = new_data["total_xp"] + level_xp

		previous_roleid = new_data["role_id"]
		next_id = new_data["role_id"]

		# Create a new new_data object to then append and modify in the next loop
		new_data = {"level": n_level, "level_xp": level_xp, "total_xp": total_xp, "role_id": next_id}

		write_json(new_data, "levels.json", "levels")
		i += 1
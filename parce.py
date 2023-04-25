import os
import json

def get_file_links():
	link = 'stalcraft-database-main\global\items'
	folder_links = [folder.path for folder in os.scandir(link)]
	sub_folder_link = []
	for sub_folder in folder_links:
		for folder in os.scandir(sub_folder):
			if os.path.isfile(folder):
				sub_folder_link.append(folder.path)
	read_files(sub_folder_link)


def read_files(path):
	to_save =  {}
	with open('db.json', 'w', encoding='utf-8') as db:
		for file in path:
			with open(file, 'r', encoding='utf-8') as file:
				file = json.load(file)
				item_id = file.get('id')
				item_name = file['name']['lines'].get('en').lower()
				to_save[item_id] = item_name
		json.dump(to_save, db)
		db.close()




get_file_links()
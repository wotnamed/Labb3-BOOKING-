import json



# json.dumps(data) dump string not file
# youtube tutorial https://www.youtube.com/watch?v=-51jxlQaxyA
with open ("hotels_backup.json", "r") as file:
    data = json.load(file)

with open("hotels.json", "w") as foul:
    json.dump(data, foul, indent=4)

print(file)
print(data)
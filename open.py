import json

with open('Metro_json', 'r') as file:
    data = json.load(file)
print(data['RIOBA Напиток кокосовый, 1 л'])
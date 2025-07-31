import csv
import sys
import uuid

RESTAURANTS_CSV = '../data/restaurants.csv'

def add_restaurant(name, location):
    restaurant_id = str(uuid.uuid4())
    with open(RESTAURANTS_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([restaurant_id, name, location])
    print(f'Restaurant added: {name} (ID: {restaurant_id})')

def list_restaurants():
    with open(RESTAURANTS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            print(f'ID: {row[0]}, Name: {row[1]}, Location: {row[2]}')

def list_restaurants_by_chain():
    """Group restaurants by chain name and show all locations"""
    restaurants = {}
    with open(RESTAURANTS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name = row[1]
            if name not in restaurants:
                restaurants[name] = []
            restaurants[name].append({'id': row[0], 'location': row[2]})
    
    print("=== RESTAURANT CHAINS AND LOCATIONS ===")
    for chain_name, locations in restaurants.items():
        print(f"\n{chain_name}:")
        for location in locations:
            print(f"  - {location['location']} (ID: {location['id']})")

def list_restaurants_by_location():
    """Group restaurants by location"""
    locations = {}
    with open(RESTAURANTS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            location = row[2]
            if location not in locations:
                locations[location] = []
            locations[location].append({'id': row[0], 'name': row[1]})
    
    print("=== RESTAURANTS BY LOCATION ===")
    for location, restaurants in locations.items():
        print(f"\n{location}:")
        for restaurant in restaurants:
            print(f"  - {restaurant['name']} (ID: {restaurant['id']})")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python restaurant_management.py [add <name> <location> | list | chains | locations]')
    elif sys.argv[1] == 'add' and len(sys.argv) == 4:
        add_restaurant(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'list':
        list_restaurants()
    elif sys.argv[1] == 'chains':
        list_restaurants_by_chain()
    elif sys.argv[1] == 'locations':
        list_restaurants_by_location()
    else:
        print('Invalid command.') 
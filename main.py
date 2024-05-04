import os
from datetime import datetime
from json import dump
from os import getcwd, makedirs, path
from dotenv import load_dotenv

from modules.functions import (
    calculate_coordinates,
    calculate_length,
    generate_pattern,
    load_existing_data,
)

from modules.banners import (
    banner,
    finishing_application,
    pring_city_by_geo,
    print_combined_data,
    print_current_step,
    print_files_stored,
    print_geo_coordinater,
    print_len_steps,
    print_start_harvesting,
    print_successfully,
    print_telegram_initialization,
    print_update_html,
    print_update_local_json,
)

from telethon import TelegramClient
from telethon import functions, types
import asyncio

load_dotenv()

APP_NAME = os.getenv('APP_NAME')
API_ID = int(os.getenv('APP_ID'))
API_HASH = os.getenv('API_HASH')

async def harvest_locations(client, step_coordinates, users_data, avatar_directory, report_json_directory, filename, step):

    # Iterate over latitude and longitude pairs in step_coordinates
    for latitude, longitude in step_coordinates:
        result = await client(functions.contacts.GetLocatedRequest(
            geo_point=types.InputGeoPoint(
                lat=latitude,
                long=longitude,
                accuracy_radius=500
            )
        ))

        # Print the step and its coordinates
        print_start_harvesting()
        step += 1

        # Print current step with coordinates
        print_current_step(step, latitude, longitude)

        for update in result.updates:
            if isinstance(update, types.UpdatePeerLocated):
                for peer_located in update.peers:
                    if peer_located.distance == 500:
                        if isinstance(peer_located.peer, types.PeerUser):  # Check if the peer is a PeerUser
                            user_id = peer_located.peer.user_id
                            user_info = next((user for user in result.users if user.id == user_id), None)
                            if user_info:
                                # Get current timestamp
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                if user_id not in users_data:
                                    # If the user is not in the dictionary, add them with initial data
                                    username = user_info.username
                                    if user_info.photo:
                                        photo_id = user_info.photo.photo_id
                                    else:
                                        photo_id = None
                                    users_data[user_id] = {
                                        "first_name": user_info.first_name,
                                        "last_name": user_info.last_name,
                                        "username": user_info.username,
                                        "phone": user_info.phone,
                                        "photo_id": photo_id,
                                        "coordinates": [],
                                        "coordinates_average": {"latitude": 0, "longitude": 0, "timestamp": 0}
                                    }
                                    # Download avatar
                                    if username:
                                        avatar_filename = path.join(avatar_directory, f"{username}.jpg")
                                        if avatar_filename:
                                            if not path.exists(avatar_filename):
                                                try:
                                                    await client.download_profile_photo(username, file=avatar_directory + username, download_big=True)
                                                    print(f"Foto de perfil descargada exitosamente en {avatar_directory + username}")
                                                except Exception as e:
                                                    print(f"Error downloading profile photo for {username}: {e}")
                                    else:
                                        if photo_id:
                                            avatar_filename = path.join(avatar_directory, f"{photo_id}.jpg")
                                            if avatar_filename:
                                                if not path.exists(avatar_filename):
                                                    try:
                                                        await client.download_media(photo_id, f"{avatar_directory + str(photo_id)}.jpg")
                                                        print(f"Foto de perfil descargada exitosamente en {avatar_directory + str(photo_id)}")
                                                    except Exception as e:
                                                        print(f"Error downloading profile photo for {photo_id}: {e}")

                                # Append new coordinates
                                users_data[user_id]["coordinates"].append((latitude, longitude, timestamp))

                                # Calculate average coordinates
                                avg_latitude = sum(coord[0] for coord in users_data[user_id]["coordinates"]) / len(users_data[user_id]["coordinates"])
                                avg_longitude = sum(coord[1] for coord in users_data[user_id]["coordinates"]) / len(users_data[user_id]["coordinates"])

                                # Update the average coordinates
                                users_data[user_id]["coordinates_average"] = {"latitude": avg_latitude, "longitude": avg_longitude}


        # Write the updated data to the file
        print_update_local_json()
        with open(report_json_directory + filename + ".json", 'w') as file:
            dump(users_data, file, indent=4)
        print_successfully()


async def main():
    from modules.general_settings import latitude, longitude, meters

    pattern = generate_pattern((calculate_length(meters + 400) + 800) // 200)
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    step_coordinates = []

    step = 0
    users_data = {}
    filename = f'{latitude}-{longitude}-{current_datetime}'

    avatar_directory = "./avatars/"
    report_json_directory = "./reports-json/"

    if not path.exists(avatar_directory):
        makedirs(avatar_directory)
    if not path.exists(report_json_directory):
        makedirs(report_json_directory)

    print_geo_coordinater(latitude,longitude)

    pring_city_by_geo(latitude,longitude)

    # Perform steps according to the pattern
    for i, steps in enumerate(pattern):
        if i == 0:
            direction = 'starting'
        elif i % 4 == 1:
            direction = 'west'
        elif i % 4 == 2:
            direction = 'south'
        elif i % 4 == 3:
            direction = 'east'
        else:
            direction = 'north'
        for _ in range(steps):
            latitude, longitude = calculate_coordinates(latitude, longitude, direction, 0.6)  # 600 meters in kilometers
            step_coordinates.append((latitude, longitude))

    # Load existing data from file
    users_data = load_existing_data(report_json_directory + filename)

    ### Print number of steps
    print_len_steps(len(step_coordinates), meters)

    # Initialize the Telegram client
    print_telegram_initialization()

    # Inicializa el cliente de Telegram
    client = TelegramClient(APP_NAME, API_ID, API_HASH)
    await client.start()
    print_successfully()

    await harvest_locations(client, step_coordinates, users_data, avatar_directory, report_json_directory, filename, step)

    await client.disconnect()

# Ejecutar la función main en el loop de eventos
asyncio.run(main())
'''

Library for interacting with the PokeAPI.

https://pokeapi.co/

'''

import requests
import image_lib
import os


POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():

    #poke_info = get_pokemon_info("Rockruff")
    #get_pokemon_names()
    download_pokemon_artwork('123',r'c:\temp')
    return

def get_pokemon_info(pokemon_name):

    """Gets information about a specified Pokemon from the PokeAPI.
    Args:
        pokemon (str): Pokemon name (or Pokedex number)
    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.

    """

    # Clean the Pokemon name parameter by:
    # - Converting to a string object, 
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters

    pokemon_name = str(pokemon_name).strip().lower()
    url= POKE_API_URL + pokemon_name

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon_name}...', end='')
    resp_msg = requests.get(url)

    # Check if request was successful

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()

    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return

def get_pokemon_names(offset=0, limit=100000):

    query_params ={
        "limit" : limit,
        "offset" : offset
    }
    print(f'Getting list of Pokemon names...', end='')

    resp_msg = requests.get(POKE_API_URL, params=query_params)

    # Check if request was successful

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        resp_dict = resp_msg.json()
        pokemon_names = [p["name"] for p in resp_dict ['results'] ]
        return pokemon_names
        
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return

def download_pokemon_artwork(pokemon_name, folder_path):

    poke_info = get_pokemon_info(pokemon_name)

    if poke_info is None:
        return False
    
    poke_image_url = poke_info['sprites']['other']['official-artwork']['front_default']

    image_data = image_lib.download_image(poke_image_url)
    if image_data is None:
        return False
    

    image_ext = poke_image_url.split('.')[-1]
    file_name = f'{poke_info["name"]}.{image_ext}'
    file_path = os.path.join(folder_path,file_name)


    if image_lib.save_image_file(image_data, file_path):
        return file_path
    return False
        
if __name__ == '__main__':
    main()
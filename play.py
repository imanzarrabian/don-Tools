# -*- coding: utf-8 -*-
import requests
import sys


# REST functions
def get_histories():
    histories_url = "https://don-production.herokuapp.com/api/histories"
    r = requests.get(url = histories_url)
    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("GET /histories response not parsed")


def player_from_session(session, char_id):
    return [p for p in session["players"] if p["character"]["id"] == choosen_char_id][0]


def create_session(characterId, invited_email):
    params = {"characterId": int(characterId), "invite": str(invited_email)}
    session_url = "https://don-production.herokuapp.com/api/sessions"
    r = requests.post(url = session_url, json = params)
    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("POST /sessions response not parsed")

def execute_action(action_id, action_type, player_uuid):
    params = {"type": str(action_type), "id": int(action_id)}
    execute_url = "https://don-production.herokuapp.com/api/players/"+str(player_uuid)+"/execute"
    r = requests.post(url = execute_url, json = params)

    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("POST /sessions response not parsed")


# Game Engine
def display_state_and_actions(state):
    print """
        ------
    """
    print state["description"]
    print """
        ------
    """

    actions = state["actions"]
    available_actions = filter(lambda x: x["available"] == True, actions)
    disabled_actions = filter(lambda x: x["available"] == False, actions)

    for available_action in available_actions:
        print str(available_action["id"]) + " - " + available_action["title"]

    print """
        ------
    """

    action_choosen_id = int(raw_input("Votre choix : "))
    action_choosen_feedback = [x for x in available_actions if x["id"] == action_choosen_id][0]["feedback"]

    print action_choosen_feedback

    print """
        ------
    """
    return action_choosen_id, "action"


# Main story introduction
print """
    --------
    Le 11 février 2044. L'armistice de la 4ème guerre mondiale vient d'être signée.
    Les dirigeants des 6 pays de la H-belt ont finalement conclu un pacte avec le Japon et les Etats-Unis.
    Ce pacte est dorénavant inscrit dans les entrailles de Don qui veillera et sanctionnera toute violation.

    Don est une intelligence artificelle qui crée et dicte les lois.
    Les frontières se sont effacées et l'existence de pays n'est aujourd'hui que symbolique.
    Un seul gouvernement pour tous et ce n'est pas une démocratie.
    Elle est pensée par la machine et appliquée par les hommes.
    Don voit, écoute, décide des événements du monde des humains et de son expérience.
    La machine a le pouvoir de vie et de mort.

    Kate est institutrice dans une école historique de la ville.
    Marc est ancien militaire et travaille aujourd'hui comme agent de terrain de la H-belt.
    Kate et Marc sont mariés et vivent en banlieue de Lyon, capitale française depuis la 3ème bombe H.

    """

histories_data = get_histories()
available_chars = histories_data["characters"]

print "Quel joueur êtes vous ? "

for char in available_chars:
    print str(char["id"]) + " - " + str(char["name"])

choosen_char_id = int(raw_input("Numéro du joueur : "))

choosen_chars = [x for x in available_chars if x["id"] == choosen_char_id]
other_chars = [x for x in available_chars if x["id"] != choosen_char_id]

other_char_name = ""
if len(other_chars) > 0 and  len(choosen_chars) > 0:
    print "Vous êtes : " + str(choosen_chars[0]["name"])
    other_char_name = str(other_chars[0]["name"])
else:
    sys.exit("Bug in the matrix")

# Get the other user email
invited_email = raw_input("Qui sera votre " + other_char_name + "? (email):")

# Create a game session
session_data = create_session(choosen_char_id, invited_email)
player = player_from_session(session_data,choosen_char_id)
player_uuid = player["uuid"]

while 1:
    selected_action_id, selected_type = display_state_and_actions(player["state"])
    session_updated = execute_action(selected_action_id, selected_type, player_uuid)
    player = player_from_session(session_updated, choosen_char_id)
    display_state_and_actions(player["state"])
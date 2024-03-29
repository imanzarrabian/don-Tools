# -*- coding: utf-8 -*-
import requests
import sys
from threading import Thread

class style:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ITALIC = '\x1B[3m'
   END = '\033[0m'

base_url = "https://don-web-api-production.herokuapp.com"

# REST functions
def get_histories():
    histories_url = base_url + "/api/histories"
    r = requests.get(url = histories_url)
    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("GET /histories response not parsed")

def player_from_session_with_char_id(session, char_id):
    return [p for p in session["players"] if p["character"]["id"] == choosen_char_id][0]

def other_player_from_session_with_char_id(session, char_id):
    return [p for p in session["players"] if p["character"]["id"] != choosen_char_id][0]

def player_from_session_with_uuid(session, uuid):
    return [p for p in session["players"] if p["uuid"] == uuid][0]


def create_session(characterId, history_id):
    params = {"characterId": int(characterId), "historyId": int(history_id)}
    session_url = base_url + "/api/sessions"
    r = requests.post(url = session_url, json = params)
    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("POST /sessions response not parsed")

def join_session(uuid, session_id):
    params = {"uuid": str(uuid)}
    join_session_url = base_url + "/api/sessions/"+str(session_id)+"/join"

    r = requests.post(url = join_session_url, json = params)
    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("POST /sessions/uuid/join response not parsed")

def execute_action(action_id, action_type, player_id):
    #params = {"type": str(action_type), "id": int(action_id)}
    params = {"id": int(action_id)}
    execute_url = base_url + "/api/players/"+str(player_id)+"/execute"

    r = requests.post(url = execute_url, json = params)

    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("POST /sessions response not parsed")


def refresh_session(session_id):
    execute_url = base_url + "/api/sessions/"+str(session_id)
    r = requests.get(url = execute_url)

    if r.status_code == 200:
        return r.json()
    else:
        print r.text
        sys.exit("GET /sessions/:id response not parsed")



# Game Engine
def display_state_and_actions_and_messages(state, originId):

    if originId != state["id"]:
        print """
            ------
        """
        print style.BOLD + style.PURPLE + style.UNDERLINE + state["title"].encode('utf-8') + style.END
        print style.ITALIC + state["description"].encode('utf-8') + style.END
        print """
            ------
        """

    actions = state["actions"]

    #on indexe les actions possibles en local
    number_actions = len(actions)

    print style.BOLD + "0 - DEBUG - Refresh Session" + style.END

    i = 1
    for action in actions:
        notificationType = action.get("notificationType", "")
        title  = "SMS - " + action["title"] if notificationType == "sms" else action["title"]
        print style.BOLD + str(i) + " - " + title.encode('utf-8') + style.END #+ " - id : " + str(action["id"])
        i = i + 1
    print """
        ------
    """

    action_choosen_number = int(raw_input("Votre choix : "))
    #traitement des choix "action" et "message"
    if action_choosen_number == 0:
        return -1, "refresh"
    elif action_choosen_number < number_actions + 1 :
        notificationType = actions[action_choosen_number - 1].get("notificationType", "")

        action_choosen_feedback = actions[action_choosen_number - 1]["feedback"] if notificationType != "sms" else "Vous envoyez un message"
        action_choosen_id = actions[action_choosen_number - 1]["id"]
        if notificationType != "sms":
            print action_choosen_feedback.encode('utf-8')
        else:
            print action_choosen_feedback.encode('utf-8') + " : " + actions[action_choosen_number - 1]["notificationContent"].encode('utf-8')
        print """
            ------
        """
        return action_choosen_id, "action"

# Main story introduction
print style.ITALIC + """
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

    """ + style.END

if len(sys.argv) < 3: #first player
    #get histories
    #available chars and history_id
    histories_data = get_histories()
    available_chars = histories_data["characters"]
    history_id = histories_data["id"]

    #Input user char choice
    print style.DARKCYAN + "---- Quel joueur êtes vous ? " + style.END

    for char in available_chars:
        print str(char["id"]) + " - " + str(char["name"]).encode('utf-8')

    choosen_char_id = int(raw_input("---- Numéro du joueur selectionné : "))
    #choosen_char_id = 1

    choosen_chars = [x for x in available_chars if x["id"] == choosen_char_id]
    other_chars = [x for x in available_chars if x["id"] != choosen_char_id]

    other_char_name = ""
    if len(other_chars) > 0 and  len(choosen_chars) > 0:
        print style.DARKCYAN + "---- Vous êtes " + str(choosen_chars[0]["name"]).encode('utf-8') + style.END
        other_char_name = str(other_chars[0]["name"])
    else:
        sys.exit("Bug in the matrix")

    # Create a game session
    session_data = create_session(choosen_char_id, history_id)
    session_id = session_data["id"]

    #get both player
    player = player_from_session_with_char_id(session_data,choosen_char_id)
    other_player = other_player_from_session_with_char_id(session_data, choosen_char_id)

    player_uuid = player["uuid"]
    player_id = player["id"]
    other_player_uuid = other_player["uuid"]

    #prompt the command line for the other to play
    print style.DARKCYAN + "---- L'autre joueur joura " + str(other_char_name).encode('utf-8') + style.END
    print ""
    print style.BOLD + ">>>>>> Démarrez l'autre joueur avec python play.py " + str(other_player_uuid).encode('utf-8') + " " + str(session_id) + " <<<<<<" + style.END


elif len(sys.argv) == 3: #second player
    # Create a game session
    session_data = join_session(sys.argv[1], sys.argv[2]) #player UUID and session id
    session_id = session_data["id"]

    #get playing player
    player = player_from_session_with_uuid(session_data,sys.argv[1])
    player_uuid = player["uuid"]
    player_id = player["id"]
    print "---- Vous êtes " + str(player["character"]["name"]).encode('utf-8')


else:
    print "whaaaaaat?"


lastOriginId = 0

current_state = player["state"]

while 1:
    selected_action_id, selected_type = display_state_and_actions_and_messages(player["state"], lastOriginId)
    lastOriginId = player["state"]["id"]
    if selected_action_id != -1 and selected_type != "refresh":
        session_updated = execute_action(selected_action_id, selected_type, player_id)
    else:
        session_updated = refresh_session(session_id)

    player = player_from_session_with_uuid(session_updated, player_uuid)

    if (player["state"]["win"]):
        print player["state"]["description"].encode('utf-8')
        print style.BOLD + style.PURPLE + style.UNDERLINE + "YOU WIN !!" + style.END
        break
    if (player["state"]["loose"]):
        print player["state"]["description"].encode('utf-8')
        print style.BOLD + style.RED + style.UNDERLINE + "You LOSE !!" + style.END
        break

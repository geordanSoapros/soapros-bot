from flask import Flask, render_template, request, jsonify, json
import requests
import traceback
import aiml
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAB159kkGrUBAChAXTIRzCb9G2be4LM1A1e0PWiSwZByUqsRHjc2VyX0jzZBe9yGvmIzjG0KpufOQo8wV5QBVxcP8V0zxojtooHlWL81rM5pZBjZBKANZC8fRuyaz4e6uwxAISFRCFjZAUdHLMZAkymOFORk3Fg6WAeKsvkCw2fmwZDZD'

kernel = aiml.Kernel()


if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

@app.route('/webhook', methods=['GET'])
def handle_verification():
    print("Verificando token.")
    if request.args.get('hub.verify_token', '') == '24789098':
        print("Verificacion correcta.")
        return request.args.get('hub.challenge')
    else:
        print("Verificacion fallida")
    return 'Error, validacion de token'

@app.route('/webhook', methods=['POST'])
def handle_messages():
    print("Obteniendo Mensajes")
    payload = request.get_data()
    # print(payload)
    for sender, message in messaging_events(payload):
        print("Obteniendo de %s: %s" % (sender, message))
        send_message(PAGE_ACCESS_TOKEN, sender, message)
    return "ok"

def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "Solo puedo manejar texto por ahora"

def send_message(token, recipient, text):
    if text == 'Solo puedo manejar texto por ahora':
        print("Mensaje por defecto")
        bot_response = text
    else:
        req_name = requests.get("https://graph.facebook.com/v2.6/{0}?fields=first_name&access_token={1}".format(recipient,PAGE_ACCESS_TOKEN))
        name = json.loads(req_name.text)
    
        kernel.setPredicate("name", name["first_name"], recipient)
        print(kernel.getPredicate("name", recipient))
        
        bot_response = kernel.respond(text, recipient)
         
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
        "recipient": {"id": recipient}, "message": {"text": bot_response}}),
    headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)
        
def call_geolocalitation_api(postalcode):
    r = requests.get('http://api.geonames.org/postalCodeSearchJSON?postalcode={0}&maxRows=1&username=botlibre'.format(postalcode))
    json_data = json.loads(r.text)
    return json_data["postalCodes"][0]["adminName2"]

if __name__ == "__main__":
    app.run(debug=True)


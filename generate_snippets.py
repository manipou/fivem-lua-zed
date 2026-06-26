import json
import urllib.request

def to_pascal_case(name):
    if not name:
        return ""
    parts = name.split('_')
    pascal = "".join(part.capitalize() for part in parts if part)
    if name.startswith('_'):
        pascal = '_' + pascal
    return pascal

def main():
    print("Fetching natives.json from FiveM...")
    url = "https://runtime.fivem.net/doc/natives.json"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    snippets = {}
    
    # First, inject custom FiveM/FXManifest helper snippets
    custom_snippets = {
        "CreateThread": {
            "prefix": ["CreateThread", "createthread"],
            "body": [
                "CreateThread(function()",
                "\twhile true do",
                "\t\tWait(${1:0})",
                "\t\t$0",
                "\tend",
                "end)"
            ],
            "description": "Creates a new thread/coroutine that runs asynchronously. Use Wait() inside loops to prevent crashing the game."
        },
        "Citizen.CreateThread": {
            "prefix": ["Citizen.CreateThread", "citizen.createthread"],
            "body": [
                "Citizen.CreateThread(function()",
                "\twhile true do",
                "\t\tCitizen.Wait(${1:0})",
                "\t\t$0",
                "\tend",
                "end)"
            ],
            "description": "Legacy syntax to create a new thread/coroutine that runs asynchronously. Use Wait() or Citizen.Wait() inside loops to prevent crashing the game."
        },
        "Wait": {
            "prefix": ["Wait", "wait"],
            "body": [
                "Wait(${1:1000})"
            ],
            "description": "Suspends execution of the current thread for the specified number of milliseconds."
        },
        "Citizen.Wait": {
            "prefix": ["Citizen.Wait", "citizen.wait"],
            "body": [
                "Citizen.Wait(${1:1000})"
            ],
            "description": "Suspends execution of the current thread for the specified number of milliseconds."
        },
        "RegisterNetEvent": {
            "prefix": ["RegisterNetEvent", "registernetevent", "RegisterServerEvent"],
            "body": [
                "RegisterNetEvent('${1:eventName}', function(${2:args})",
                "\t$0",
                "end)"
            ],
            "description": "Registers an event as safe to be triggered from remote clients/servers. Shorthand for RegisterNetEvent + AddEventHandler in modern FiveM Lua."
        },
        "AddEventHandler": {
            "prefix": ["AddEventHandler", "addeventhandler"],
            "body": [
                "AddEventHandler('${1:eventName}', function(${2:args})",
                "\t$0",
                "end)"
            ],
            "description": "Adds an event handler for a local or registered network event."
        },
        "TriggerServerEvent": {
            "prefix": ["TriggerServerEvent", "triggerserverevent"],
            "body": [
                "TriggerServerEvent('${1:eventName}', ${2:args})"
            ],
            "description": "Triggers a server-side event from a client-side script."
        },
        "TriggerClientEvent": {
            "prefix": ["TriggerClientEvent", "triggerclientevent"],
            "body": [
                "TriggerClientEvent('${1:eventName}', ${2:targetPlayer}, ${3:args})"
            ],
            "description": "Triggers a client-side event on a specific player (or -1 for all players) from a server-side script."
        },
        "TriggerEvent": {
            "prefix": ["TriggerEvent", "triggerevent"],
            "body": [
                "TriggerEvent('${1:eventName}', ${2:args})"
            ],
            "description": "Triggers a local event in the same environment (client-side to client-side, or server-side to server-side)."
        },
        "RegisterNUICallback": {
            "prefix": ["RegisterNUICallback", "registernuicallback"],
            "body": [
                "RegisterNUICallback('${1:callbackName}', function(${2:data}, ${3:cb})",
                "\t$0",
                "\tcb('ok')",
                "end)"
            ],
            "description": "Registers a callback for a NUI (HTML/JS) message sent via fetch('https://' + GetParentResourceName() + '/callbackName')."
        },
        "SendNUIMessage": {
            "prefix": ["SendNUIMessage", "sendnuimessage"],
            "body": [
                "SendNUIMessage({",
                "\taction = '${1:actionName}',",
                "\t${2:data = data}",
                "})"
            ],
            "description": "Sends a message to the NUI (HTML/JS) side of the resource."
        },
        "SetTimeout": {
            "prefix": ["SetTimeout", "settimeout"],
            "body": [
                "SetTimeout(${1:1000}, function()",
                "\t$0",
                "end)"
            ],
            "description": "Executes a function asynchronously after the specified delay in milliseconds."
        },
        "fxmanifest": {
            "prefix": ["fxmanifest", "manifest"],
            "body": [
                "fx_version 'cerulean'",
                "game 'gta5'",
                "",
                "author '${1:AuthorName}'",
                "description '${2:Description}'",
                "version '${3:1.0.0}'",
                "",
                "client_scripts {",
                "\t'client/**/*.lua'",
                "}",
                "",
                "server_scripts {",
                "\t'server/**/*.lua'",
                "}"
            ],
            "description": "Create a standard fxmanifest.lua template."
        },
        "fxmanifest_fx_version": {
            "prefix": "fx_version",
            "body": "fx_version '${1:cerulean}'",
            "description": "Specifies the FXManifest version. Common versions include 'cerulean', 'bodacious', 'adamant'."
        },
        "fxmanifest_game": {
            "prefix": "game",
            "body": "game '${1:gta5}'",
            "description": "Specifies the target game for the resource ('gta5' or 'rdr3')."
        },
        "fxmanifest_client_scripts": {
            "prefix": "client_scripts",
            "body": [
                "client_scripts {",
                "\t'${1:client/**/*.lua}'",
                "}"
            ],
            "description": "Lists scripts to be loaded on the client side."
        },
        "fxmanifest_server_scripts": {
            "prefix": "server_scripts",
            "body": [
                "server_scripts {",
                "\t'${1:server/**/*.lua}'",
                "}"
            ],
            "description": "Lists scripts to be loaded on the server side."
        },
        "fxmanifest_shared_scripts": {
            "prefix": "shared_scripts",
            "body": [
                "shared_scripts {",
                "\t'${1:shared/**/*.lua}'",
                "}"
            ],
            "description": "Lists scripts to be loaded on both client and server sides."
        },
        "fxmanifest_ui_page": {
            "prefix": "ui_page",
            "body": "ui_page '${1:html/index.html}'",
            "description": "Specifies the UI page (HTML/NUI) for the resource."
        },
        "fxmanifest_files": {
            "prefix": "files",
            "body": [
                "files {",
                "\t'${1:html/**/*}'",
                "}"
            ],
            "description": "Lists files to be loaded into the game client (NUI files, assets, etc.)."
        }
    }
    
    snippets.update(custom_snippets)
    
    print("Processing natives from FiveM...")
    total_natives = 0
    for namespace, group in data.items():
        for _hash, native in group.items():
            raw_name = native.get("name")
            if not raw_name:
                continue # Skip unnamed natives as they can't be called directly
            
            pascal_name = to_pascal_case(raw_name)
            
            # Format parameters
            params = native.get("params", [])
            param_placeholders = []
            param_docs = []
            
            for idx, p in enumerate(params, 1):
                p_name = p.get("name", f"arg{idx}")
                p_type = p.get("type", "any")
                # Avoid reserved words / sanitize placeholder
                param_placeholders.append(f"${{{idx}:{p_name}}}")
                param_docs.append(f"{p_name}: {p_type}")
                
            # Create the snippet body
            params_str = ", ".join(param_placeholders)
            body_str = f"{pascal_name}({params_str})"
            
            # Create description
            results_type = native.get("results", "void")
            ns = native.get("ns", namespace)
            native_hash = native.get("hash", _hash)
            desc_text = native.get("description", "")
            
            doc_lines = [
                f"Namespace: {ns}",
                f"Hash: {native_hash}",
                f"Returns: {results_type}",
            ]
            if param_docs:
                doc_lines.append("Parameters:\n" + "\n".join(f"  - {doc}" for doc in param_docs))
            if desc_text:
                doc_lines.append("\n" + desc_text.strip())
                
            description = "\n".join(doc_lines)
            
            snippets[pascal_name] = {
                "prefix": [pascal_name, raw_name],
                "body": [body_str],
                "description": description
            }
            total_natives += 1
            
    print(f"Total processed natives: {total_natives}")
    
    output_path = "snippets/lua.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated snippets and wrote to {output_path}")

if __name__ == "__main__":
    main()

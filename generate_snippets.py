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

def map_type(t):
    if not t:
        return "any"
    t = t.lower().replace(" ", "").replace("*", "")
    if t in ["int", "player", "ped", "vehicle", "entity", "hash", "scrhandle", "object", "cam", "fireid", "pickup", "weapon"]:
        return "integer"
    if t in ["float"]:
        return "number"
    if t in ["bool", "boolean"]:
        return "boolean"
    if t in ["char", "char*", "string"]:
        return "string"
    if t in ["void"]:
        return "nil"
    return "any"

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
            "prefix": "CreateThread",
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
            "prefix": "Citizen.CreateThread",
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
            "prefix": "Wait",
            "body": [
                "Wait(${1:1000})"
            ],
            "description": "Suspends execution of the current thread for the specified number of milliseconds."
        },
        "Citizen.Wait": {
            "prefix": "Citizen.Wait",
            "body": [
                "Citizen.Wait(${1:1000})"
            ],
            "description": "Suspends execution of the current thread for the specified number of milliseconds."
        },
        "RegisterNetEvent": {
            "prefix": "RegisterNetEvent",
            "body": [
                "RegisterNetEvent('${1:eventName}', function(${2:args})",
                "\t$0",
                "end)"
            ],
            "description": "Registers an event as safe to be triggered from remote clients/servers. Shorthand for RegisterNetEvent + AddEventHandler in modern FiveM Lua."
        },
        "RegisterServerEvent": {
            "prefix": "RegisterServerEvent",
            "body": [
                "RegisterNetEvent('${1:eventName}', function(${2:args})",
                "\t$0",
                "end)"
            ],
            "description": "Legacy alias to RegisterNetEvent."
        },
        "AddEventHandler": {
            "prefix": "AddEventHandler",
            "body": [
                "AddEventHandler('${1:eventName}', function(${2:args})",
                "\t$0",
                "end)"
            ],
            "description": "Adds an event handler for a local or registered network event."
        },
        "TriggerServerEvent": {
            "prefix": "TriggerServerEvent",
            "body": [
                "TriggerServerEvent('${1:eventName}', ${2:args})"
            ],
            "description": "Triggers a server-side event from a client-side script."
        },
        "TriggerClientEvent": {
            "prefix": "TriggerClientEvent",
            "body": [
                "TriggerClientEvent('${1:eventName}', ${2:targetPlayer}, ${3:args})"
            ],
            "description": "Triggers a client-side event on a specific player (or -1 for all players) from a server-side script."
        },
        "TriggerEvent": {
            "prefix": "TriggerEvent",
            "body": [
                "TriggerEvent('${1:eventName}', ${2:args})"
            ],
            "description": "Triggers a local event in the same environment (client-side to client-side, or server-side to server-side)."
        },
        "RegisterNUICallback": {
            "prefix": "RegisterNUICallback",
            "body": [
                "RegisterNUICallback('${1:callbackName}', function(${2:data}, ${3:cb})",
                "\t$0",
                "\tcb('ok')",
                "end)"
            ],
            "description": "Registers a callback for a NUI (HTML/JS) message sent via fetch('https://' + GetParentResourceName() + '/callbackName')."
        },
        "SendNUIMessage": {
            "prefix": "SendNUIMessage",
            "body": [
                "SendNUIMessage({",
                "\taction = '${1:actionName}',",
                "\t${2:data = data}",
                "})"
            ],
            "description": "Sends a message to the NUI (HTML/JS) side of the resource."
        },
        "SetTimeout": {
            "prefix": "SetTimeout",
            "body": [
                "SetTimeout(${1:1000}, function()",
                "\t$0",
                "end)"
            ],
            "description": "Executes a function asynchronously after the specified delay in milliseconds."
        },
        "fxmanifest": {
            "prefix": "fxmanifest",
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
    
    # We will first group all raw natives by their PascalCase names
    natives_by_name = {}
    total_raw_natives = 0
    
    for namespace, group in data.items():
        for _hash, native in group.items():
            raw_name = native.get("name")
            if not raw_name:
                continue # Skip unnamed natives
            
            pascal_name = to_pascal_case(raw_name)
            total_raw_natives += 1
            
            # Attach registry keys
            native["ns"] = native.get("ns", namespace)
            native["hash"] = native.get("hash", _hash)
            
            if pascal_name not in natives_by_name:
                natives_by_name[pascal_name] = []
                
            # Filter out identical duplicate definitions (e.g., same params and results)
            is_identical = False
            for existing in natives_by_name[pascal_name]:
                if existing["params"] == native["params"] and existing["results"] == native["results"]:
                    is_identical = True
                    break
            
            if not is_identical:
                natives_by_name[pascal_name].append(native)
                
    # Now compile EmmyLua stubs file headers
    stubs_lines = [
        "---@meta",
        "-- =========================================================================",
        "--             FiveM Lua Natives Library Definitions (EmmyLua Stubs)",
        "-- =========================================================================",
        "-- This file contains static function stubs for all FiveM native functions.",
        "-- Do not run this file directly in-game. It is meant to be indexed by ",
        "-- language servers like `lua-language-server` to provide autocomplete, ",
        "-- parameter details, return types, and hovers.",
        "-- =========================================================================\n"
    ]
    
    print(f"Total processed raw natives: {total_raw_natives}")
    print(f"Total unique PascalCase native names: {len(natives_by_name)}")
    
    # Process each grouped native
    for pascal_name, defs in natives_by_name.items():
        # --- 1. SNIPPETS COMPILATION ---
        if len(defs) == 1:
            # Standard single definition snippet
            native = defs[0]
            params = native.get("params", [])
            param_placeholders = [f"${{{idx}:{p.get('name', f'arg{idx}')}}}" for idx, p in enumerate(params, 1)]
            param_docs = [f"{p.get('name', f'arg{idx}')}: {p.get('type', 'any')}" for idx, p in enumerate(params, 1)]
            
            body_str = f"{pascal_name}({', '.join(param_placeholders)})"
            desc_text = native.get("description", "")
            
            doc_lines = [
                f"Namespace: {native['ns']}",
                f"Hash: {native['hash']}",
                f"Returns: {native.get('results', 'void')}",
            ]
            if param_docs:
                doc_lines.append("Parameters:\n" + "\n".join(f"  - {doc}" for doc in param_docs))
            if desc_text:
                doc_lines.append("\n" + desc_text.strip())
                
            snippets[pascal_name] = {
                "prefix": pascal_name,
                "body": [body_str],
                "description": "\n".join(doc_lines)
            }
        else:
            # Overloaded definitions (e.g. client/server/shared differences)
            # Create distinct labeled snippets all sharing the same trigger prefix!
            for idx, native in enumerate(defs, 1):
                ns = native["ns"]
                snippet_key = f"{pascal_name} [{ns}]"
                # If there's duplicate definitions inside the same namespace, append index
                if snippet_key in snippets:
                    snippet_key = f"{pascal_name} [{ns} - {idx}]"
                
                params = native.get("params", [])
                param_placeholders = [f"${{{i}:{p.get('name', f'arg{i}')}}}" for i, p in enumerate(params, 1)]
                param_docs = [f"{p.get('name', f'arg{i}')}: {p.get('type', 'any')}" for i, p in enumerate(params, 1)]
                
                body_str = f"{pascal_name}({', '.join(param_placeholders)})"
                desc_text = native.get("description", "")
                
                doc_lines = [
                    f"Namespace: {ns} (Overloaded Version {idx})",
                    f"Hash: {native['hash']}",
                    f"Returns: {native.get('results', 'void')}",
                ]
                if param_docs:
                    doc_lines.append("Parameters:\n" + "\n".join(f"  - {doc}" for doc in param_docs))
                if desc_text:
                    doc_lines.append("\n" + desc_text.strip())
                    
                snippets[snippet_key] = {
                    "prefix": pascal_name,
                    "body": [body_str],
                    "description": "\n".join(doc_lines)
                }
                
        # --- 2. EMMYLUA STUBS COMPILATION ---
        if len(defs) == 1:
            # Standard single definition stub
            native = defs[0]
            params = native.get("params", [])
            results_type = native.get("results", "void")
            
            stub_comments = []
            desc_text = native.get("description", "")
            if desc_text:
                clean_desc = desc_text.strip().replace("\r", "")
                for line in clean_desc.split("\n"):
                    stub_comments.append(f"--- {line}")
            else:
                stub_comments.append(f"--- Namespace: {native['ns']} | Hash: {native['hash']}")
                
            stub_params = []
            for idx, p in enumerate(params, 1):
                p_name = p.get("name", f"arg{idx}")
                p_type = p.get("type", "any")
                
                lua_p_name = p_name
                if p_name in ["repeat", "end", "local", "function", "then", "else", "elseif", "until", "do", "while", "for", "in", "break", "return", "nil", "true", "false", "and", "or", "not"]:
                    lua_p_name = f"_{p_name}"
                
                stub_params.append(lua_p_name)
                stub_comments.append(f"---@param {lua_p_name} {map_type(p_type)}")
                
            mapped_ret = map_type(results_type)
            if mapped_ret != "nil":
                stub_comments.append(f"---@return {mapped_ret}")
                
            stubs_lines.extend(stub_comments)
            stubs_lines.append(f"function {pascal_name}({', '.join(stub_params)}) end\n")
        else:
            # Overloaded stub definition
            # We treat defs[0] as the primary signature, and others as ---@overload annotations
            primary = defs[0]
            overloads = defs[1:]
            
            # Write overload definitions first
            for ov in overloads:
                ov_params = []
                for idx, o_p in enumerate(ov.get("params", []), 1):
                    p_name = o_p.get("name", f"arg{idx}")
                    p_type = o_p.get("type", "any")
                    
                    if p_name in ["repeat", "end", "local", "function", "then", "else", "elseif", "until", "do", "while", "for", "in", "break", "return", "nil", "true", "false", "and", "or", "not"]:
                        p_name = f"_{p_name}"
                    ov_params.append(f"{p_name}: {map_type(p_type)}")
                    
                ov_ret = map_type(ov.get("results", "void"))
                stubs_lines.append(f"---@overload fun({', '.join(ov_params)}): {ov_ret}")
                
            # Write primary signature comments
            desc_text = primary.get("description", "")
            if desc_text:
                clean_desc = desc_text.strip().replace("\r", "")
                for line in clean_desc.split("\n"):
                    stubs_lines.append(f"--- {line}")
            else:
                stubs_lines.append(f"--- Namespace: {primary['ns']} (Overloaded primary signature) | Hash: {primary['hash']}")
                
            primary_params = []
            for idx, p in enumerate(primary.get("params", []), 1):
                p_name = p.get("name", f"arg{idx}")
                p_type = p.get("type", "any")
                
                lua_p_name = p_name
                if p_name in ["repeat", "end", "local", "function", "then", "else", "elseif", "until", "do", "while", "for", "in", "break", "return", "nil", "true", "false", "and", "or", "not"]:
                    lua_p_name = f"_{p_name}"
                
                primary_params.append(lua_p_name)
                stubs_lines.append(f"---@param {lua_p_name} {map_type(p_type)}")
                
            primary_ret = map_type(primary.get("results", "void"))
            if primary_ret != "nil":
                stubs_lines.append(f"---@return {primary_ret}")
                
            stubs_lines.extend([
                f"function {pascal_name}({', '.join(primary_params)}) end\n"
            ])
            
    # 1. Write the snippets
    snippets_path = "snippets/lua.json"
    with open(snippets_path, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated clean overloaded snippets and wrote to {snippets_path}")
    
    # 2. Write the EmmyLua stubs file
    stubs_path = "fivem_natives.lua"
    with open(stubs_path, "w", encoding="utf-8") as f:
        f.write("\n".join(stubs_lines))
    print(f"Successfully generated clean overloaded EmmyLua stubs file and wrote to {stubs_path}")

if __name__ == "__main__":
    main()

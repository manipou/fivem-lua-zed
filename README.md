# FiveM Lua Extension for Zed

A high-performance extension for **Zed** that provides complete auto-completion, rich snippets, and interactive documentation for **FiveM Lua natives** and general FiveM API functions.

## Features

- **5,300+ FiveM Natives:** Includes the entire native registry directly from the official FiveM documentation.
- **Dual-completion Support:** Triggers autocompletion using both the modern PascalCase convention (`GetPlayerPed`) and the original ALL_CAPS format (`GET_PLAYER_PED`).
- **Interactive Tab-Stops:** Auto-populates function parameters as tab-stops (e.g., `SetEntityCoords(${1:entity}, ${2:x}, ${3:y}, ${4:z}, ...)`), allowing you to write complex code instantly.
- **Rich Hover Documentation:** Displays detailed native info, including namespace, hash, return type, parameters, and official descriptions.
- **FiveM Utility Helpers:** Snippets for standard async loops, event registering, triggers, and NUI callbacks:
  - `CreateThread` & `Citizen.CreateThread` (pre-filled with game loop wait intervals)
  - `Wait` & `Citizen.Wait`
  - `RegisterNetEvent` (modern combined registration and event handler)
  - `AddEventHandler`
  - `TriggerServerEvent` / `TriggerClientEvent` / `TriggerEvent`
  - `RegisterNUICallback` & `SendNUIMessage`
  - `SetTimeout`
- **FXManifest Templates:** Instant snippets for creating `fxmanifest.lua` configurations with autocompletes for manifest fields (`fx_version`, `game`, `client_scripts`, `server_scripts`, `shared_scripts`, `ui_page`, `files`).

---

## Installing Locally (Dev Extension)

Since you are developing locally, you can install and test this extension directly in Zed as a **Dev Extension**:

1. In Zed, open the command palette (`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS).
2. Type `zed: install dev extension` and hit Enter.
3. Select this folder (`Zed_FiveM_Ext`) containing `extension.toml`.
4. The extension will install instantly and begin providing autocompletions for all `.lua` files in your workspace!

To check if it's active:
- Open any `.lua` file (such as a resource client script or an `fxmanifest.lua`).
- Start typing `GetPlayerPed` or `CreateThread` or `fxmanifest` to see the autocomplete overlay.

---

## 🚀 Pro-Tip: Professional-Grade LSP Autocomplete (Highly Recommended)

While snippets are incredibly convenient, they occasionally compete with local words in Zed's UI. For **flawless, native, lightning-fast autocompletions** with **full parameter types**, **hover annotations**, and **Go-To-Definition (Ctrl+Click)**, you can link the generated `fivem_natives.lua` stub library globally in Zed!

1. Open your global Zed settings (`Ctrl+,` or `Cmd+,`).
2. Add the path to `fivem_natives.lua` inside your `lsp.lua-language-server` workspace library configuration:
   ```json
   {
     "lsp": {
       "lua-language-server": {
         "settings": {
           "Lua": {
             "workspace": {
               "library": [
                 "C:/Projects/Zed_FiveM_Ext/fivem_natives.lua"
               ]
             }
           }
         }
       }
     }
   }
   ```
   *(Make sure to adjust the path above to match the exact location of your `fivem_natives.lua` file. Use forward slashes `/` even on Windows!)*
3. Save your settings.
4. **Result:** The Lua Language Server will instantly index all 5,300+ FiveM native functions. Every single native will now autocomplete flawlessly with full static typing, parameters, and instant hovers in *all* of your FiveM projects!

---

## Updating the Snippets

The extension includes an automated generator script that communicates directly with FiveM's runtime API to compile the latest natives registry. If FiveM releases new natives, you can easily update the extension's snippet catalog by running:

```bash
python generate_snippets.py
```

This will fetch the latest registry, build the entire definitions library, and update `snippets/lua.json` automatically!

---

## License

This extension is licensed under the [MIT License](LICENSE).

# HOTKEY MANAGER FOR NUKEX:

[YouTube](https://www.youtube.com/watch?v=ajO1VFTUTo0&t=2s)  
[Nukepedia](http://www.nukepedia.com/)

This app will help you to create hotkeys for nodes in NodeGraph

It has next advantages:
1. You do not need to write code - all with Qt;
2. You do not need to reboot Nuke to make hotkeys work;
3. You can use 'shift' in hotkeys - the system of creating nodes was
rewritten to make this functionality possible;
4. You can create any hotkeys bundles of nodes you want with any
knobs you want;
5. You can choose for which node to ShowPanel (or not show at all?);
6. You can modify any knobs inside nodes.

This system works in Nuke ToolSets engine - it means that every time
you will call hotkey it will create toolset. But for user experience it
will still look like just creating nodes

Hope you enjoy!

# FIRST INSTALL:
1) Move "HotkeyManager" folder to "/.nuke/HotkeyManager"
2) In the !start! of file "/.nuke/init.py" add next code:

> import nuke  
> nuke.addPluginPath("./HotkeyManager")

# HOW TO UPDATE:
1) Copy config files* from "/.nuke/HotkeyManager"
2) Move !new! "HotkeyManager" folder to "/.nuke/HotkeyManager"
3) Paste config files* to "/.nuke/HotkeyManager"

*"ToolSets", "hotkey_manager_config.json"

[alt text](http://www.nukepedia.com/images/users/NyanNyanGringo/github_logo.png)
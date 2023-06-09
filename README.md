# The Lord of The Nodes

[YouTube](https://www.youtube.com/watch?v=h2O-PNnSndI)  
[Nukepedia](http://www.nukepedia.com/python/nodegraph/hotkey-manager)

![alt text](http://www.nukepedia.com/images/users/NyanNyanGringo/lord_of_nodes/lord_of_nodes_logo.jpeg)

### <center>Nodes control never was so easy!</center>

## You have...
1. Set Knob Defaults in one click
2. Set Hotkeys in two clicks
3. Full presets control:
   - Showing Properties Panel
   - Using Context-Sensitive
   - Using Knob Defaults

System works in Nuke ToolSets engine - it means that every time you will call hotkey it will create toolset.
But for user experience it will still look like just creating nodes.
Create any Hotkeys bundles of nodes you want with any knobs you want!

*Why Foundry still haven't done something similar?*

## FIRST INSTALL:
1) Move "VP_Lord_of_Nodes" folder to "/.nuke/VP_Lord_of_Nodes"
2) In the !start! of file "/.nuke/init.py" add next code:

> import nuke  
> nuke.pluginAddPath("./VP_Lord_of_Nodes")

## HOW TO UPDATE (MANUALLY):
1) Delete folder "lord_of_nodes" ("/.nuke/VP_Lord_of_Nodes/lord_of_nodes")
2) Move !new! "lord_of_nodes" folder to "/.nuke/VP_Lord_of_Nodes/lord_of_nodes"

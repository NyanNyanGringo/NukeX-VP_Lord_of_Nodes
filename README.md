# LORD OF NODES FOR NUKEX:

[YouTube](https://www.youtube.com/watch?v=zZLdHVLjIM0)  
[Nukepedia](http://www.nukepedia.com/python/nodegraph/hotkey-manager)

This app will help you to create hotkeys for nodes in NodeGraph

It has next advantages:
1. You can create any hotkeys bundles of nodes you want with any knobs you want *
2. You can use 'shift' in hotkeys - the system of creating nodes was rewritten to make this functionality possible
3. You do not need to reboot Nuke to make hotkeys work
4. You can choose for which node to ShowPanel (or not show at all?)
5. You do not need to write code - all with Qt

*System works in Nuke ToolSets engine - it means that every time you will call hotkey it will create toolset. But for user experience it will still look like just creating nodes

Hope you enjoy!

# FIRST INSTALL:
1) Move "VP_Lord_of_Nodes" folder to "/.nuke/VP_Lord_of_Nodes"
2) In the !start! of file "/.nuke/init.py" add next code:

> import nuke  
> nuke.pluginAddPath("./VP_Lord_of_Nodes")

# HOW TO UPDATE:
1) Delete folder "lord_of_nodes" ("/.nuke/VP_Lord_of_Nodes/lord_of_nodes")
2) Move !new! "lord_of_nodes" folder to "/.nuke/VP_Lord_of_Nodes/lord_of_nodes"

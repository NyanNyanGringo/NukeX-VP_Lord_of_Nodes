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

<!-- START COPY FROM HERE -->


    <div style="display: flex; flex-direction: column; align-items: start;">

        <!-- YOUTUBE AND GITHUB LOGOS -->

        <div style="position: relative; align-self: center; display: flex; gap: 50px">
            <a
                href="https://www.youtube.com/watch?v=ajO1VFTUTo0&amp;t=2s"
                target="_blank"
                ><img
                style="
                    border-radius: 15px;
                    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
                    width: 274px;
                    height: auto;
                "
                src="http://www.nukepedia.com/images/users/NyanNyanGringo/youtube_logo.jpg"
                alt="youtube_logo"
                />
            </a>
            <a
                href="https://github.com/NyanNyanGringo/NukeX_HotkeyManager"
                target="_blank"
                ><img
                style="
                    border-radius: 15px;
                    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
                    width: 274px;
                    height: auto;
                "
                src="http://www.nukepedia.com/images/users/NyanNyanGringo/github_logo.png"
                alt="github_logo"
                />
            </a>
        </div>
        
        <!-- TEXT: INTRO -->
        
        <!-- <h3 style="align-self: center;">
            This app will help you to create hotkeys for nodes in NodeGraph!
        </h3> -->

        <!-- INSTRUCTIONS -->
        
        <h2 style="align-self: center;">CREATOR MENU</h2>
        
        <img
            style="border-radius: 10px; width: 600px; height: auto; align-self: center;"
            src="http://www.nukepedia.com/images/users/NyanNyanGringo/hotkey_creator_menu.png"
            alt="hotkey_creator_menu"
        />

        <h2 style="align-self: center;">EDIT MENU</h2>
        
        <img
            style="border-radius: 10px; width: 600px; height: auto; align-self: center;"
            src="http://www.nukepedia.com/images/users/NyanNyanGringo/hotkey_edit_menu.png"
            alt="hotkey_creator_menu"
        />

        <h2 style="align-self: center;">NODEGRAPH MENU</h2>
        
        <img
            style="border-radius: 10px; width: 600px; height: auto; align-self: center;"
            src="http://www.nukepedia.com/images/users/NyanNyanGringo/hotkey_nodegraph_menu.png"
            alt="hotkey_creator_menu"
        />

        <!-- HOTKEY ADVANTAGES -->

        <h2 style="align-self: center;">HOTKEY MANAGER ADVANTAGES</h2>
        <h3>
            <ol style="margin-left: 50px;">
                <li style="margin-top: 10px;">You can create any hotkeys bundles of nodes you want with any knobs you want
                    <span style="color:red;">*</span>
                </li>

                <li style="margin-top: 10px;">
                    You can use 'shift' in hotkeys - the system of creating nodes was rewritten to make this functionality possible
                </li>

                <li style="margin-top: 10px;">
                    You do not need to reboot Nuke to make hotkeys work
                </li>

                <li style="margin-top: 10px;">
                    You can choose for which node to ShowPanel (or not show at all?)
                </li>
                
                <li style="margin-top: 10px;">
                    You do not need to write code - all with Qt
                </li>
            </ol>
        </h3>
        
        <p style="margin-left: 75px;">
            <span style="color:red;">*</span>
            System works in Nuke ToolSets engine - it means that every time you will call hotkey it will create toolset. But for user experience it will still look like just creating nodes
        </p>
        

        <!-- FIRST INSTALL -->


        <h2 style="align-self: center;">FIRST INSTALL</h2>


        <h3>
            <ol style="margin-left: 50px;">
                <li style="margin-top: 10px;">
                    Move "HotkeyManager" folder to "/.nuke/HotkeyManager"
                </li>

                <li style="margin-top: 10px;">
                    In the !start! of file "/.nuke/init.py" add next code:
                </li>
            </ol>
        </h3>
        
        
        <h3>
            <ul style="list-style: none; background-color: #efefef; border-radius: 8px; max-width: fit-content; padding: 15px; margin-left: 75px;">
                <li style="color: grey">import nuke</li>
                <li style="color: grey">nuke.addPluginPath("./HotkeyManager")</li>
            </ul>
        </h3>


        <!-- HOW TO UPDATE -->


        <h2 style="align-self: center;">HOW TO UPDATE</h2>

        
        <h3>
            <ol style="margin-left: 50px;">
                <li style="margin-top: 10px;">
                    Copy config files<span style="color:red;">*</span> from "/.nuke/HotkeyManager"
                </li>

                <li style="margin-top: 10px;">
                    Move !new! "HotkeyManager" folder to "/.nuke/HotkeyManager"
                </li>

                <li style="margin-top: 10px;">
                    Paste config files* to "/.nuke/HotkeyManager"
                </li>
            </ol>
        </h3>


        <p style="margin-left: 75px;">
            <span style="color:red;">*</span> Folder "ToolSets" and file "hotkey_manager_config.json"
        </p>


        <!-- CHANGES -->


        <h2 style="align-self: center;">CHANGES</h2>

        <ul style="margin-left: 50px;">
            <ul style="margin-left: -50px; color: rgb(0, 200, 255)">
                v1.3:
            </ul>

            <li style="list-style: circle; margin-top: 10px;">
                Fixed function "set_mouse_tracking_in_nodegraph"
            </li>

            <li style="list-style: circle; margin-top: 10px;">
                Fixed Qt bug on MacOs when Create/Edit menus opens in new tabs
            </li>
        </ul>


        <!-- END COPY FROM HERE -->
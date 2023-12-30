"""
How to work with app_updater:
1. Change update_config.py values: github_username and github_repository
2. Add next code to your application builder:
    '''
    from app_updater import updateHelper
    action = updateHelper.add_update_action_to_menu(menu=???)  # to update by clicking action
    updateHelper.start_updating_application_when_initiazile(action)  # to ckeck update when initialize
    '''
3. Build app like in example:


How to build app to make app_updater work:
1. Structure of app should be like:
    + Plugin Path Folder (Folder that add through nuke.addPluginPath()):
        - menu.py
        - config
        + Application (that will be updated/replaced):
            - app_updater
            - Other Application Files
2. Inside Application should be version-file that called like: "v0.0.0"
3. When create GitHub application release - follow this:
    a. tag format: v0.0.0
    b. name format: RepositoryName_v0.0.0 (example: NukeX-VP_LittleHelpers_v0.0.0)
    c. comments: use # in every line
    d. set as a pre-release - do not use!

"""

# EDIT
github_username = "NyanNyanGringo"
github_repository = "NukeX-VP_Lord_of_Nodes"

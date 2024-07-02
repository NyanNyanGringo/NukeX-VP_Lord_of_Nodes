# TODO: add find preset for creator
# TODO: add create in nodegraph only one preset
# TODO: add Root for knobDefault support
# TODO: add Merge, Dissolve etc. support when many nodes selected
# TODO: DespillMadness don't work correct because of Presents incorrect knob values


import nuke


if nuke.NUKE_VERSION_MAJOR > 12:
	import lord_of_nodes.menu

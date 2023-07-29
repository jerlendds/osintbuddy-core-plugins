from osintbuddy.elements import CopyText
import osintbuddy as ob


class WhoisPlugin(ob.Plugin):
    label = "Whois"
    show_label = False
    color = "#F47C00"
    node = [
        CopyText(label="Raw Whois", icon="world"),
    ]

    author = 'the OSINTBuddy team'
    description = ''

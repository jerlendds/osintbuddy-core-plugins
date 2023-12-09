from osintbuddy.elements import CopyText
import osintbuddy as ob


class Whois(ob.Plugin):
    label = "Whois"
    show_label = False
    color = "#F47C00"
    node = [
        CopyText(label="Raw Whois", icon="world-search"),
    ]
    icon = "world-search"
    author = "the OSINTBuddy team"
    description = ""

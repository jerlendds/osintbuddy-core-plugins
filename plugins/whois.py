from osintbuddy import DiscoverableEntity
from osintbuddy.elements import CopyText, TextAreaInput, Empty


class Whois(DiscoverableEntity):
    label = "Whois"
    icon = "world-search"
    color = "#F5893A"
    show_label = False

    properties = [
        TextAreaInput(label="Whois Data"),
        [Empty(), Empty()],
    ]

    author = "Team@ICG"
    description = "Raw information from the public WHOIS database"

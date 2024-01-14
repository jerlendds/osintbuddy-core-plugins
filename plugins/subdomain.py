from osintbuddy.elements import TextInput
from osintbuddy import transform, DiscoverableEntity, EntityRegistry


class Subdomain(DiscoverableEntity):
    label = "Subdomain"
    icon = "submarine"
    color = "#FFCC33"
    show_label = False

    properties = [
        TextInput(label="Subdomain", icon="world"),
    ]

    author = "Team@ICG"
    description = "A domain that is part of a larger domain"
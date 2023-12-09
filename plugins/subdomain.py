from osintbuddy.elements import TextInput
import osintbuddy as ob


class Subdomain(ob.Plugin):
    label = "Subdomain"
    show_label = False
    color = "#FFCC33"
    node = [
        TextInput(label="Subdomain", icon="world"),
    ]
    icon = "submarine"
    author = 'the OSINTBuddy team'

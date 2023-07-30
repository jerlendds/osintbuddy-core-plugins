from osintbuddy.elements import TextInput
import osintbuddy as ob


class SubdomainPlugin(ob.Plugin):
    label = "Subdomain"
    show_label = False
    color = "#FFCC33"
    node = [
        TextInput(label="Subdomain", icon="world"),
    ]

    author = 'the OSINTBuddy team'

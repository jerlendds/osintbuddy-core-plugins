from osintbuddy.elements import TextInput
import osintbuddy as ob

class UsernameProfile(ob.Plugin):
    label = 'Username Profile'
    show_label = False
    color = '#D842A6'
    node = [
        TextInput(label='Category', icon='category'),
        TextInput(label='Site', icon='world'),
        TextInput(label='Link', icon='link'),
        TextInput(label='Username', icon='user'),
    ]

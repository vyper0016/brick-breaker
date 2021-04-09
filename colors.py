from json import load

with open('colours.json', 'r') as f:
    color_dict = load(f)


class Color:
    def __init__(self, name: str):
        try:
            color_dict[name]
        except KeyError:
            raise KeyError(f'color {name} not found')

        self.name = name
        self.red, self.green, self.blue = color_dict[name]['red'], color_dict[name]['green'], color_dict[name]['blue']
        self.hex = color_dict[name]['hex']
        self.rgb = (self.red, self.green, self.blue)


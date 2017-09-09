class ConfigData:

    def __init__(self, data):
        self.data = data

    def __str__(self):
        string = 'FILE_TYPES = {'
        space = '    '
        for language, extensions in self.data.items():
            string += f'\n{space}\'{language}\': (\n{space}{space}'

            for extension in extensions:
                string += f'\'{extension}\', '

            string += f'\n{space}),'

        string += '\n}'
        return string

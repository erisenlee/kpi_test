import configparser
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(BASE_DIR, 'config.ini')


class ReadConfig:
    def __init__(self, file_path=None):
        self.file_path = file_path if file_path else config_file
        
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file_path,encoding='utf-8')

    def get_section(self, section_name):
        if not self.parser.has_section(section_name.upper()):
            raise ValueError('section_name uncorrect')
        options = self.parser.items(section_name.upper())
        return {name:value for name,value in options}

    def get_option(self, section, option):
        if self.parser.has_option(section, option):
            return self.parser.get(section, option)
        else:
            return None

    

if __name__ == '__main__':
    c = ReadConfig()
    value=c.get_section('db')
    print(value)
        
        
    

        
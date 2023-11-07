from app import utils
from components.base_component import BaseComponent

pre_defined_sources = ('link', 'csv')


class DataPreprocessor(BaseComponent):
    def __init__(self, datasource):
        super().__init__('DataPreprocessor')
        self.sources = utils.read_yaml_file(datasource)
        self.csv_sources = self.sources.get('csv', [])
        self.html_sources = self.sources.get('link', [])

    def get_csv_sources(self):
        return self.csv_sources

    def get_html_sources(self):
        return self.html_sources

    def run(self, **kwargs):
        pass

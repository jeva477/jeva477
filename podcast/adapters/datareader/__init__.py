from podcast.domainmodel.model import Podcast, Author
from podcast.adapters.datareader.csvdatareader import CSVDataReader

class Repository:
    def __init__(self):
        csv_reader = CSVDataReader()
        csv_reader.readPodcasts()
        csv_reader.readEpisodes()
        self._all_podcasts = csv_reader.all_podcasts
        self._all_episodes = csv_reader.all_episodes

    @property
    def all_podcasts(self):
        return self._all_podcasts

    @property
    def all_episodes(self):
        return self._all_episodes


import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:

    all_podcasts = []
    all_episodes = []
    all_categories = set(())
    all_authors = set(())

    #reader for episodes
    """
         - id
         - podcast_id
         - title
         - audio
         - audio_length
         - description
         - pub_date

    """

    def readEpisodes(self):
        with open('podcast/adapters/data/episodes.csv') as csvfile:
            episode_list = csv.reader(csvfile)
            next(episode_list)
            for episodes in episode_list:
                ep_id = int(episodes[0])
                podcast_id = int(episodes[1])
                title = episodes[2]
                audio = episodes[3]
                audio_length = int(episodes[4])
                description = episodes[5]
                pub_date = episodes[6]

                ep_podcast = self.all_podcasts[podcast_id - 1]

                new_episode = Episode(ep_id, ep_podcast, title, audio, description, audio_length)

                ep_podcast.add_episode(new_episode) #adds episode to the podcast
                self.all_episodes.append(new_episode)

    #reader for podcasts
    """
        - id - 0
        - title - 1
        - image - 2
        - description - 3
        - language - 4
        - categories - 5
        - website - 6
        - author - 7
        - itunes_id - 8
    """

    def readPodcasts(self):
        with open(
                'podcast/adapters/data/podcasts.csv'
                , mode='r') as csvfile:
            podcasts_list = csv.reader(csvfile)
            next(podcasts_list)
            for podcasts in podcasts_list:
                pdc_id = podcasts[0]
                author_name = podcasts[7]
                if not isinstance(author_name, str) or not author_name.strip():
                    author_name = pdc_id
                try:
                    pdc_id = int(pdc_id)
                except:
                    pass
                author = Author(pdc_id, author_name)
                if author in self.all_authors:
                    break

                self.all_authors.add(author)
                title = podcasts[1]
                image = podcasts[2]
                description = podcasts[3]
                language = podcasts[4]
                categories = podcasts[5]
                website = podcasts[6]
                itunes_id = int(podcasts[8])

                currentPodcast = Podcast(pdc_id, author, title, image, description, website, itunes_id, language)

                cat_list = categories.split(' | ')
                #               makes the categories
                for i in range(len(cat_list)):
                    new_cat = Category(len(self.all_categories) + 1, cat_list[i])
                    self.all_categories.add(new_cat)
                    currentPodcast.add_category(new_cat)
                self.all_podcasts.append(currentPodcast)
                author.add_podcast(currentPodcast)


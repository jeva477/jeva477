"""Initialize Flask app."""
import random
from flask import Flask, render_template, url_for, request

from podcast.adapters.datareader import Repository

repository = Repository()

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    @app.route('/')
    def home():
        page = request.args.get('page', 1, type=int)
        # Use Jinja to customize a predefined html page rendering the layout for showing a single podcast.
        pd=[]

        podcast_list = repository.all_podcasts

        per_page = 20
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(podcast_list) + per_page - 1) // per_page

        items_on_page = podcast_list[start:end]

        return render_template('layout.html', podcasts=items_on_page, page=page, total_pages=total_pages)

    @app.route('/podcastDescription', methods=['GET'])
    def podcastDescription():
        q = request.args.getlist('id')
        print(q)
        id = int(q[0])
        page = int(q[1])

        #id = request.args.get('id', 1, type=int)
        #page = request.args.get('page', 1, type=int)
        podcast = repository.all_podcasts[int(id) - 1]

        per_page = 4
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(podcast.episodes) + per_page - 1) // per_page

        podcast_episodes = podcast.episodes[start:end]

        return render_template("podcastDescription.html", podcast=podcast, episodes=podcast_episodes,
                               page=page, total_pages=int(total_pages))


    @app.route('/catalogue')
    def catalogue():
        pod_list = []
        for i in range(3):
            pod_to_add = repository.all_podcasts[random.randint(0,len(repository.all_podcasts)-1)]
            while pod_to_add not in pod_list:
                pod_list.append(pod_to_add)
            else:
                pod_to_add = repository.all_podcasts[random.randint(0, len(repository.all_podcasts) - 1)]

        return render_template("catalogue.html", podcasts=pod_list)

    return app
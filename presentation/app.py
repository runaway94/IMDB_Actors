from flask import Flask, render_template, request

from IMDB_Actors.data.get_from_database import get_actor_for_table, get_single_actor

app = Flask(__name__)


@app.route('/')
def actors():  # put application's code here
    actors = get_actor_for_table();
    print(actors)
    return render_template('actors.html', actorTableEntrys=actors)

@app.route('/actor')
def actor():
    actor_id = request.args.get('id', default=1, type=str)
    actor = get_single_actor(actor_id)
    print(actor)
    return render_template('actor_detail.html', actor=actor)


if __name__ == '__main__':
    app.run()

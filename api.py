import flask
import bas.dao
import json

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def bas_query():
    gsin = flask.request.args.get('gsin', '')
    notices = bas.dao.search(gsin)
    return flask.Response(json.dumps(notices, indent=2), mimetype='application/json')

if __name__ == '__main__':
    app.run()

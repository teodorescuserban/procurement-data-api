import flask
import bas.dao
import json

app = flask.Flask(__name__)
app.debug = True

def split(value):
    if value:
        return [s.strip().upper() for s in value.split(',')]
    else:
        return ()

@app.route('/tender-notices.json')
def bas_query():
    gsins = split(flask.request.args.get('gsins', ''))
    delivery = split(flask.request.args.get('delivery', ''))
    opportunity = split(flask.request.args.get('opportunity', ''))
    notices = bas.dao.search(gsins=gsins, delivery=delivery, opportunity=opportunity)
    return flask.Response(json.dumps(notices, indent=2), mimetype='application/json')

if __name__ == '__main__':
    app.run()

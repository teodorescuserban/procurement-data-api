import flask
import bas.dao
import json
import csv
import io

app = flask.Flask(__name__)
app.debug = True

def split(value):
    if value:
        return [s.strip().upper() for s in value.split(',')]
    else:
        return ()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route('/tender-notices.<format>')
def bas_query(format):
    gsins = split(flask.request.args.get('gsins', ''))
    delivery = split(flask.request.args.get('delivery', ''))
    opportunity = split(flask.request.args.get('opportunity', ''))
    keywords = split(flask.request.args.get('keywords', ''))
    notices = bas.dao.search(gsins=gsins, delivery=delivery, opportunity=opportunity, keywords=keywords)
    if format == 'json':
        return flask.Response(json.dumps(notices, indent=2), mimetype='application/json')
    elif format == 'csv':
        return flask.Response(generate_csv(notices), mimetype='text/csv;charset=UTF-8')
    else:
        raise Exception("Unsupported format: " + format)

@app.route('/contracts.<format>')
def contracts(format):
    gsins = split(flask.request.args.get('gsins', ''))
    keywords = split(flask.request.args.get('keywords', ''))
    contracts = bas.dao.search_contracts(gsins=gsins, keywords=keywords)
    if format == 'json':
        return flask.Response(json.dumps(contracts, indent=2), mimetype='application/json')
    else:
        raise Exception("Unsupported format: " + format)

def generate_csv(notices):
    headers = [
        'tender',
        'title_en',
        'title_fr',
        'buyer_en',
        'buyer_fr',
        'gsins',
        'regions_delivery',
        'regions_opportunity',
        'url_en',
        'url_fr',
        'date_closing'
    ]
    def to_csv(row):
        with io.StringIO() as output:
            writer = csv.writer(output)
            writer.writerow(row)
            return output.getvalue()

    yield(to_csv(headers))
    for notice in notices:
        def fix(value):
            if isinstance(value, str):
                return value
            else:
                return ','.join(value)
        yield(to_csv([fix(notice[header]) for header in headers]))

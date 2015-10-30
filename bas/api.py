"""
Controllers for the BuyAndSell procurement-data API.

Using Flask 0.10

Started October 2015 by David Megginson
"""

import flask

from bas.dao import search_tenders, search_contracts
from bas.output import gen_json, gen_tenders_csv, gen_contracts_csv

# Set up the app object for export
app = flask.Flask(__name__)
app.debug = True


@app.after_request
def after_request(response):
    """Add a CORS header to all output."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/tenders.<format>')
@app.route('/tender-notices.<format>') # deprecated
def tenders(format):
    """Return a list of matching tenders."""
    gsins = _split_tokens(flask.request.args.get('gsins', ''))
    delivery = _split_tokens(flask.request.args.get('delivery', ''))
    opportunity = _split_tokens(flask.request.args.get('opportunity', ''))
    keywords = _split_tokens(flask.request.args.get('keywords', ''))
    tenders = search_tenders(gsins=gsins, delivery=delivery, opportunity=opportunity, keywords=keywords)
    if format == 'json':
        return flask.Response(gen_json(tenders), mimetype='application/json')
    elif format == 'csv':
        return flask.Response(gen_tenders_csv(tenders), mimetype='text/csv;charset=UTF-8')
    else:
        raise Exception("Unsupported format: " + format)


@app.route('/contracts.<format>')
def contracts(format):
    """Return a list of matching contracts."""
    lang = flask.request.args.get('lang', 'en')
    gsins = _split_tokens(flask.request.args.get('gsins', ''))
    keywords = _split_tokens(flask.request.args.get('keywords', ''))
    contracts = search_contracts(gsins=gsins, keywords=keywords)
    if format == 'json':
        return flask.Response(gen_json(contracts), mimetype='application/json')
    elif format == 'csv':
        return flask.Response(gen_contracts_csv(contracts), mimetype='text/csv;charset=UTF-8')
    elif format == 'html':
        return flask.render_template('contracts.html', contracts=contracts, lang=lang)
    else:
        raise Exception("Unsupported format: " + format)


def _split_tokens(value):
    """
    Split tokens, trimming whitespace and converting to upper case.
    @param value the comma-separated token-list to split.
    @return a sequence representing the individual tokens.
    """
    if value:
        return [s.strip().upper() for s in value.split(',')]
    else:
        return ()


# end

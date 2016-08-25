#!/usr/bin/env python3

from bottle import route, run, template, request

from rocket_state import machine_state


@route('/')
def test():
    state = machine_state()
    my_dict = dict((name, getattr(state, name)) for name in dir(state) if not name.startswith('_'))
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    </head>
    <body>
    <h1>Rocket R60V - Machine State</h1>
       <p>This website serves a tiny interface for your RocketR60V.</p>
    <table style="width:80%">
      <tr>
        <th>Setting</th><th>current state</th><th>new state</th>
      </tr>
    """

    for key in my_dict.keys():
            html += template('<tr><td>{0}</td><td>{{{{{0}}}}}</td><td contenteditable="true">{{{{{0}}}}}</td></tr>'.format(key), **my_dict)

    html += """
    </table>

    <button id="export-btn" class="btn btn-primary">Update State</button><p id="export"></p>

    </body>
    </html>
    """
    return html


run(host='localhost', port=65000, debug=True)

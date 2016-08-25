#!/usr/bin/env python3

from bottle import route, run


@route('/hello')
def hello():
    return "Hello World!"


@route('/test')
def test():
    html = '<input type="range" min="0" max="100">'
    return html

@route('/')
def test():
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
	<table style="width:100%">
	  <tr>
	    <th>Setting</th><th>current state</th><th>new state</th>
	  </tr>
	  <tr>
	    <td>Jill</td><td>Smith</td><td contenteditable="true">50</td>
	  </tr>
	  <tr>
	    <td>Eve</td><td>Jackson</td><td contenteditable="true">94</td>
	  </tr>
	  <tr>
	    <td>John</td><td>Doe</td><td contenteditable="true">80</td>
	  </tr>
	</table>

	<button id="export-btn" class="btn btn-primary">Update State</button><p id="export"></p>

	</body>
	</html>
	"""
    return html


run(host='localhost', port=65000, debug=True)

#!/usr/bin/env python3

import argparse
from bottle import route, run, request
import socket

from rocket_state import *
from RocketAPI import R60V

obj = R60V()


@route('/')
def web():
    #%#
    # state = obj.read()
    print('state = obj.read()')
    state = machine_state()
    html = gen_template(state)
    return html

@route('/', method='POST')
def do_web():
    state = machine_state()

    # coffeeCyclesSubtotal
    # coffeeCyclesTotal
    # pressureA
    state.pressureA = parse_profile('A')
    # pressureB
    state.pressureB = parse_profile('B')
    # pressureC
    state.pressureC = parse_profile('C')
    # activeProfile
    state.activeProfile = request.forms.get('activeProfile')
    # language
    state.language = request.forms.get('language')
    # isServiceBoilerOn
    # isMachineInStandby
    # waterSource
    state.waterSource = request.forms.get('waterSource')
    # temperatureUnit
    state.temperatureUnit = request.forms.get('temperatureUnit')
    # coffeeTemperature
    state.coffeeTemperature = int(request.forms.get('coffeeTemperature'))
    # steamTemperature
    state.steamTemperature = int(request.forms.get('steamTemperature'))
    # steamCleanTime
    # coffeePID
    # groupPID
    # mysteryPID
    # autoOnTime
    # autoStandbyTime
    # autoSkipDay

    #%#
    # obj.write(state)
    print('obj.write(state)')

    html = gen_template(state)
    return html

def gen_template(state):
    my_dict = dict((name, getattr(state, name)) for name in dir(state) if not name.startswith('_'))
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        vertical-align:middle;
    }
    tr td:nth-child(2), td:nth-child(3) {
       text-align: center;
    }
    </style>
    </head>
    <body>
    <h1>Rocket R60V - Machine State</h1>
       <p>This website serves a tiny interface for your RocketR60V. Press the button to update the machine:   <input value="Update!" type="submit"/></p>
    <form action="/" method="post">
    <table style="width:90%" align="center">
      <col style="width: 40%;">
      <col style="width: 30%;">
      <col style="width: 30%;">
      <tr>
        <th>Setting</th><th>current state</th><th>new state</th>
      </tr>
    """
    # coffeeCyclesSubtotal
    html += '<tr><td>coffeeCyclesSubtotal</td><td>{0}</td><td>{0}</td></tr>'.format(state.coffeeCyclesSubtotal)
    # coffeeCyclesTotal
    html += '<tr><td>coffeeCyclesTotal</td><td>{0}</td><td>{0}</td></tr>'.format(state.coffeeCyclesTotal)
    # pressureA
    html += gen_pressure_profile('A', state.pressureA)
    # pressureB
    html += gen_pressure_profile('B', state.pressureB)
    # pressureC
    html += gen_pressure_profile('C', state.pressureC)
    # activeProfile
    html += gen_selection('activeProfile', 'Activated Profile', state.activeProfile, ActiveProfile)
    # language
    html += gen_selection('language', 'Selected language', state.language, Language)
    # isServiceBoilerOn
    html += '<tr><td>Service Boiler status [On/Off]</td><td>{}</td><td>'.format(state.isServiceBoilerOn)
    if state.isServiceBoilerOn:
        html += '<input type="checkbox" name="isServiceBoilerOn" checked>'
    else:
        html += '<input type="checkbox" name="isServiceBoilerOn" unchecked>'
    html += '</td></tr>'
    # isMachineInStandby
    html += '<tr><td>Standby status of R60V [On/Off]</td><td>{}</td><td>'.format(state.isMachineInStandby)
    if state.isMachineInStandby:
        html += '<input type="checkbox" name="isMachineInStandby" checked>'
    else:
        html += '<input type="checkbox" name="isMachineInStandby" unchecked>'
    html += '</td></tr>'
    # waterSource
    html += gen_selection('waterSource', 'Water Connection', state.waterSource, WaterSource)
    # temperatureUnit
    html += gen_selection('temperatureUnit', 'Temperature Unit', state.temperatureUnit, TemperatureUnit)
    # coffeeTemperature
    html += '<tr><td>Coffee Boiler Temperature</td><td>{}</td><td>'.format(state.coffeeTemperature)
    if state.temperatureUnit == 'Celsius':
        html += '<input type="number" value="{}" min="{t[0]}" max="{t[1]}" step="1" name="coffeeTemperature"/></td></tr>'.format(state.coffeeTemperature, t=Coffee_temp_C)
    else:
        html += '<input type="number" value="{}" min="{t[0]}" max="{t[1]}" step="1" name="coffeeTemperature"/></td></tr>'.format(state.coffeeTemperature, t=Coffee_temp_F)
    # steamTemperature
    html += '<tr><td>Steam Boiler Temperature</td><td>{}</td><td>'.format(state.steamTemperature)
    if state.temperatureUnit == 'Celsius':
        html += '<input type="number" value="{0}" min="{t[0]}" max="{t[1]}" step="1" name="steamTemperature"/></td></tr>'.format(state.steamTemperature, t=Steam_temp_C)
    else:
        html += '<input type="number" value="{}" min="{t[0]}" max="{t[1]}" step="1" name="steamTemperature"/></td></tr>'.format(state.steamTemperature, t=Steam_temp_F)
    # steamCleanTime
    html += '<tr><td>steamCleanTime</td><td>{0}</td><td>{0}</td></tr>'.format(state.steamCleanTime)
    # coffeePID
    html += '<tr><td>coffeePID</td><td>{0}</td><td>{0}</td></tr>'.format(state.coffeePID)
    # groupPID
    html += '<tr><td>groupPID</td><td>{0}</td><td>{0}</td></tr>'.format(state.groupPID)
    # mysteryPID
    html += '<tr><td>mysteryPID</td><td>{0}</td><td>{0}</td></tr>'.format(state.mysteryPID)
    # autoOnTime
    html += '<tr><td>autoOnTime</td><td>{0}</td><td>{0}</td></tr>'.format(state.autoOnTime)
    # autoStandbyTime
    html += '<tr><td>autoStandbyTime</td><td>{0}</td><td>{0}</td></tr>'.format(state.autoStandbyTime)
    # autoSkipDay
    html += '<tr><td>autoSkipDay</td><td>{0}</td><td>{0}</td></tr>'.format(state.autoSkipDay)

    html += """
    </table>
    </form>

    </body>
    </html>
    """
    return html

def gen_pressure_profile(name, state):
    html_tmp = '<tr><td>Pressure Profile: {}</td>'.format(name)
    html_tmp += """<td><table align="center" valign="middle">
        <tr><th>s</th><th>bar</th></tr>
        <tr><td>{t[0][0]}</td><td>{t[0][1]}</td></tr>
        <tr><td>{t[1][0]}</td><td>{t[1][1]}</td></tr>
        <tr><td>{t[2][0]}</td><td>{t[2][1]}</td></tr>
        <tr><td>{t[3][0]}</td><td>{t[3][1]}</td></tr>
        <tr><td>{t[4][0]}</td><td>{t[4][1]}</td></tr>
        </table></td>
    """.format(t=state)
    html_tmp += '<td><table align="center">'
    html_tmp += '<tr><th>s</th><th>bar</th></tr>'
    for idx in [0, 1, 2, 3, 4]:
        html_tmp += '<tr>'
        html_tmp += '<td><input type="number" value="{t[0]}" min="{r[0]}" max="{r[1]}" step="1" name="pressure{n}_{i}0"/></td>'.format(n=name, t=state[idx], r=Time, i=idx)
        html_tmp += '<td><input type="number" value="{t[1]}" min="{r[0]}" max="{r[1]}" step="1" name="pressure{n}_{i}1"/></td>'.format(n=name, t=state[idx], r=Pressure, i=idx)
        html_tmp += '</tr>'
    html_tmp += '</table></td></tr>'
    return html_tmp

def gen_selection(property, name, cur_state, possible):
    html_tmp = '<tr><td>{n}</td><td>{c}</td><td><select name="{p}">'.format(n=name, c=cur_state, p=property)
    for sz in possible:
        if sz == cur_state:
            html_tmp += '<option selected>{}</option>'.format(sz)
        else:
            html_tmp += '<option>{}</option>'.format(sz)
    html_tmp += '</select></td></tr>'
    return html_tmp

def parse_profile(sz):
    profile = []
    for idx in [0, 1, 2, 3, 4]:
        time = int(request.forms.get('pressure{}_{}0'.format(sz, idx)))
        pressure = int(request.forms.get('pressure{}_{}1'.format(sz, idx)))
        profile.append([time, pressure])
    return profile



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Web interface for Rocket R60V.')
    parser.add_argument('-i', '--ip',
                        dest='ip',
                        action='store',
                        help='ip adress of machine')

    parser.add_argument('-p', '--port',
                        dest='port',
                        action='store',
                        help='port of machine')
    args = parser.parse_args()

    if args.ip:
        ip = args.ip
    else:
        ip = socket.gethostbyname(socket.gethostname())

    if args.port:
        port = int(args.port)
    else:
        port = 8080

    print('Starting webserver at: {}:{}'.format(ip, port))
    run(host=ip, port=port, debug=False)

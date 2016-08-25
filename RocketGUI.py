#!/usr/bin/env python3

from bottle import route, run, template, request

from rocket_state import machine_state
from rocket_state import Language
from rocket_state import DayOfWeek
from rocket_state import TemperatureUnit
from rocket_state import WaterSource
from rocket_state import ActiveProfile

from rocket_state import Time
from rocket_state import Pressure

from rocket_state import Coffee_temp_C
from rocket_state import Coffee_temp_F
from rocket_state import Steam_temp_C
from rocket_state import Steam_temp_F

state = machine_state()

@route('/')
def web():
    my_dict = dict((name, getattr(state, name)) for name in dir(state) if not name.startswith('_'))
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        text-align:center; 
        vertical-align:middle;
    }
    </style>
    </head>
    <body>
    <h1>Rocket R60V - Machine State</h1>
       <p>This website serves a tiny interface for your RocketR60V.</p>
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
    html += gen_selection('activeProfile', state.activeProfile, ActiveProfile)
    # language
    html += gen_selection('language', state.language, Language)
    # isServiceBoilerOn
    html += '<tr><td>isServiceBoilerOn</td><td>{}</td><td>'.format(state.isServiceBoilerOn)
    if state.isServiceBoilerOn:
        html += '<input type="checkbox" name="isServiceBoilerOn" checked>'
    else:
        html += '<input type="checkbox" name="isServiceBoilerOn" unchecked>'
    html += '</td></tr>'
    # isMachineInStandby
    html += '<tr><td>isMachineInStandby</td><td>{}</td><td>'.format(state.isMachineInStandby)
    if state.isMachineInStandby:
        html += '<input type="checkbox" name="isMachineInStandby" checked>'
    else:
        html += '<input type="checkbox" name="isMachineInStandby" unchecked>'
    html += '</td></tr>'
    # waterSource
    html += gen_selection('waterSource', state.waterSource, WaterSource)
    # temperatureUnit
    html += gen_selection('temperatureUnit', state.temperatureUnit, TemperatureUnit)
    # coffeeTemperature
    html += '<tr><td>coffeeTemperature</td><td>{}</td><td>'.format(state.coffeeTemperature)
    if state.temperatureUnit == 'Celsius':
        html += '<input type="number" value="{}" min="{t[0]}" max="{t[1]}" step="1" name="coffeeTemperature"/></td></tr>'.format(state.coffeeTemperature, t=Coffee_temp_C)
    else:
        html += '<input type="number" value="{}" min="{t[0]}" max="{t[1]}" step="1" name="coffeeTemperature"/></td></tr>'.format(state.coffeeTemperature, t=Coffee_temp_F)
    # steamTemperature
    html += '<tr><td>steamTemperature</td><td>{}</td><td>'.format(state.steamTemperature)
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
    <input value="Update State" type="submit" />
    </form>

    </body>
    </html>
    """
    return html

@route('/', method='POST')
def do_web():
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

def gen_pressure_profile(name, state):
    html_tmp = '<tr><td>pressure{}</td>'.format(name)
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

def gen_selection(property, cur_state, possible):
    html_tmp = '<tr><td>{p}</td><td>{c}</td><td><select name="{p}">'.format(c=cur_state, p=property)
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

run(host='localhost', port=65000, debug=False)

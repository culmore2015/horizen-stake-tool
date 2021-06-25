import platform
import re

import demjson as demjson
from flask import *
from urllib.parse import unquote
import subprocess
import requests
import json

app = Flask(__name__)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


app.after_request(after_request)


def is_windows():
    return platform.system() == 'Windows'


TOOL_PATH = "C:\\staketool\\" if is_windows() else '/staketool/'
CMD_WORK_PWD = "C:\\staketool\\" if is_windows() else '/staketool/'


def exec_cmd(cmd):
    result = ''
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=CMD_WORK_PWD)
        result_lines = process.stdout.readlines()
        for line in result_lines:
            result += line.decode()
        result = re.compile(r'\x1b[^m]*m').sub('', result.strip())
        print('=================================\n' + cmd + '\n' + result)
    except Exception as e:
        print(e)
    return result


@app.route('/stake/list', methods=['GET'])
def get_stake_list():
    api_url = 'https://supernodes1.na.zensystem.io/api/stake/list?key=' + request.args.get("apikey")
    items = requests.get(api_url, timeout=5).json()
    results = []
    for it in items:
        balance_api = 'https://explorer.horizen.global/insight-api-zen/addr/' + it['stkaddr'] + '/?noTxList=1'
        it['balance'] = requests.get(balance_api, timeout=5).json()['balance']
        results.append(it)

    response = make_response(jsonify(results))
    return response


@app.route('/stake/create', methods=['POST'])
def create_stake():
    # ./staketool createstakeverification --testnet --stake=zto4YEJgg4dvbkGebcDiY2E2EYrcB1Qj5ws --payaddress='[{"address":"ztWkahECUQDmrb3ZGEPsyEoiZFdys3KJ42t","pct":50},{"address":"zta42DzhNTsUQv1kVbFKYy5V82AQsZPXpAf","pct":50}]'
    stake = request.form.get("stkaddr")
    pay_address = unquote(request.form.get('payaddress')).replace('\"', '\\"')
    tool = 'staketool.exe' if (platform.system() == 'Windows') else './staketool'
    cmd = TOOL_PATH + tool + ' createstakeverification --stake=' + stake + ' --payaddress="' + pay_address + '"'
    result = exec_cmd(cmd)
    resp = {}
    try:
        resp['message'] = '验证金额：' + str(demjson.decode(result)['amount'])
    except Exception as e:
        print(e)
        resp['message'] = result
    response = make_response(jsonify(resp))
    return response


@app.route('/stake/verify', methods=['POST'])
def verify_stake():
    # ./staketool sendtxandstakeverification --apikey=xn353f81aca15784c0650a76e0084bb4a57ce9395f  --txid=6974cc998a2244a871a1603229d0f94a5f91c0b36ae13c3601dd74792f5929e5
    apikey = request.form.get("apikey")
    txid = request.form.get("txid")
    tool = 'staketool.exe' if (platform.system() == 'Windows') else './staketool'
    cmd = TOOL_PATH + tool + ' sendtxandstakeverification --apikey=' + apikey + ' --txid=' + txid
    result = exec_cmd(cmd)
    resp = {'message': result}
    response = make_response(jsonify(resp))
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

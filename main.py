import sys
import apachelogs
from flask import Flask
from flask import jsonify
from collections import Counter

logfile = sys.argv[1]
datadir = "/data/"
app = Flask(__name__)

# what log format are we expecting
parser = apachelogs.LogParser(apachelogs.COMBINED)

@app.route('/stats')
def make_stats():
    # instantiate lists
    all_ips = []
    status_codes = []
    referers_get = []

    # walk file and extract the data we need
    with open(datadir + logfile) as f:
        for line in f:
            entry = parser.parse(line)
            all_ips.append(entry.remote_host)
            status_codes.append(entry.final_status)
            if "GET" in entry.request_line:
                referers_get.append(entry.headers_in["Referer"])

    # calculate
    ips_uniq_count = len(set(all_ips))
    hits_per_ip = Counter(all_ips)
    response_codes = Counter(status_codes)
    top_referers_get = dict(Counter(referers_get).most_common(5))

    # let's do some outputs
    data = {}
    data['ips_uniq_cnt'] = ips_uniq_count
    data['hits_per_ip_cnt'] = hits_per_ip
    data['response_codes_cnt'] = response_codes
    data['top_referers_GET_cnt'] = top_referers_get

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

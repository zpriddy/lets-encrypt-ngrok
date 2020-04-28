"""  Copyright 2019 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from flask import Flask, request
import os
import json
import datetime

filename = "/webhook-logs/log.txt"  # file that webhook payloads will be written
logs_dir = "/webhook-logs/"

if os.path.exists(filename):
    append_write = "a"  # append if already exists
else:
    append_write = "w"  # make a new file if not

app = Flask(__name__)


@app.route("/<path:path>", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def index(path=None):
    if request.method == "GET":
        return "<h1>Hello from Webhook Listener!</h1>"
    if request.method == "POST":
        filename = (
            logs_dir
            + ((path + "-") if path else "")
            + str(datetime.datetime.now().isoformat())
            + ".json"
        )
        with open(filename, "w") as f:
            headers = {}
            for key in request.headers.keys():
                headers[key] = request.headers.get_all(key)

            log_data = {
                "headers": headers,
                "method": request.method,
                "path": request.path,
                "query_string": request.query_string.decode(),
                "args": request.args.to_dict(),
                "data": {
                    "json": request.json,
                    "form": request.form.to_dict(),
                    "text": request.data.decode(),
                }
            }
            f.write(json.dumps(log_data, indent=4, sort_keys=True))
        return '{"success":"true"}'


if __name__ == "__main__":
    context = (
        os.environ.get("CERT"),
        os.environ.get("KEY"),
    )  # certificate and key file. Cannot be self signed certs
    app.run(
        host="0.0.0.0", port=5000, ssl_context=context, threaded=True, debug=True
    )  # will listen on port 5000

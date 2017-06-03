from flask import Flask, request
import log
import auth
import schedules_repository
import os

app = Flask(__name__)

@app.route("/sync", methods = ['POST'])
def sync():
    schedule = request.json
    auth_response = auth.authenticate('root', 'root')
    schedules_repository.save(schedule)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
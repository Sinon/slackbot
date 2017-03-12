import os

from flask import Flask, request, jsonify, Response
import requests


app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


def slack_resp(text, response_type='in_channel'):
    return {'text': text, 'response_type': response_type}


@app.route('/parrot', methods=['POST'])
def inbound():
    print(request.form)
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    inbound_message = username + " in " + channel + " says: " + text
    return jsonify(slack_resp(inbound_message))


valid_build_job_name = ['api']


@app.route('/build', methods=['POST'])
def build():
    print(request.form)
    username = request.form.get('user_name')
    text = request.form.get('text')
    response_url = request.form['response_url']
    if text not in valid_build_job_name:
        text = ('Unknown job {} supplied. Valid options: {}'
                ).format(text, valid_build_job_name)
        response_type = 'ephemeral'
        return jsonify(slack_resp(text, response_type))
    text = 'Build {} has been started by {}'.format(text, username)
    requests.post(response_url, json=slack_resp(text))
    # TODO Simulate a long job with message when build has "finished"
    requests.post(response_url, json=slack_resp('Build has finished.'))
    return Response(), 200


@app.route('/deploy', methods=['POST'])
def deploy():
    print(request.form)
    text = request.form['text']
    text_tokenised = text.split(' ')
    response_url = request.form['response_url']
    if len(text_tokenised) != 2:
        text = ('Incorrect number of parameters supplied ({}).'
                ' /deploy [branch] [environment]'.format(len(text_tokenised)))
        response_type = 'ephemeral'
        return jsonify(slack_resp(text, response_type))

    git_b, environment = text.split(' ')
    requests.post(response_url, json={"response_type": "in_channel"})
    text = 'Deploying branch {} to {}'.format(git_b, environment)
    requests.post(response_url, json=slack_resp(text))
    # TODO Simulate a long job with message when deploy has "finished"
    requests.post(response_url, json=slack_resp('Deploy has finished!'))
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)


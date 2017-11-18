import hashlib
import hmac
import click
import configparser
import sys
import json
import os

def set_config():
    if "LABELORD_CONFIG" in os.environ:
        return os.environ['LABELORD_CONFIG']
    else:
        return 'config.cfg'

#retur the list of target repos from config file set to 1/yes/on
def get_config_repos(config):
    repos = []
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(config)

    if (parser.has_section('repos')):
        for (each_repo, each_flag) in parser.items('repos'):
            if(parser.getboolean('repos', each_repo)):
                repos.append(each_repo)
        return repos
    else:
        click.echo('No repositories specification has been found', err=True)
        sys.exit(7)


def get_tkn(config):
    parser = None
    parser = configparser.ConfigParser()
    parser.read(config)
    config = set_config()

    if(parser.has_option('github','token')):
        return parser['github']['token']
    else:
        click.echo('No GitHub token has been provided', err=True)
        sys.exit(3)

#return secret from the config file
def get_secret(config):
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(config)
    if (parser.has_section('github') and parser.has_option('github','webhook_secret')):
        return parser['github']['webhook_secret']
    else:
        click.echo('No webhook secret has been provided', err=True)
        sys.exit(8)


#create label in other repos
def create_label(name, color, repos, session, origin):
    for repo in repos:
        if(repo != origin):
            data = {"name": name, "color": color}
            json_data = json.dumps(data)
            r = session.post("https://api.github.com/repos/"+repo+"/labels", json_data)
    return "200"

#edit label in other repos
def edit_label(old_name, new_name, new_color, repos, session, origin):
    for repo in repos:
        if(repo != origin):
            data = {"name": new_name, "color": new_color}
            json_data = json.dumps(data)
            if(old_name == None):
                r = session.patch("https://api.github.com/repos/" + repo + "/labels/" + new_name,json_data)
            else:
                r = session.patch("https://api.github.com/repos/" + repo + "/labels/" + old_name, json_data)
    return "200"

#delete label in other repos
def delete_label(name,repos, session, origin):
    for repo in repos:
        if(repo != origin):
            r = session.delete("https://api.github.com/repos/"+repo+"/labels/" + name)
    return "200"

#return True if the computed and received signatures are the same
def check_signature(secret, request):
    sig = 'sha1=' + hmac.new(secret.encode('utf-8'), request.data, hashlib.sha1).hexdigest()
    #compare computed and received signature
    if sig == get_signature(request):
        return True
    else:
        return False

#return x-github-signaure from request
def get_signature(request):
    if('X-Hub-Signature' in request.headers):
        return request.headers['X-Hub-Signature']
    else:
        return ""

def get_old_name(request):
    if('name' in request.json['changes']):
        return request.json['changes']['name']['from']

def get_old_color(request):
    if('color' in request.json['changes']):
        return request.json['changes']['color']['from']

#return action used for the label from request
def get_action(request):
    return request.json['action']

#return label name from request
def get_lname(request):
    return request.json['label']['name']

#return label color from request
def get_lcolor(request):
    return request.json['label']['color']

def get_repo_name(request):
    return request.json['repository']['full_name']

#return Github event from request
def get_event(request):
    return request.headers['X-Github-Event']




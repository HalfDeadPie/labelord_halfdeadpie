# This is skeleton for labelord module
# MI-PYT, task 1 (requests+click)
# File: labelord.py
import hashlib
import hmac

import click
import flask
import requests
import configparser
import sys
import json
import os
from flask import request


class Label:
    def __init__(self, name, color):
        self.n = name
        self.c = color
        
class Error:
    def __init__(self, operation, repo, label, message):
        self.o = operation
        self.r = repo
        self.l = label
        self.m = message

def eprint(err):
    click.echo("GitHub: ERROR {}" .format(err), err=True)

#TOKEN SETTING
def get_token(token,config):
    if(token != None):
        return token
    else:
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read(config)
        if(parser.has_section('github')):
            return parser['github']['token']
        else:
            return None
        
#TOKEN CHECK        
def check_token(token):
    if(token == None):
        click.echo('No GitHub token has been provided', err=True)
        sys.exit(3)
        
#AUTHORIZATION
def authorization(ctx,token):
    session = ctx.obj['session']
    session.headers = {'User-Agent': 'Python'}
    def token_auth(req):
        req.headers['Authorization'] = 'token ' + token
        return req
    session.auth = token_auth
    return ctx.obj['session']

#UPDATED REPOS COUNTING
def add_updated(ctx, repo):
        updated = ctx.obj['updated']
        if(updated.count(repo) == 0):
            updated.append(repo)

#ERROR COUNTER
def add_error(ctx, operation, repo, label, message):
        errors = ctx.obj['errors']
        err = Error(operation, repo, label, message)
        errors.append(err)       

#GET ERROR MESSAGE FROM JSON
def get_message(r):
    text = r.json()['message']
    message= str(r.status_code) + " - " + text
    return message

#LABEL COMPARE
def cmp_labels(a,b):
    if(a.n== b.n and a.c == b.c):
        return True
    else:
        return False

def is_named(template, label):
    for temp in template:
        if(temp.n == label.n):
            return True
    return False

def same_lower_name(a, b):
    if(a.n.lower() == b.n.lower() ):
        return True
    else:
        return False
    
def is_included(template, label):
    for temp in template:
        if(cmp_labels(temp,label)):
            return True
        elif(temp.n == label.n):
            temp.c = label.c
    return False

def is_named_diff(template, label):
    for temp in template:
        if(different_case(temp, label)):
            return True
    return False

def different_case(a,b):
    if(a.n != b.n and a.n.lower() == b.n.lower()):
        return True
    else:
        return False

#ACTUALIZE                
def actualize(ctx, repo, template, verbose, dry_run, quiet, replace):
        session = ctx.obj['session']        
        last = 0
        page = 1
        target_labels = []
        message = ""
        while True:  
        #REQUEST
            r = session.get('https://api.github.com/repos/' +repo+ '/labels?per_page=100&page=' + str(page) )
            #1. all possible labels received
            if(len(template) == 0):
                add_updated(ctx, repo)
            if(r.status_code == 200):
                for i in r.json():
                    color = i['color']
                    name = i['name']
                    lb = Label(name, color)
                    target_labels.append(lb)
            elif(r.status_code == 404):
                message = "[LBL][ERR] " + repo + "; " + get_message(r)
                if(quiet==False and verbose):
                    click.echo('{}' .format(message))
                add_error(ctx, "LBL", repo, None, get_message(r))
                return
            else:
                message = "[LBL][ERR] " + repo + "; " + get_message(r)
                add_error(ctx, "LBL", repo, None, get_message(r))
            if( page == 1 ):
                if(not r.links):
                    break;
                last = get_last_page(r)
            elif( page == last):
                break;
            page += 1

        for template_label in template:
            #PATCH
            if ( (not is_included(target_labels, template_label) and is_named(target_labels, template_label)) or
                 is_named_diff(target_labels,template_label)):
                #label found
                data = {"name": template_label.n, "color": template_label.c}
                json_data = json.dumps(data)                    
                if(dry_run == False):
                    p = session.patch("https://api.github.com/repos/"+repo+"/labels/"+template_label.n.lower(), json_data)
                message = '[UPD]'
                if(dry_run):
                    message += '[DRY] '
                    add_updated(ctx, repo)
                else:
                    if(p.status_code == 200):
                        message += '[SUC] '
                        add_updated(ctx, repo)
                    else:
                        message += '[ERR] '
                        add_error(ctx, "UPD", repo, template_label, get_message(p))
                message += repo +'; '+ template_label.n +'; '+ template_label.c
                if(dry_run == False and p.status_code != 200):
                        message += '; '+ get_message(p)
                    #final message
                if(verbose and message!="" and not quiet):
                    click.echo('{}' .format(message))
                                    

            #POST
            elif(not is_named(target_labels, template_label)):
                data = {"name": template_label.n, "color": template_label.c}
                json_data = json.dumps(data)

                message = '[ADD]'
                if(dry_run == False):
                    p = session.post("https://api.github.com/repos/"+repo+"/labels", json_data)
                if(dry_run):
                    message += '[DRY] '
                    add_updated(ctx, repo)
                else:
                    if(p.status_code == 201):
                        message += '[SUC] '
                        add_updated(ctx, repo)
                    else:
                        message += '[ERR] '
                        add_error(ctx, "ADD", repo, template_label, get_message(p))
                message += repo +'; '+ template_label.n +'; '+ template_label.c
                if(dry_run == False and p.status_code != 201):
                    message += '; '+ get_message(p)

                #final message
                if(verbose and message!="" and not quiet):
                    click.echo('{}' .format(message))

    
        if(replace):
            for target in target_labels:
                if(not is_included(template, target)):
                    if(dry_run == False):
                        r = session.delete("https://api.github.com/repos/" +repo+ "/labels/"+ target.n)
                    message = '[DEL]'
                    if(dry_run):
                        message += '[DRY] '
                        add_updated(ctx, repo)
                    else:
                        if(r.status_code == 204):
                            message += '[SUC] '
                            add_updated(ctx, repo)
                        else:
                            message += '[ERR] '
                            add_error(ctx, "[DEL]", repo, target, get_message(r))
                    message += repo +'; '+ target.n +'; '+ target.c
                    if(dry_run == False and r.status_code != 204):
                        message += '; '+ get_message(r)   
                    if(verbose and message!="" and not quiet):
                        click.echo('{}' .format(message))

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('labelord, version 0.1')
    ctx.exit()

@click.group('labelord')
@click.option('--config', '-c', default='config.cfg',
              help='Path of the auth config file.')
@click.option('--token', '-t', envvar='GITHUB_TOKEN.',
              help='GitHub API token.')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show the version and exit.')
@click.pass_context
def cli(ctx, token, config):    
    session = ctx.obj.get('session', requests.Session())
    ctx.obj['session'] = session
    ctx.obj['config'] = config
    ctx.obj['token'] = token

def get_last_page(response):
    result = response.links['last']['url']
    final = result.split("&page=")
    result = int(final[1])
    return result

@cli.command()
@click.pass_context
def list_repos(ctx):
    """Listing accessible repositories."""
    config = ctx.obj['config']
    realtoken = ctx.obj['token']
    if(realtoken == None):
        realtoken = get_token(ctx.obj['token'],config)
    check_token(realtoken)
    session = authorization(ctx,realtoken)


    #REQUEST
    session = ctx.obj['session']
    page = 1
    last = 0
    while True:
        r = session.get('https://api.github.com/user/repos?per_page=100&page='+str(page) )
        #1. data received
        if(r.status_code == 200):
            for i in r.json():
                owner = i['owner']['login']
                repo = i['name']
                click.echo('{}/{}' .format(owner,repo))
        #2. data not received - bad code
        elif(r.status_code == 404):
            eprint(get_message(r))
            sys.exit(5)       
        elif(r.status_code == 401):
            eprint(get_message(r))
            sys.exit(4)
        else:
            sys.exit(10)
        if( page == 1 ):
            if(not r.links):
                break;
            last = get_last_page(r)
        elif( page == last):
            break;
        page += 1

@cli.command()
@click.pass_context
@click.argument('repository')
def list_labels(ctx, repository):
    """Listing labels of desired repository."""
    session = ctx.obj['session']
    last = 0
    page = 1

    config = ctx.obj['config']
    realtoken = ctx.obj['token']
    if(realtoken == None):
        realtoken = get_token(ctx.obj['token'],config)
    check_token(realtoken)
    session = authorization(ctx,realtoken)

    while True:  
    #REQUEST
        r = session.get('https://api.github.com/repos/' +repository+ '/labels?per_page=100&page=' + str(page) )
        #1. all possible labels received
        if(r.status_code == 200):
            for i in r.json():
                color = i['color']
                name = i['name']
                click.echo('#{} {}' .format(color,name))
        #2. data not received - bad code
        elif(r.status_code == 401):
            eprint(get_message(r))
            sys.exit(4)            
        elif(r.status_code == 404):
            eprint(get_message(r))
            sys.exit(5)
        else:
            sys.exit(10)

        if( page == 1 ):
            if(not r.links):
                break;
            last = get_last_page(r)
        elif( page == last):
            break;
        page += 1

@cli.command()
@click.pass_context
@click.argument('mode', type=click.Choice(['update', 'replace']))
@click.option('--template-repo', '-r', default=None,
            help='The name of the template repo for labels.')
@click.option('--verbose','-v', is_flag=True)
@click.option('--dry-run','-d', is_flag=True)
@click.option('--quiet','-q', is_flag=True)
@click.option('--all-repos', '-a', is_flag=True)
def run(ctx,mode, template_repo, verbose, dry_run, quiet, all_repos):
    """Run labels processing."""
    config = ctx.obj['config']
    real_template_repo = None
    session = ctx.obj['session']
    config = ctx.obj['config']
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(config)
    template = []
    targets = []
    message = ""
    updated = []
    errors = []
    ctx.obj['updated'] = updated
    ctx.obj['errors'] = errors

    realtoken = ctx.obj['token']
    if(realtoken == None):
        realtoken = get_token(ctx.obj['token'],config)
    check_token(realtoken)
    session = authorization(ctx,realtoken)
    

    #repo from the command line
    if(template_repo != None):
        real_template_repo = template_repo
    #repo from the config file
    elif(parser.has_section('others') and parser.has_option('others','template-repo')):
        real_template_repo = parser['others']['template-repo']     

    #template repo from the config file
    last = 0
    page = 1

    if(real_template_repo != None):
        while True:
            r = session.get('https://api.github.com/repos/' + str(real_template_repo) + "/labels?per_page=100&page=" + str(page))    
            if(r.status_code == 200):
                for i in r.json():
                    color = i['color']
                    name = i['name']
                    lb = Label(name,color)
                    template.append(lb)
            elif(r.status_code == 401):
                if(quiet == False):
                    click.echo(get_message(r), err=True)
                sys.exit(4)                
            else:
                message = "[LBL][ERR] " + real_template_repo + "; " + get_message(r)
                add_error(ctx, "LBL", real_template_repo, None, get_message(r))
                
            if( page == 1 ):
                if(not r.links):
                    break;
                last = get_last_page(r)
            elif( page == last):
                break;
            page += 1

    #labels from config file
    else:
        if(parser.has_section('labels')):
            for (each_key, each_val) in parser.items('labels'):
                lb = Label(each_key, each_val)
                template.append(lb)
        else:
                #if(quiet == False):
            click.echo("No labels specification has been found", err=True)
            sys.exit(6)

    if(message != "" and verbose and quiet == False):
        click.echo("{}" .format(message))

    last = 0
    page = 1


    if(all_repos):
        while True:
            r = session.get('https://api.github.com/user/repos?per_page=100&page=' + str(page))
            #1. data received
            if(r.status_code == 200):
                for i in r.json():
                    owner = i['owner']['login']
                    name = i['name']
                    repo = owner +"/"+ name
                    targets.append(repo)
            #2. data not received - bad code
            elif(r.status_code == 401):
                if(quiet == False):
                     click.echo(get_message(r), err=True)
                sys.exit(4)
            else:
                sys.exit(10)

            if( page == 1 ):
                if(not r.links):
                    break;
                last = get_last_page(r)
            elif( page == last):
                break;
            page += 1

    
    else:
        if(parser.has_section('repos')):
            for (each_repo, each_flag) in parser.items('repos'):
                if(parser.getboolean('repos',each_repo)):
                        targets.append(each_repo)
        else:
            click.echo("No repositories specification has been found", err=True)
            sys.exit(7)
                

    
    #Target repos in targets    
    for repo in targets:
        if( mode == "replace" ):
                actualize(ctx, repo, template, verbose, dry_run, quiet, True)
        else:
                actualize(ctx, repo, template, verbose, dry_run, quiet, False)

    #Printing        
    if( (verbose and quiet) or (verbose==False and quiet==False) ):
        if(len(errors) > 0):
            for error in errors:
                errmsg = error.o +"; "+ error.r + "; "
                if(error.l != None):
                    errorlabel = error.l
                    errmsg += errorlabel.n + "; " +errorlabel.c + "; "
                errmsg += error.m
                click.echo('ERROR: {}' .format(errmsg), err=True)
            click.echo('SUMMARY: {} error(s) in total, please check log above' .format(len(errors)), err=True)
            sys.exit(10)
        else:
            click.echo('SUMMARY: {} repo(s) updated successfully' .format(len(updated)))
            sys.exit(0)
            
    #print verbose summary        
    if(verbose or dry_run):
        if(len(errors) > 0):
            click.echo("[SUMMARY] {} error(s) in total, please check log above" .format(len(errors)))
            sys.exit(10)
        else:
            click.echo('[SUMMARY] {} repo(s) updated successfully' .format(len(updated)))
            sys.exit(0)

    if(len(errors) > 0 and quiet==False):
        click.echo("[SUMMARY] {} error(s) in total, please check log above" .format(len(errors)))
        sys.exit(10)

    if(len(errors) > 0):
        sys.exit(10)

#####################################################################
# STARING NEW FLASK SKELETON (Task 2 - flask)
#check the config
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


class LabelordWeb(flask.Flask):
    my_session = None
    my_repos = []
    my_token = None
    my_config = None
    my_secret = None
    last_label = ""
    last_action = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can do something here, but you don't have to...
        # Adding more args before *args is also possible
        # You need to pass import_name to super as first arg or
        # via keyword (e.g. import_name=__name__)
        # Be careful not to override something Flask-specific
        # @see http://flask.pocoo.org/docs/0.12/api/
        # @see https://github.com/pallets/flask
        import_name=__name__
        self.my_config = set_config()
        config = self.my_config
        self.my_repos = get_config_repos(config)
        self.my_token = get_tkn(config)
        self.my_secret = get_secret(config)

    def inject_session(self, session):
        # TODO: inject session for communication with GitHub
        # The tests will call this method to pass the testing session.
        # Always use session from this call (it will be called before
        # any HTTP request). If this method is not called, create new
        # session.
        self.my_session = session

    def reload_config(self):
        # TODO: check envvar LABELORD_CONFIG and reload the config
        # Because there are problems with reimporting the app with
        # different configuration, this method will be called in
        # order to reload configuration file. Check if everything
        # is correctly set-up
        self.my_config = set_config()
        config = self.my_config
        self.my_repos = get_config_repos(config)
        self.my_token = get_tkn(config)
        self.my_secret = get_secret(config)

# TODO: instantiate LabelordWeb app
# Be careful with configs, this is module-wide variable,
# you want to be able to run CLI app as it was in task 1.
#app = flask.Flask(__name__)
app = LabelordWeb(__name__)
# TODO: implement web app
# hint: you can use flask.current_app (inside app context)
@app.route('/', methods=['GET', 'POST'])
def index():
    set_config()
    cfg = app.my_config
    repos = []
    repos = get_config_repos(cfg)
    r = request.method

    #GET METHOD
    if r == "GET":
        return get_info(repos)

    #POST METHOD
    elif r == "POST":
        if check_signature(get_secret(cfg), request):
            if get_event(request) == "ping":
                return "ok"
            elif get_event(request) == "label":
                app.my_session.headers = {'User-Agent': 'Python'}
                def token_auth(req):
                    req.headers['Authorization'] = 'token ' + app.my_token
                    return req
                app.my_session.auth = token_auth
                session = app.my_session

                repo = get_repo_name(request)
                if(repo in repos):
                    action = get_action(request)
                    name = get_lname(request)
                    color = get_lcolor(request)

                    if(name != app.last_label or action != app.last_action):
                        app.last_label = name
                        app.last_action = action
                        # CREATED
                        if (action == 'created'):
                            return create_label(name, color, repos, session, repo)
                        # EDITED
                        if (action == 'edited'):
                            old_name = get_old_name(request)
                            return edit_label(old_name, name, color, repos, session, repo)
                        # DELETED
                        if (action == 'deleted'):
                            return delete_label(name, repos, session, repo)
                    else:
                        return "OK"
                else:
                    code = 400
                    msg = 'BAD REQUEST'
                    return msg, code
        else:
            code = 401
            msg = 'UNAUTHORIZED'
            return msg, code

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

#Return info about application for GET method
def get_info(repos):
    info = "labelord application is master-to-master application for label replication using webhook for GitHub<br>"
    for i in repos:
        info += i +' '+ repo_link(i) + '<br>'
    return info



#return link to github and connected repo
@app.template_filter()
def repo_link(repo):
    return "https://github.com/" + repo



@cli.command()
@click.pass_context
@click.option('--host', '-h', default="127.0.0.1")
@click.option('--port', '-p', default=5000)
@click.option('--debug', '-d', is_flag=True)
def run_server(ctx, host, port, debug):
    # TODO: implement the command for starting web app (use app.run)
    # Don't forget to app the session from context to app
    app.my_config = ctx.obj['config']
    app.my_session = ctx.obj['session']
    app.run(host,port,debug)
# ENDING  NEW FLASK SKELETON
#####################################################################

if __name__ == '__main__':
    cli(obj={})

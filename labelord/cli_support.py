import click
import configparser
import sys
import json

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
        #problem
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
    click.echo('labelord, version 0.3')
    ctx.exit()

def get_last_page(response):
    result = response.links['last']['url']
    final = result.split("&page=")
    result = int(final[1])
    return result
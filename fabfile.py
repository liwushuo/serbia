# -*- encoding: utf-8 -*-

from fabric.api import task, run, local, prefix, hide, show, abort, with_settings
from fabric.state import env
from fabric.contrib.files import exists
from fapistrano import deploy
from fapistrano.utils import register_env, register_role, green_alert


env.project_name = 'serbia'
env.app_name = 'serbia'
env.repo = 'git@github.com:insysu/serbia.git'
env.user = 'deploy'
env.use_ssh_config = True
env.keep_releases = 5
env.branch = 'master'
env.env_role_configs = {
    'gfwsh': {
        'app': {
            'hosts': ['gfw-app01']
        }
    },
    'gfwsh_beta': {
        'app': {
            'hosts': ['gfw-app01'],
            'project_name': 'serbia-beta'
        }
    },
    'lws': {
        'app': {
            'hosts': ['app-app01']
        }
    }
}


@task
@register_env('gfwsh')
def gfwsh():
    env.env='gfwsh'
    pass


@task
@register_env('gfwsh_beta')
def gfwsh_beta():
    # env.env='gfwsh'
    pass


@task
@register_env('lws')
def lws():
    pass


@task
@register_role('app')
def app():
    pass


@deploy.first_setup_repo
def deploy_first_setup_repo():
    run('source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %(project_name)s' % env)
    _setup_repo()


@deploy.setup_repo
def deploy_setup_repo():
    _setup_repo()


def _setup_repo():
    run('git clone git@github.com:insysu/serbia-settings.git')
    if env.env=='gfwsh_beta':
        env.env = 'gfwsh'
    run('cp serbia-settings/%(env)s/*.py %(app_name)s/settings/' % env)
    run('rm -rf serbia-settings')
    with prefix(env.activate):
        run('pip install -q -r requirements.txt || pip install -r requirements.txt')
        run('FLASK_ENV=prod python manage.py db upgrade')

    green_alert('Building frontend assets')
    with show('output'):
        run('cd serbia/frontend && fis release -mopDd ../')

@task
def restart_beat():
    run('supervisorctl restart %(project_name)s-beat' % env)


@task
def runserver(port=5000):
    local('find . -name "*.pyc" -exec rm -rf {} \;', capture=False)
    local("python manage.py runserver --host 0.0.0.0 -p %s" % port, capture=False)


@task
def build_static():
    local('cd serbia/frontend && fis release -Lcmpwd ../')

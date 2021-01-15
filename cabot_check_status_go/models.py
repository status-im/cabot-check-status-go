import socket
import subprocess
from os import path
from os import environ as env
from django.db import models

from cabot.cabotapp.models import StatusCheck, StatusCheckResult

RAW_DATA_TEMPLATE = '''
Command:
{}
Return Code:
{}
Stdout:
{}
Stderr:
{}
'''

class StatusGoException(Exception):
    def __init__(self, message, raw_data):
        self.message = message
        self.raw_data = raw_data

class StatusGoStatusCheck(StatusCheck):
    check_name = 'status-go'
    edit_url_name = 'update-status-go-check'
    duplicate_url_name = 'duplicate-status-go-check'
    icon_class = 'glyphicon-random'

    # First value is the flag used with node-canary
    NODE_TYPES = (
        ('mailserver', 'history'),
        ('staticnode', 'relay'),
    )

    node_type = models.CharField(
        max_length=10,
        choices=NODE_TYPES,
        default='mailserver',
        help_text='Node type.'
    )
    enode = models.TextField(
        help_text='Enode address.'
    )

    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            rval = self._check()
        except StatusGoException as e:
            result.raw_data = e.raw_data
            result.error = u'Error occurred: {}'.format(e.message)
            result.succeeded = False
        except Exception as e:
            result.error = u'Error occurred: {}'.format(e)
            result.succeeded = False
        else:
            result.raw_data = rval
            result.succeeded = True

        return result

    def _check(self):
        log_level = env.get('STATUS_GO_CANARY_LOG_LEVEL', 'WARN')
        canary_path = env.get('STATUS_GO_CANARY_PATH')
        if canary_path is None:
            raise Exception('STATUS_GO_CANARY_PATH env variable not found!')

        if not path.exists(canary_path):
            raise Exception('No such file: {}'.format(canary_path))

        command = [
            canary_path,
            '-{}={}'.format(self.node_type, self.enode),
            '-home-dir=/tmp/cabot_check_status_go_{}'.format(self.name),
            '-timeout={}'.format(self.timeout-1),
            '-log={}'.format(log_level),
            '-log-without-color',
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        process.wait()
        return_code = process.poll()

        rval = RAW_DATA_TEMPLATE.format(
            ' \\\n  '.join(command), return_code, stdout, stderr
        )

        if return_code != 0:
            raise StatusGoException('Failed: {}'.format(stderr), rval)

        return rval

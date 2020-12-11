import socket
import subprocess
from os import environ as env
from django.db import models

from cabot.cabotapp.models import StatusCheck, StatusCheckResult


class StatusGoStatusCheck(StatusCheck):
    check_name = 'status-go'
    edit_url_name = 'update-status-go-check'
    duplicate_url_name = 'duplicate-status-go-check'
    icon_class = 'glyphicon-random'

    hostname = models.TextField(help_text='Node hostname.')
    enode = models.TextField(help_text='Enode address.')

    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            self._check()
        except Exception as e:
            result.error = u'Error occurred: %s' % (e.message,)
            result.succeeded = False
        else:
            result.succeeded = True

        return result

    def _check(self):
        canary_path = env.get('STATUS_GO_CANARY_PATH')
        if canary_path is None:
            raise Exception('STATUS_GO_CANARY_PATH env variable not found!')

        process = subprocess.Popen([
                canary_path,
                '-mailserver={}'.format(self.enode),
                '-home-dir=/tmp/cabot_check_status_go_{}'.format(self.hostname),
                '-log=WARN',
                '-log-without-color',
            ],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        process.wait()
        return_code = process.poll()

        if return_code != 0:
            raise Exception('Failed: {}'.format(stdout))


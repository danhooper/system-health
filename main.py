import datetime
from email.mime.text import MIMEText
import smtplib
import psutil


class Process(object):
    def __init__(self, name):
        self.name = name
        self.num_procs = 0
        self.output =''

    def update_process(self, proc):
        self.num_procs += 1
        self.output +=  'Process: %s\nCPU: %s\nMem: %s\n' % (
            self.name, proc.get_cpu_percent(),
            proc.get_memory_percent())

    def get_output(self):
        if self.output:
            return self.output
        else:
            return 'Process: %s is not running' % self.name


class ProcessInfo(object):
    def __init__(self, process_monitor_list):
        self.process_monitor_list = process_monitor_list

    def get_message_text(self):
        print('Getting ProcessInfo text')
        for proc_mon in self.process_monitor_list:
            for proc in psutil.process_iter():
                if proc.name == proc_mon.name:
                    proc_mon.update_process(proc)
        return '\n'.join([p.get_output() for p in self.process_monitor_list])


def main():
    process_info = ProcessInfo([Process('mythbackend'),
                                Process('mythfrontend.real'),
                                Process('apache2')])
    email_msg = MIMEText(process_info.get_message_text())
    email_msg['Subject'] = 'System Health %s' % str(datetime.datetime.now())
    email_msg['To'] = 'dan.c.hooper@gmail.com'
    email_str = email_msg.as_string()
    smtp_server = smtplib.SMTP('127.0.0.1')
    smtp_server.sendmail('dan.c.hooper@gmail.com', ['dan.c.hooper@gmail.com'],
                     email_str)


if __name__ == '__main__':
    main()

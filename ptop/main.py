import threading
import logging
import requests
import argparse
import sys
import string
import random
import os
import platform

from ptop import __version__, _log_file
from ptop.statistics import Statistics
from ptop.interfaces import PtopGUI
from ptop.constants import SUPPORTED_THEMES
from huepy import *

from ptop.plugins.dask_sensor import DaskSensor

# Backwards compatibility for string input operation
try:
    input = raw_input
except NameError:
    pass

logger = logging.getLogger('ptop.main')


def _update():
    '''
        Try to update ptop at application start after asking the user
    '''
    try:
        CURRENT_VERSION = str(__version__)
        os_name = "{0} {1}".format(platform.system(),
                                   platform.release()
                                   )
        resp = requests.get("https://ptop-telemetry.darxtrix.in", params={'os_name': os_name, 'version': __version__}, timeout=1)
        NEW_VERSION = str(resp.text)
        if NEW_VERSION != CURRENT_VERSION and resp.status_code == 200:
            sys.stdout.write(blue("A new version is available, would you like to update (Y/N) ? "))
            sys.stdout.flush()
            user_consent = input()
            if user_consent.lower() == 'y':
                logger.info("main.py :: Updating ptop to version {0}".format(NEW_VERSION))
                # run update instructions
                update_success_status = 0
                source_folder = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                sys.stdout.write(green("\nCreating a temporary directory /tmp/{0} ...\n".format(source_folder)))
                sys.stdout.flush()
                update_success_status |= os.system('mkdir /tmp/{0}'.format(source_folder))
                sys.stdout.flush()
                update_success_status |= os.system('git clone https://github.com/darxtrix/ptop.git /tmp/{0}'.format(source_folder))
                sys.stdout.write(green("\nInstalling ptop ...\n"))
                sys.stdout.flush()
                update_success_status |= os.system('cd /tmp/{0}/ && sudo python setup.py install'.format(source_folder))
                # if we are not successful in updating status
                if update_success_status != 0: 
                    sys.stdout.write(red("\nError occured while updating ptop.\n"))
                    sys.stdout.write(red("Please report the issue at https://github.com/darxtrix/ptop/issues with the terminal output.\n"))
                    sys.stdout.flush()
                    sys.exit(1)

    except Exception as e:
        logger.info("Exception :: main.py :: Exception occured while updating ptop "+str(e))



def main():
    try:
        # app wide global stop flag
        global_stop_event = threading.Event()

        # command line argument parsing
        parser = argparse.ArgumentParser(description='ptop argument parser')
        
        parser.add_argument('-a','--address',
                            dest='dask_address',
                            action='store',
                            type=str,
                            required=True,
                            help=
                            '''
                                dask-distributed scheduler address.
                                
                                ie. 127.0.0.1:324597
                            ''')

        parser.add_argument('-r','--refresh',
                            dest='refresh',
                            action='store',
                            type=float,
                            default=500,
                            required=False,
                            help=
                            '''
                                Refresh rate in milliseconds
                                Default 500
                            ''')
                            
        parser.add_argument('-t','--theme',
                            dest='theme',
                            action='store',
                            type=str,
                            required=False,
                            choices=SUPPORTED_THEMES.keys(),
                            help=
                            '''
                                Valid themes are :
                                 elegant
                                 colorful
                                 dark
                                 light
                                 simple
                                 blackonwhite
                            ''')
                            
        parser.add_argument('-v','--version',
                            action='version',
                            version='ptop {}'.format(__version__))

        results = parser.parse_args()

        # commandline arguments massaging
        theme = (results.theme if results.theme else 'elegant')
        refresh_rate = results.refresh
        
        dask_sensor = DaskSensor(name='Dask', dask_address = results.dask_address, sensorType=None, interval=0.5)
        SENSORS_LIST = [dask_sensor]

        sensor_refresh_rates = {SENSORS_LIST[i]: refresh_rate for i in range(len(SENSORS_LIST))}

        # TODO ::  Catch the exception of the child thread and kill the application gracefully
        # https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
        s = Statistics(SENSORS_LIST,global_stop_event,sensor_refresh_rates)
        # internally uses a thread Job 
        s.generate()
        logger.info('Statistics generating started')

        app = PtopGUI(s.statistics,global_stop_event,theme,sensor_refresh_rates)
        # blocking call
        logger.info('Starting the GUI application')
        app.run()


    # catch the kill signals here and perform the clean up
    except KeyboardInterrupt:
        global_stop_event.set()
        # clear log file
        # Add code for wait for all the threads before join
        with open(_log_file,'w'):
            pass
        # TODO :Wait for threads to exit before calling systemExist
        raise SystemExit

    except Exception as e:
        global_stop_event.set()
        # don't clear the log file
        logger.info("Exception :: main.py "+str(e))
        print(sys.exc_info())
        raise SystemExit

if __name__ == '__main__':
    main()

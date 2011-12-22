import os
import sys
import timeit
import datetime
import logging_unterpolation

# 1000 logging statements
count = 1000

setup_statement = "import logging;logging.basicConfig(level=logging.{logging_level}, file='logfile.txt');loop = range(%s);{patched_command}" % count

results = open(os.path.join(os.path.dirname(__file__), 'performance_results.txt'), 'a+')

def show_results(result):
    "Print results in terms of microseconds per pass."
    global count
    per_pass = 1000000 * (result / count)
    results.write('%.2f usec/pass\n' % (per_pass,))

def conduct_logging(patched, level, interpolated, formatted): 
    
    assert not (interpolated and formatted)
    if not (interpolated or formatted):
        prototype = 'i'
    elif interpolated:
        prototype = '"%d", i'
    else:
        prototype = '"{0}", i'

    if patched:
        patched_command = 'from logging_unterpolation.tests.performance_results import logging_unterpolation; logging_unterpolation.patch_logging();'
        patched_status = 'patched'
    else:
        patched_command = ''
        patched_status = 'unpatched'

    results.write('{patched_status} logger, {logging_level} level, logging statement: logging.debug({prototype})\n'.format(patched_status=patched_status, logging_level=level, prototype=prototype))
    sys.stdout.flush()
    t = timeit.Timer("""
for i in loop:
    logging.debug({prototype})
""".format(prototype=prototype),
                    setup_statement.format(logging_level=level, patched_command=patched_command))
    show_results(t.timeit(number=count))

results.write('results for {0}, on {1}, over {2} records\n'.format(sys.version, datetime.datetime.utcnow().strftime("%A %d. %B %Y"), count))
conduct_logging(patched=False, level='WARNING', interpolated=False, formatted=False)
conduct_logging(patched=False, level='WARNING', interpolated=True, formatted=False)
conduct_logging(patched=False, level='DEBUG', interpolated=False, formatted=False)
conduct_logging(patched=False, level='DEBUG', interpolated=True, formatted=False)
conduct_logging(patched=True, level='WARNING', interpolated=False, formatted=False)
conduct_logging(patched=True, level='WARNING', interpolated=True, formatted=False)
conduct_logging(patched=True, level='WARNING', interpolated=False, formatted=True)
conduct_logging(patched=True, level='DEBUG', interpolated=False, formatted=False)
conduct_logging(patched=True, level='DEBUG', interpolated=True, formatted=False)
conduct_logging(patched=True, level='DEBUG', interpolated=False, formatted=True)
results.close()

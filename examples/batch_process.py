from EinsteinVision.EinsteinVision import EinsteinVisionService
from threaded_processing import *
from queue import Queue
import os
import time
import json
import sys

if len(sys.argv) < 3:
    print('\nWrong number of arguments. Usage:\npython batch_process.py email@email.com file.pem\n')
    sys.exit(1)

model_id = 'GeneralImageClassifier'
e = EinsteinVisionService(email=sys.argv[1], pem_file=sys.argv[2])

print('\nAcquiring Token so we can call API')
e.get_token()
print('Done.')

threadID = 1
threadList = ["T1", "T2", "T3", "T4", "T5"]
runningThreads = []
queueLock = threading.Lock()

result_q = Queue()
work_q = Queue()

print('\nGetting jpg filenames from images folder...')

photos = os.listdir('images/')
photos = [p for p  in photos if '.jpg' in p]

for img in photos:
    work_q.put('images/'+img)

print('Done.')

tick = time.time()

for tName in threadList:
    t = myThread(threadID, tName, work_q, result_q, e, model_id, queueLock)
    runningThreads.append(t)
    t.start()
    threadID += 1    

for t in runningThreads:
    t.join()

tock = time.time()

print('\nFinished. Number os Results: %s' % (result_q.qsize()))
print('Time taken in seconds: %s' % (tock-tick))

print('Writing results to resuls.json...')
results = []
while not result_q.empty():
    results.append(result_q.get())

f = open('results.json', 'w')

f.write('[')

for line in results[:-1]:
    l = line[2]
    l['filename'] = line[1]
    f.write(json.dumps(l) + ',\n')

# write last line to avoid the ","
l = results[len(results)-1]
l[2]['filename'] = l[1]
f.write(json.dumps(l[2]))
f.write(']')

f.close()

print('\n\n*** Process finished, check results.json ***\n\n')

import queue
import threading
import time

class myThread (threading.Thread):
    
    def __init__(self, threadID, name, q, result_q, einstein, model_id, the_lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.result_q = result_q
        self.einstein = einstein
        self.the_lock = the_lock
        self.model_id = model_id
    
    def run(self):
        print ("Starting " + self.name)
        process_data(self.name, self.q, self.result_q, self.einstein, self.model_id, self.the_lock)
        print ("Exiting " + self.name)


def process_data(threadName, workQueue, result_q, einstein, model_id, the_lock):
    
    while not workQueue.empty():
        
        the_lock.acquire()             
        data = workQueue.get()
        the_lock.release()

        print ("%s processing %s" % (threadName, data))
        r = einstein.get_fileb64_image_prediction(model_id=model_id, filename=data)
        
        # may need to refresh token
        if 'message' in r.json():
            if 'Invalid' in r.json()['message']:
                the_lock.acquire()
                einstein.get_token()
                the_lock.release()
                
                # Try again:
                r = einstein.get_fileb64_image_prediction(model_id=model_id, filename=data)
        
        result_q.put((threadName, data, r.json()))
        

import time

def timeDecorator(function):
    def timeWrapper(*args, **kwargs):
        start = time.time()
        results = function(*args, **kwargs)
        #print(results)
        print("Time taken to execute function " + function.__name__ + " is "+ str(time.time()-start) + " seconds.")
        return results
    return timeWrapper

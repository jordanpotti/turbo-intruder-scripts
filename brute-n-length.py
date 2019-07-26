# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/tree/master/resources/examples
# Turbo Intruder brute force string with N char length
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False,
                           maxQueueSize=10,
                           timeout=5,
                           maxRetriesPerRequest=3
                           )
    engine.start()

    for i in range(3, 8):
        engine.queue(target.req, randstr(i), learn=1)
        engine.queue(target.req, target.baseInput, learn=2)

    from itertools import product
    from string import ascii_letters, digits # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    N = 3
    for i in product(ascii_letters + digits, repeat=N):
        engine.queue(target.req, ''.join(i))


def handleResponse(req, interesting):
    # attributes are req.status, req.wordcount, req.length and req.response
    # if '200 Ok' not in req.response:
    if req.status != 404:
        table.add(req)
    if interesting:
        table.add(req)
        #callbacks.addToSiteMap(req.getBurpRequest())
        # You can also trigger scans, report issues, send to spider, etc:
        # https://portswigger.net/burp/extender/api/burp/IBurpExtenderCallbacks.html

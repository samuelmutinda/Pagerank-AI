import random
import copy
import datetime

def transition_model(corpus, page, damping_factor):
    distribution = dict.fromkeys(corpus)
    pages = list(corpus.keys())
    links = list(corpus[page])
    numberofpages = len(pages)
    numberoflinks = len(links)
    if not corpus[page]:
        pageprobability = 1 / numberofpages
        for page in corpus:
            distribution[page] = pageprobability
        return distribution
    probabilityoflink = damping_factor / numberoflinks
    pageprobability = (1 - damping_factor) / numberofpages
    for p in corpus:
        distribution[p] = pageprobability
    for link in links:
        distribution[link] += probabilityoflink
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    pagerankdict = dict.fromkeys(corpus, 0)
    randompage = random.choice([key for key in corpus.keys()])
    numberofsamples = n
    for i in range(n):
        pagerankdict[randompage] += 1
        distribution = transition_model(corpus, randompage, damping_factor)
        sampleweights = []
        pageslist = []
        for d in distribution:
            pageslist.append(d)
            sampleweights.append(distribution[d])
        randompage = random.choices(pageslist, sampleweights, k=1).pop()
        i += 1
    for key in pagerankdict.keys():
        pagerankdict[key] /= numberofsamples
    return pagerankdict

def modifypagerank(page, corpus, damping_factor, pagerankdict):
    numberofpages = len(corpus)
    parta = (1 - damping_factor) / numberofpages
    summation = 0
    for corpuspage in corpus:
        if corpus[corpuspage] != set():
            if page in corpus[corpuspage]:
                numberoflinks = len(corpus[corpuspage])
                summation += pagerankdict[corpuspage] / numberoflinks
        else:
            summation += pagerankdict[corpuspage] / numberofpages
        partb = damping_factor * summation
        pagerank = parta + partb
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    numberofpages = len(corpus.keys())
    pagerankdict = dict.fromkeys(corpus, 1/numberofpages)
    modifiedpagerankdict = dict.fromkeys(corpus, 1/numberofpages)
    for page in corpus:
        modifiedpagerankdict[page] = modifypagerank(page, corpus, damping_factor, modifiedpagerankdict)
    maxerror = 1
    while maxerror >= 0.001:
        pagerankdict = modifiedpagerankdict.copy()
        for page in corpus:
            modifiedpagerankdict[page] = modifypagerank(page, corpus, damping_factor, modifiedpagerankdict)
        errors = []
        for page in corpus:
            error = abs(pagerankdict[page] - modifiedpagerankdict[page])
            errors.append(error)
        maxerror = max(errors)
    return pagerankdict

corpus = {"1.html": {"2.html", "3.html"}, 
          "2.html":{"3.html"}, 
          "3.html": {"2.html"},
          "4.html": {"2.html"}
           }
print(sample_pagerank(corpus, 0.85, 1000))
print(iterate_pagerank(corpus, 0.85))
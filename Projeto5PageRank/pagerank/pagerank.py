import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = dict()

    if not corpus[page]:
        probability = 1 / len(corpus)
        for p in corpus:
            distribution[p] = probability
        return distribution
    
    
    currentPageLinks = corpus[page]
    numberOfLinks = len(currentPageLinks)
    probabilityOfEachPage = (damping_factor / numberOfLinks) + ((1 - damping_factor) / len(corpus))
    
    for p in corpus:
        if p in currentPageLinks:
            distribution[p] = (damping_factor / numberOfLinks) + ((1 - damping_factor) / len(corpus))
        else:
            distribution[p] = (1 - damping_factor) / len(corpus)

    return distribution
    #{"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Calcular o modelo de transição da página atual: Chame a sua função transition_model para obter as probabilidades:
    #Sortear a próxima página com base nas probabilidades do modelo: Para isso, use random.choices, que aceita pesos:
    #Depois do loop, transformar os contadores em probabilidades: Divida cada contador por n:
    cont = dict()
    for page in corpus:
        cont[page] = 0
    
    randomPage = random.choice(list(corpus.keys()))

    for i in range(n):
        cont[randomPage] += 1
        model = transition_model(corpus, randomPage, damping_factor)
        pages = list(model.keys())
        probabilitiesOfTheRandomPage = list(model.values())
        randomPage = random.choices(pages, probabilitiesOfTheRandomPage, k=1)[0]


    pageRank = dict()
    for page in corpus:
        pageRank[page] = cont[page] / n 

    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    N = len(corpus)
    constant = (1 - damping_factor) / N
    pageRank = dict()
    for page in corpus:
        pageRank[page] = 1 / len(corpus)
    converged = False
    
    while not converged:
        new_rank = {}
        
        for page in corpus:
            total = 0

            for possible_page in corpus:
                links = corpus[possible_page]

                if not links:
                    links = corpus.keys()

                if page in links:
                    total += pageRank[possible_page] / len(links)

            new_rank[page] = constant + damping_factor * total
                
        converged = True
        
        for page in pageRank:
            if abs(new_rank[page] - pageRank[page]) > 0.001:
                converged = False
        pageRank = new_rank
            
    return pageRank    


if __name__ == "__main__":
    main()

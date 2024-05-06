from pubmed_xml import Pubmed_XML_Parser
import pandas as pd

# pubmed = Pubmed_XML_Parser()

data = []
def MetadataFinder(pmid):
    pubmed = Pubmed_XML_Parser()
    for article in pubmed.parse(pmid):
        # print(article)        # Article<30003002>
        # print(article.data)   # dict object
        # print(article.to_json(indent=2))   # json string
        # print(article.pmid, article.title, article.abstract) # by attribute
        # print(article['pmid'], article['title'], article['abstract']) # by key
        # print(article['pmid'], article['title']) # by key
        print(article.authors)
        data.append({
            'PMID': article['pmid'],
            'Title': article['title'],
            'DOI':article['doi'],
            'Author':article['authors']
        })
    return data



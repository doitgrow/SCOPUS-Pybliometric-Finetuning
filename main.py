from pybliometrics.scopus import ScopusSearch, AffiliationRetrieval
from collections import defaultdict
from datetime import datetime
import pandas as pd

def to_strftime(date:tuple)-> str: 
    date_created = datetime(date[0], date[1], date[2]) # ex) data = (2021, 9, 20)
    return date_created.strftime("%Y-%m-%d")

class Paper(ScopusSearch):
    
    def __init__(self, *args, **kwargs):
        ScopusSearch.__init__(self, *args, **kwargs)
        # super(Paper, self).__init__(*args, **kwargs) # available instead a line above
        self.affiliation_ids = []
        self.affiliations = defaultdict(list)

    def __len__(self):
        return len(self.results)

    @property
    def eids(self):
        self._eids = self._get_eids()
        return self._eids

    def _get_eids(self):
        eids = [doc.eid for doc in self.results]
        return eids

    @property
    def afids(self):
        self._afids = self._get_afids()
        return list(set(self._afids))

    def _get_afids(self):
        for doc in self.results:
            if doc.author_afids is None:
                continue
            for afid in doc.author_afids.split(";"):
                if afid == '':
                    continue
                if '-' in afid:
                    for _afid in afid.split("-"):
                        self.affiliation_ids.append(_afid.strip())
                else:
                    self.affiliation_ids.append(afid.strip())
        return self.affiliation_ids

    def get_affiliations(self):
        affiliation_ids = self.afids
        for afid in affiliation_ids:
            affiliations = self.Affiliation(afid)
            self.affiliations['afid'].append(afid)
            self.affiliations['affiliation_name'].append(affiliations.affiliation_name)
            self.affiliations['country'].append(affiliations.country)
            self.affiliations['date_created'].append(to_strftime(affiliations.date_created))
            self.affiliations['author_count'].append(affiliations.author_count)
            self.affiliations['document_count'].append(affiliations.document_count)
            self.affiliations['org_type'].append(affiliations.org_type)
            
        return pd.DataFrame(self.affiliations)


    # Affiliation Retrieval Class 
    class Affiliation(AffiliationRetrieval):

        def __init__(self, *args, **kwargs):
            AffiliationRetrieval.__init__(self, *args, **kwargs)
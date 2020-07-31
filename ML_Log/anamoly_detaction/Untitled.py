#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[80]:


file=pd.read_csv('weblog.csv')


# In[81]:


f=file.values


# In[83]:


np.unique(f[:10000,0])


# In[ ]:


lines = list()

members= input("Please enter a member's name to be deleted.")

with open('weblog.csv', 'r') as readFile:

    reader = csv.reader(readFile)

    for row in reader:

        lines.append(row)
        if len(row[0])!=10:
            

        for field in row:

            if field == members:

                lines.remove(row)


# In[94]:


df=pd.DataFrame(f[:5000,[0,1,3]],columns=['ip','date','status'])


# In[95]:


df


# In[113]:


for i in range(df.shape[0]):
    df['date'][i]=df['date'][i][1:]
    df[]


# In[ ]:





# In[114]:


df


# In[117]:


from datetime import datetime

# current date and time
now = datetime.now()

timestamp = datetime.timestamp(14/Nov)
print("timestamp =", timestamp,' ',datetime.now())


# In[84]:


from sklearn.preprocessing import LabelEncoder


# In[85]:


le =LabelEncoder()


# In[96]:


ds=df.apply(le.fit_transform)


# In[101]:


d=ds.values


# In[109]:


d


# In[98]:


from sklearn.cluster import DBSCAN


# In[105]:


dbs=DBSCAN(eps=0.24,min_samples=10)


# In[106]:


dbs.fit(d)


# In[108]:


dbs.fit_predict(d)


# In[7]:


from logmine import *


# In[4]:


pip install logmine


# In[3]:


pip install --upgrade pip


# In[8]:


import logmine as l


# In[27]:


import sys
import re
import os
import allignment
import copy
import hashlib
import pandas as pd
from datetime import datetime
from collections import defaultdict

class partition():
    def __init__(self, idx, log="", lev=-1):
        self.logs_idx = [idx]
        self.patterns = [log]
        self.level = lev


# In[20]:


pip install alignment


# In[21]:


pip install copy


# In[30]:


class LogParser():
    def __init__(self, indir, outdir, log_format, max_dist=0.001, levels=2, k=1, k1=1, k2=1, alpha=100, rex=[]):
        self.logformat = log_format
        self.path = indir
        self.savePath = outdir
        self.rex = rex
        self.levels = levels
        self.max_dist = max_dist
        self.k = k
        self.k1 = k1
        self.k2 = k2
        self.alpha = alpha
        self.df_log = None
        self.logname = None
        self.level_clusters = {}


    def parse(self, logname):
        print('Parsing file: ' + os.path.join(self.path, logname))
        self.logname = logname
        starttime = datetime.now()
        self.load_data()
        for lev in range(self.levels):
            if lev == 0:
                # Clustering
                self.level_clusters[0] = self.get_clusters(self.df_log['Content_'], lev)
            else:
                # Clustering
                patterns = [c.patterns[0] for c in self.level_clusters[lev-1]]
                self.max_dist *= self.alpha
                clusters = self.get_clusters(patterns, lev, self.level_clusters[lev-1])

                # Generate patterns
                for cluster in clusters:
                    cluster.patterns = [self.sequential_merge(cluster.patterns)]
                self.level_clusters[lev] = clusters
        self.dump()
        print('Parsing done. [Time taken: {!s}]'.format(datetime.now() - starttime))

    def dump(self):
        if not os.path.isdir(self.savePath):
            os.makedirs(self.savePath)

        templates = [0] * self.df_log.shape[0]
        ids = [0] * self.df_log.shape[0]
        templates_occ = defaultdict(int)
        for cluster in self.level_clusters[self.levels-1]:
            EventTemplate = cluster.patterns[0]
            EventId = hashlib.md5(' '.join(EventTemplate).encode('utf-8')).hexdigest()[0:8]
            Occurences = len(cluster.logs_idx)
            templates_occ[EventTemplate] += Occurences

            for idx in cluster.logs_idx:
                ids[idx] = EventId
                templates[idx]= EventTemplate
        self.df_log['EventId'] = ids
        self.df_log['EventTemplate'] = templates

        occ_dict = dict(self.df_log['EventTemplate'].value_counts())
        df_event = pd.DataFrame()
        df_event['EventTemplate'] = self.df_log['EventTemplate'].unique()
        df_event['Occurrences'] = self.df_log['EventTemplate'].map(occ_dict)
        df_event['EventId'] = self.df_log['EventTemplate'].map(lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()[0:8])

        self.df_log.drop("Content_", inplace=True, axis=1)
        self.df_log.to_csv(os.path.join(self.savePath, self.logname + '_structured.csv'), index=False)
        df_event.to_csv(os.path.join(self.savePath, self.logname + '_templates.csv'), index=False, columns=["EventId","EventTemplate","Occurrences"])

    def get_clusters(self, logs, lev, old_clusters=None):
        clusters = []
        old_clusters = copy.deepcopy(old_clusters)
        for logidx, log in enumerate(logs):
            match = False
            for cluster in clusters:
                dis = self.msgDist(log, cluster.patterns[0]) if lev == 0 else self.patternDist(log, cluster.patterns[0])
                if dis and dis < self.max_dist:
                    if lev == 0:
                        cluster.logs_idx.append(logidx)
                    else:
                        cluster.logs_idx.extend(old_clusters[logidx].logs_idx)
                        cluster.patterns.append(old_clusters[logidx].patterns[0])
                    match = True

            if not match: 
                if lev == 0:
                    clusters.append(partition(logidx, log, lev)) # generate new cluster
                else:
                    old_clusters[logidx].level = lev
                    clusters.append(old_clusters[logidx]) # keep old cluster

        return clusters

    def sequential_merge(self, logs):
        log_merged = logs[0]
        for log in logs[1:]:
            log_merged = self.pair_merge(log_merged, log)
        return log_merged

    def pair_merge(self, loga, logb):
        loga, logb = allignment.water(loga.split(), logb.split())
        logn = []
        for idx, value in enumerate(loga):
            logn.append('<*>' if value != logb[idx] else value)
        return " ".join(logn)

    def print_cluster(self, cluster):
        print("------start------")
        print("level: {}".format(cluster.level))
        print("idxs: {}".format(cluster.logs_idx))
        print("patterns: {}".format(cluster.patterns))
        print("count: {}".format(len(cluster.patterns)))
        for idx in cluster.logs_idx:
            print(self.df_log.iloc[idx]['Content_'])
        print("------end------")

    def msgDist(self, seqP, seqQ):
        dis = 1
        seqP = seqP.split()
        seqQ = seqQ.split()
        maxlen = max(len(seqP), len(seqQ))
        minlen = min(len(seqP), len(seqQ))
        for i in range(minlen):
            dis -= (self.k if seqP[i]==seqQ[i] else 0 * 1.0) / maxlen
        return dis

    def patternDist(self, seqP, seqQ):
        dis = 1
        seqP = seqP.split()
        seqQ = seqQ.split()
        maxlen = max(len(seqP), len(seqQ))
        minlen = min(len(seqP), len(seqQ))
        for i in range(minlen):
            if seqP[i] == seqQ[i]:
                if seqP[i] == "<*>":
                    dis -= self.k2 * 1.0 / maxlen
                else:
                    dis -= self.k1 * 1.0 / maxlen
        return dis

    def load_data(self):
        def preprocess(line):
            for currentRex in self.rex:
                line = re.sub(currentRex, '', line)
            return line

        headers, regex = self.generate_logformat_regex(self.logformat)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logname), regex, headers, self.logformat)
        self.df_log['Content_'] = self.df_log['Content'].map(preprocess)

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        ''' Function to transform log file to dataframe '''
        log_messages = []
        linecount = 0
        with open(log_file, 'r') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf

    def generate_logformat_regex(self, logformat):
        ''' 
        Function to generate regular expression to split log messages
        '''
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex


# In[31]:


l=LogParser('./a.log',',/ab/',)


# In[35]:


import sys
#sys.path.append('../')
#from logparser import LogMine

input_dir  = './' # The input directory of log file
output_dir = './aaa/' # The output directory of parsing results
log_file   = 'ss.log' # The input log file name
log_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>' # HDFS log format
log_format = '<Pid> <Date> <Time> <Level> <Component>: <Content>'
levels     = 2 # The levels of hierarchy of patterns
max_dist   = 0.001 # The maximum distance between any log message in a cluster and the cluster representative
k          = 1 # The message distance weight (default: 1)
regex      = []  # Regular expression list for optional preprocessing (default: [])

parser = LogParser(input_dir, output_dir, log_format, rex=regex, levels=levels, max_dist=max_dist, k=k)
parser.parse(log_file)


# In[38]:


from ..utils import logloader
from collections import defaultdict, Counter, OrderedDict
import re
import pandas as pd
import os
from datetime import datetime
import multiprocessing as mp
import itertools
import hashlib
import numpy as np


class PatternMatch(object):

    def __init__(self, outdir='./result/', n_workers=1, optimized=False, logformat=None):
        self.outdir = outdir
        if not os.path.exists(outdir):
            os.makedirs(outdir) # Make the result directory
        self.template_match_dict = defaultdict(dict)
        self.template_freq_dict = Counter()
        self.logformat = logformat
        self.n_workers = n_workers
        self.optimized = optimized

    def add_event_template(self, event_template, event_Id=None):
        if not event_Id:
            event_Id = self._generate_hash_eventId(event_template)
        if self.optimized:
            start_token = event_template.split(' ')[0]
            if re.search(r'<.*?>', start_token):
                start_token = '<*>'
            self.template_match_dict[start_token][self._generate_template_regex(event_template)] = (event_Id, event_template)
        else:
            self.template_match_dict[self._generate_template_regex(event_template)] = (event_Id, event_template)

    def _generate_template_regex(self, template):
        template = re.sub(r'(<\*>\s?){2,}', '<*>', template)
        regex = re.sub(r'([^A-Za-z0-9])', r'\\\1', template)
        regex = regex.replace('\<\*\>', '(.*?)')
        regex = regex.replace('\<NUM\>', '(([\-|\+]?\d+)|(0[Xx][a-fA-F\d]+))')
        regex = regex.replace('\<IP\>', '((\d+\.){3}\d+)')
        regex = '^' + regex + '$'
        return regex

    def match_event(self, event_list):
        match_list = []
        paras = []
        if self.n_workers == 1:
            results = match_fn(event_list, self.template_match_dict, self.optimized)
        else:
            pool = mp.Pool(processes=self.n_workers)
            chunk_size = len(event_list) / self.n_workers + 1
            result_chunks = [pool.apply_async(match_fn, args=(event_list[i:i + chunk_size], self.template_match_dict, self.optimized))                             for i in xrange(0, len(event_list), chunk_size)]
            pool.close()
            pool.join()
            results = list(itertools.chain(*[result.get() for result in result_chunks]))
        for event, parameter_list in results:
            self.template_freq_dict[event] += 1
            paras.append(parameter_list)
            match_list.append(event)
        return match_list, paras

    def read_template_from_csv(self, template_filepath):
        template_dataframe = pd.read_csv(template_filepath)
        for idx, row in template_dataframe.iterrows():
            event_Id = row['EventId']
            event_template = row['EventTemplate']
            self.add_event_template(event_template, event_Id)


    def match(self, log_filepath, template_filepath):
        print('Processing log file: {}'.format(log_filepath))
        start_time = datetime.now()
        loader = logloader.LogLoader(self.logformat, self.n_workers)
        self.read_template_from_csv(template_filepath)
        log_dataframe = loader.load_to_dataframe(log_filepath)
        print('Matching event templates...')
        match_list, paras = self.match_event(log_dataframe['Content'].tolist())
        log_dataframe = pd.concat([log_dataframe, pd.DataFrame(match_list, columns=['EventId', 'EventTemplate'])], axis=1)
        log_dataframe['ParameterList'] = paras
        self._dump_match_result(os.path.basename(log_filepath), log_dataframe)
        match_rate = sum(log_dataframe['EventId'] != 'NONE') / float(len(log_dataframe))
        print('Matching done, matching rate: {:.1%} [Time taken: {!s}]'.format(match_rate, datetime.now() - start_time))
        return log_dataframe

    def _dump_match_result(self, log_filename, log_dataframe):
        log_dataframe.to_csv(os.path.join(self.outdir, log_filename + '_structured.csv'), index=False)
        template_freq_list = [[eventId, template, freq] for (eventId, template), freq in self.template_freq_dict.iteritems()]
        template_freq_df = pd.DataFrame(template_freq_list, columns=['EventId', 'EventTemplate', 'Occurrences'])
        template_freq_df.to_csv(os.path.join(self.outdir, log_filename + '_templates.csv'), index=False)

    def _generate_hash_eventId(self, template_str):
        return hashlib.md5(template_str.encode('utf-8')).hexdigest()[0:8]

    def _get_parameter_list(self, row):
        template_regex = re.sub(r'([^A-Za-z0-9])', r'\\\1', row["EventTemplate"])
        template_regex = "^" + template_regex.replace("\<\*\>", "(.*?)") + "$"
        parameter_list = re.findall(template_regex, row["Content"])
        parameter_list = parameter_list[0] if parameter_list else ()
        parameter_list = list(parameter_list) if isinstance(parameter_list, tuple) else [parameter_list]
        return parameter_list

def match_fn(event_list, template_match_dict, optimized=True):
    print("Worker {} start matching {} lines.".format(os.getpid(), len(event_list)))
    match_list = [regex_match(event_content, template_match_dict, optimized)
                  for event_content in event_list]
    return match_list

def regex_match(msg, template_match_dict, optimized):
    matched_event = None
    template_freq_dict = Counter()
    match_dict = template_match_dict
    parameter_list = []
    if optimized:
        start_token = msg.split(' ')[0]
        if start_token in template_match_dict:
            match_dict = template_match_dict[start_token]
            if len(match_dict) > 1:
                match_dict = OrderedDict(sorted(match_dict.items(), 
                     key=lambda x: (len(x[1][1]), -x[1][1].count('<*>')), reverse=True))
            for regex, event in match_dict.iteritems():
                parameter_list = re.findall(regex, msg.strip())
                if parameter_list:
                    matched_event = event
                    break    
    
    if not matched_event:
        if optimized:
            match_dict = template_match_dict['<*>']
        if len(match_dict) > 1:
            match_dict = OrderedDict(sorted(match_dict.items(), 
                 key=lambda x: (len(x[1][1]), -x[1][1].count('<*>')), reverse=True))
        for regex, event in match_dict.iteritems():
            parameter_list = re.findall(regex, msg.strip())
            if parameter_list:
                matched_event = event
                break    

    if not matched_event:
        matched_event = ('NONE', 'NONE')
    if parameter_list:
        parameter_list = list(parameter_list[0])
    return matched_event, parameter_list


# In[37]:


import ..utils


# In[ ]:





import sys
import csv
import networkx as nx

from collections import defaultdict
from django.conf import settings


from nltk.tokenize import word_tokenize
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords
from collections import Counter


path1 = settings.MEDIA_ROOT
STOPLIST_FILE = path1 + "/stoplist.txt"
ALLOWLIST_FILE = path1 + "/allowlist.txt"

G = defaultdict(int)

stoplist = []
allowlist = []



class Graph:


    def read_stoplist(self):
        """
        This function is used to read stoplist
        """
        global stoplist
        with open(STOPLIST_FILE) as input_file:
            for line in input_file:
                line = line.strip()
                stoplist.append(line)

    def read_allowlist(self):
        """
        This function is used to read set of allowed token generally for Titles
        """
        global allowlist
        with open(ALLOWLIST_FILE) as input_file:
            for line in input_file:
                line = line.strip()
                allowlist.append(line)

    def get_frequencies(self, desc):

        stopset = set(stopwords.words('english'))
        filter_stops = lambda w: len(w) < 3 or w in stopset
        words = word_tokenize(desc)

        print '------gram--------'
        words_to_count = [word for word in words if word not in stopset]
        words_to_count = [word for word in words_to_count if not len(word) < 3]
        c = Counter(words_to_count)
        single = c.most_common(20)
        print single

        print '------bigram--------'
        bcf = BigramCollocationFinder.from_words(words)
        bcf.apply_word_filter(filter_stops)
        bigrm = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 15)
        print bigrm

        print '------trigram--------'
        tcf = TrigramCollocationFinder.from_words(words)
        tcf.apply_word_filter(filter_stops)
        tcf.apply_freq_filter(3)  #only keep those that appear more than 3 times
        trigrm = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 10)
        print trigrm

        matches = [single,bigrm,trigrm]
        return matches


    def clean_job_title(self,title):
        """
        This method is used to clean titles, so we can generate graphs of them
        """
        result = []

        title = title.replace("\"", "")

        if title.find("/") != -1:
            title = title[:title.find("/")]

        if title.find("-") != -1:
            title = title[:title.find("-")]

        if title.find(",") != -1:
            title = title[:title.find(",")]

        if title.find("&") != -1:
            title = title[:title.find("&")]

        for token in title.split(" "):
            if token.lower() not in stoplist and token.strip() != "":
                if token not in allowlist:
                    result.append(token.title())
                else:
                    result.append(token)

        return " ".join(result)

    def update_graph(self,titles):
        """
        This method contains logic of how we process titles
        """
        global G
        for i in range(1, len(titles)):
            if titles[i - 1] != titles[i]:
                k = "%s\t%s" % (titles[i - 1], titles[i])
                G[k] += 1

    def render_graph(self, output_file):
        """
        This method is used to render graph of Job Descriptions
        """
        X = nx.Graph()
        for k,v in G.items():
            a, b = k.split("\t")
            X.add_weighted_edges_from([(a, b, v)])
        nx.write_dot(X, output_file)

    def process(self, input_file, output_file):
        """
        This function is used to process data for given input and output filenames
        """

        gr = Graph()
        gr.read_stoplist()
        gr.read_allowlist()
        current_resume_id = ""
        current_job_titles = []


        with open(input_file, 'rb') as file_to_read:
            #Skip the header
            for line in file_to_read.readlines()[1:]:
                line = line.strip()
                rec = line.split(";")
                resume_id, url, job_id,job_title = rec[:4]

                if current_resume_id == "":
                    current_resume_id = resume_id

                if resume_id != current_resume_id:
                    gr.update_graph(current_job_titles)
                    current_job_titles = []
                    current_resume_id = resume_id

                current_job_title = gr.clean_job_title(job_title)
                if current_job_title.strip() != "":
                    current_job_titles.append(current_job_title)


    #if __name__ == "__main__":
    #    if len(sys.argv) < 2:
    #        print "Please sepcify input and output file names"
    #        sys.exit(0)
    #    input_file, output_file = sys.argv[1:]

    def graph_main(self, input_file, output_file):
        gr = Graph()
        matches = gr.process(input_file, output_file)
        gr.render_graph(output_file)

        desc = ""
        title = ""

        with open(input_file,'rb') as csvfile:
            sreader = csv.reader(csvfile, delimiter=';')
            for row in sreader:
                desc1 = row[10]
                desc = desc + " " + desc1
                titl1 = row[3]
                title = title + " " + titl1

        matches = gr.get_frequencies(desc)
        tite = gr.get_frequencies(title)


        return  {'matches':matches, 'title':tite}








__author__ = 'nnyegaard'

import math
import re
import feedparser


def sampletrain(cl):
    cl.train("Nobody owns the water.", "good")
    cl.train("the quick rabbit jumps fences", "good")
    cl.train("buy pharmaceuticals now", "bad")
    cl.train("make quick money at the online casino", "bad")
    cl.train("the quick brown fox jumps", "good")


def getwords(doc):
    splitter = re.compile('\\W*')
    # Split the words by non-alpha characters
    words = [s.lower() for s in splitter.split(doc) if 2 < len(s) < 20]
    # Return the unique set of words only
    return dict([(w, 1) for w in words])


class classifier(object):
    def __init__(self, getfeatures):
        self.thresholds = {}
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures

    # Increase the count of a feature/category pair
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # Increase the count of a category
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    # The number of times a feature has appeared in a category
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values())

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f, cat)
            # Increment the count for this category
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1, ap=0.7):
        basicprob = prf(f, cat)
        totals = sum([self.fcount(f, c) for c in self.categories()])
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp

    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]


class naivebayes(classifier):
    def docprob(self, item, cat):
        features = self.getfeatures(item)

        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

    def classify(self, item, default=None):
        probs = {}
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.getthreshold(best) > probs[best]:
                return default
            return best


class fisherclassifier(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.minimums = {}

    def cprob(self, f, cat):
        clf = self.fprob(f, cat)
        if clf == 0:
            return 0

        freqsum = sum([self.fprob(f, c) for c in self.categories()])
        p = clf / freqsum
        return p

    def fisherprob(self, item, cat):
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
        fscore = -2 * math.log(p)

        return self.invchi2(fscore, len(features) * 2)

    def setminimum(self, cat, min):
        self.minimums[cat] = min

    def getminimum(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def classify(self, item, default=None):
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)

        for i in range(1, df // 2):
            term *= m / 1
            sum += term
        return min(sum, 1.0)


def read(feed, classifier):
    f = feedparser.parse(feed)

    for entry in f['entries']:
        print
        print "_____"
        print "Title:        " + entry["title"].encode("utf-8")
        print "Publisher:        " + entry["publisher"].encode("utf-8")
        print
        print entry["summary"].encode("utf-8")

        # Combine all the text to create one item for the classifier
        fulltext = '%s\n%s\n%s' % (entry['title'], entry['publisher'], entry['summary'])

        print "Guess:   " + str(classifier.classify(fulltext))
        cl = raw_input("Enter category:  ")
        if cl == "":
            print "Will use my guess: " + str(classifier.classify(fulltext))
            classifier.train(fulltext, str(classifier.classify(fulltext)))
        else:
            classifier.train(fulltext, cl)


def entryfeatures(entry):
    splitter = re.compile("\\W*")
    f = {}

    titlewords = [s.lower() for s in splitter.split(entry['title']) if 2 < len(s) < 20]
    for w in titlewords:
        f["Title:" + w] = 1

    summarywords = [s.lower() for s in splitter.split(entry['summary']) if 2 < len(s) < 20]

    uc = 0
    for i in range(len(summarywords)):
        w = summarywords[i]
        f[w] = 1
        if w.isupper():
            uc += 1

        if i < len(summarywords) - 1:
            twowords = " ".join(summarywords[i:i + 1])
            f[twowords] = 1

        f["Publisher:" + entry["PUBLISHER"]] = 1

        if float(uc)/len(summarywords) > 0.3:
            f["UPPERCASE"] = 1

        return f


if __name__ == '__main__':
    # print "Test of naivebayes:"
    # cl = naivebayes(getwords)
    # sampletrain(cl)
    # print cl.classify("quick rabbit", default="unknow")
    # print cl.classify("quick money", default="unknow")
    # print cl.getthreshold("bad")
    # cl.setthreshold("bad", 3.0)
    # print cl.getthreshold('bad')
    # print cl.classify("quick money", default="unknow")
    # for i in range(10):
    #     sampletrain(cl)
    # print cl.classify("quick money", default="unknow")

    # print "Test of fisher"
    # cl = fisherclassifier(getwords)
    # sampletrain(cl)
    # print cl.cprob("quick", "good")
    # print cl.cprob("money", "bad")
    # print cl.weightedprob("money", "bad", cl.cprob)
    # print cl.fisherprob("quick rabbit", "good")
    # print cl.fisherprob("quick rabbit", "bad")
    # print "With classifier"
    # print cl.classify("quick rabbit")
    # print cl.classify("quick money")
    # cl.setminimum("bad", 0.8)
    # print cl.getminimum("bad")
    # print cl.classify("quick money")
    # cl.setminimum("good", 0.4)
    # print cl.classify("quick money")

    cl = fisherclassifier(getwords)
    read('http://kiwitobes.com/feeds/python_search.xml', cl)
    print cl.cprob("python", "prog")
    print cl.cprob("python", "snake")
    print cl.cprob("python", "monty")
    print cl.cprob("eric", "monty")
    print cl.fprob("eric", "monty")


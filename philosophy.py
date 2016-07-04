import urllib2
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
plt.style.use('ggplot')

def stripParentheses(string):
	"""
	Remove brackets from a string
	Leave brackets between "<a></a>" tags in place
	"""
	string = "" + str(string)
    	#print "input: ",string
    	parenMode = 0
    	tagMode = False
    	out = ''
    	for character in string:
    	#Check for tag when not in parantheses mode
		if parenMode < 1:
			if character == '>':
				tagMode = False
				
			if character == "<":
				tagMode = True
			
		#Check for parentheses
		if tagMode is False:
			if character == '(':
		    		parenMode += 1

			if parenMode > 0:
		    		out += ' '
			else:
		    		out += character

			if character == ')' :
		    		parenMode -= 1
		else:
			out += character
    	#print "output: ",out
    	return out

class pageTracker(object):
	"""
	This class tracks the links visited
	"""
	def __init__(self):
		self.path = []
		self.reachPhilosophy = False
		self.visited = None
		self.cachedLength = 0

	def addToPath(self, pageLink):
		self.path.append(pageLink)
		self.visited.add(pageLink)

	def pathLength(self):
		return len(self.visited) - 1

class wikiCrawler(object):
	"""
	This class folows a given or in this case a random wikipedia 
	article and folows it's trace to the philosophy page each 
	time following the first link in the article's content that is
	not within parantheses or italicized.
	"""
	def __init__(self, prefix="http://en.wikipedia.org", userAgent='Mozilla/5.0'):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [('User-agent', userAgent)]
		self.prefix = prefix

	def crawl(self, article, tracker, mem):
		print article
		resource = self.opener.open(article)
		data = resource.read()
		resource.close()
		soup = BeautifulSoup(stripParentheses(data))
		if tracker.visited is None:
			tracker.visited = set()
			print soup.title.string.rpartition('-')[0]
			tracker.addToPath(self.prefix + '/wiki/' + soup.title.string.rpartition('-')[0])
		else:
			tracker.addToPath(article)
		if article in mem: # Check cache if pagelink leads to the Philosophy Wikipedia Page
			t = mem[article]
			linkPath = t[1][1:]
			print 'Accessing Cached Results'
			tracker.reachPhilosophy = True
			for pageLink in linkPath:
				print pageLink
			tracker.cachedLength = t[0]
			return
		if soup.table is not None:
			soup.table.decompose()
		for paragraph in soup.find('div', id="bodyContent").find('div', id='mw-content-text').findAll('p'):
			for child in paragraph.children:
				if 'a' != child.name: #only obtain non-italicized links
					continue
				else:
					link = child
					k = 0
					if len(link.attrs) > 2: #Skip Wikitionary, Image Links
						if link.attrs['class'][0] == 'extiw' or link.attrs['class'][0] == 'image' or link.attrs['class'][0] == 'new':
							continue
					for val, att in link.attrs.iteritems():
						if val == "href":
							nexturl = att
						if val == "title":
							next = att
							k = 1
					if k == 0: #citations or something, no title, skip
						continue
					if next == "Philosophy":
						print "You have arrived to the Philosphy Page"
						tracker.reachPhilosophy = True
						tracker.addToPath('https://en.wikipedia.org/wiki/Philosophy')
						#Fill cache with the pagelinks visited
						for i, pageLink in enumerate(tracker.path):
							if pageLink not in mem:
								mem[pageLink] = (tracker.pathLength() - i, tracker.path[i:])
						return
					else:
						if not nexturl.startswith("http://"):
							nexturl = self.prefix + nexturl
						if nexturl in tracker.visited:
							print 'You have hit a loop!'
							return
						else:
							self.crawl(nexturl, tracker, mem)
							return	

	
if __name__ == '__main__':
	#Create a variable with the url
	url = 'https://en.wikipedia.org/wiki/Special:Random'
	prefix = 'https://en.wikipedia.org'
	crawler = wikiCrawler(prefix=prefix)
	total = 0
	philosophyHits = 0
	pageVisits = []
	mem = {}
	while philosophyHits < 500:
		tracker = pageTracker()
		crawler.crawl(article=url, tracker=tracker, mem=mem)
		if tracker.reachPhilosophy:
			philosophyHits += 1
			pageVisits.append(tracker.pathLength() + tracker.cachedLength)
			print 'Path Length to Philosophy: %s' %(tracker.pathLength() + tracker.cachedLength)
		print
		total += 1

	percentage = float(philosophyHits)/total*100.0
	print 'Percentage of pages that lead to Philosophy: %s%%.' %percentage

	plt.figure()
	plt.hist(pageVisits, 20, normed = True, facecolor='green', alpha=0.75)
	plt.xlabel('Page Visits to Philosopy')
	plt.ylabel('Frequency')
	plt.title('Distribution of Path Lengths')
	plt.savefig('PageLength_Distribution.png')




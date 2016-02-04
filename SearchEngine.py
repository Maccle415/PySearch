import stringParse
import operator
from datetime import datetime


__author__ = 'darrenleak'


class SearchEngine:

    haystack = []

    #this will create a unique list of words and store the index that relates to the app name in the appList
    uniqueWordList = {}

    bestScore = 0
    bestScoreHistory = []

    '''
        :param needle:
        :param haystack:
        :return:
    '''
    def search(self, needle, haystack):

        self.haystack = haystack

        #Do indexing work
        self.createUniqueWordList(haystack)

        #Create the scored list(contain all the values with their scores/order to )
        return self.createSearchScore(needle, haystack)

    '''
        This basically does the indexing

        - takes the haystack and splits is up into separate words
        - store the index of the app name from where it came from in the appList
    '''
    def createUniqueWordList(self, haystack):

        #make all of the words lowers case to make it easier to search
        haystack = map(str.lower, haystack)

        #loop through all appNames in the haystack
        for index, appName in enumerate(haystack):

            splitAppName = appName.split(" ")

            #loop through all words from splitAppName array
            for word in splitAppName:

                #add the word to unique list if does not exist
                if word not in self.uniqueWordList:
                    self.uniqueWordList[word] = []

                #add the index to the word
                self.uniqueWordList[word].append(index)

    #create filter and score the results
    def createSearchScore(self, needle, haystack):

        needles = needle.lower().split(" ")
        haystack = map(str.lower, haystack)

        appNamesWithScores = {}

        #checks how many words a search terms contains
        for singleNeedle in needles:

            for indexes in self.uniqueWordList[singleNeedle]:

                if self.haystack[indexes] not in appNamesWithScores:
                    appNamesWithScores[self.haystack[indexes]] = 5

                elif self.haystack[indexes] in appNamesWithScores:
                    appNamesWithScores[self.haystack[indexes]] += 5

        appNamesWithScoresToLower = map(str.lower, appNamesWithScores)
        curSearchIndex = 0

        for index, appName in enumerate(appNamesWithScoresToLower):

            origName = appName
            appName = appName.split(" ")
            curNeedle = needles[curSearchIndex]

            while curNeedle not in appName:

                curSearchIndex += 1
                curNeedle = needles[curSearchIndex]

            searchTermFirstIndex = appName.index(curNeedle)
            searchSubString = appName[searchTermFirstIndex:len(appName)]

            increaseScoreBy = self.score(needles, searchSubString)

            for i, a in enumerate(appNamesWithScores):
                if origName == a.lower():
                    appNamesWithScores[a] += increaseScoreBy

            curSearchIndex = 0

        sortedAppWithScores = sorted(appNamesWithScores.items(), key=operator.itemgetter(1))

        return list(reversed(sortedAppWithScores))

    #score system
    def score(self, searchTerm, searchSubString):

        searchSubString = map(str.lower, searchSubString)

        lastFiveWords = []

        curSearchTermIndex = 0
        curSearchTermSubStringIndex = 0
        curSubStringIndex = 0
        missedTerm = 1

        for subStringWord in searchSubString:

            if curSearchTermIndex < len(searchTerm) and searchTerm[curSearchTermIndex] == subStringWord:

                curSearchTermIndex += 1
                curSearchTermSubStringIndex = searchSubString.index(subStringWord)

                self.bestScore += 7
                self.bestScoreHistory.append(self.bestScore)

            elif curSearchTermIndex < len(searchTerm) and subStringWord in searchTerm:

                self.bestScore += (5 / missedTerm)

                self.bestScoreHistory.append(self.bestScore)

                curSearchTermIndex = 0
                missedTerm = 0

            elif curSearchTermIndex < len(searchTerm):

                if missedTerm < ((len(searchTerm) + 1) - (curSearchTermIndex + 1)):
                    missedTerm += 1
                else:
                    curSearchTermIndex += 1

            else:

                curSearchTermIndex = 0
                self.bestScore = 0

        retVal = self.bestScoreHistory[len(self.bestScoreHistory) - 1]

        self.bestScore = 0
        self.bestScoreHistory = []

        return retVal

appList = [
    "Google Play",
    "Google Play Music",
    "Google Calendar",
    "Google Maps",
    "Twitter",
    "YouTube",
    "Story Album",
    "Google App",
    "Flipboard",
    "Maps",
    "TripAdvisor",
    "Google Play Games",
    "Contacts",
    "Email",
    "Gmail",
    "Any.Do",
    "S Translator",
    "Chromecast",
    "Spring Ninja",
    "Google Play Services",
    "Programming Hub",
    "Optical Reader",
    "Google Play Newsstand",
    "Google Play Books",
    "Awesome South Africa",
    "Gallery",
    "Opera Mail",
    "Hangouts",
    "Calculator",
    "Group Play",
    "Google App Play",
    "Test Google",
    "Google app play store",
    "Google app store play"
]

se = SearchEngine()

startTime = datetime.now()
searchResult = se.search("Google Play", appList)

#display the search results in order of most relevance
for result in searchResult:
    print result[0]

print "Execution time : ", datetime.now() - startTime
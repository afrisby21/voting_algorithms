# Andrew Frisby

from openpyxl import load_workbook

# importing Counter from collections to help find modes of lists in a few of the functions
from collections import Counter


def generatePreferences(values):
    """
        generatePreferences will take an openpyxl worksheet with each agent's preference scores and return a dictionary with
        the ranked preferences for each agent. This dictionary will be used in the voting functions.

        Parameters:
            values: openpyxl worksheet - worksheet where the columns are the alternatives and the rows are the agents.
            Each cell contains that agent's preference score for the corrsponding alternative.
        
        Return:
            pref_dict: dictionary - dictionary where the keys are the agent's numbers (integers) and the values are the 
            ordered lists of the agents' preferred alternatives (also integers). Example: {1:[2,1,3,4], 2:[4,1,3,2], ...}
    """

    # creating empty dictionary which will be populated with each agent's alternative preference order and returned at the end
    pref_dict = {}

    # creating empty list which will be populated with tuples of the alternatives and their preference score for each agent
    # example: [(1, 0.296178), (2, 0.434362),...]
    # this will then be sorted by first the preference score, then the alternative integer to ensure the higher alternative
    # will be selected when preference scores are equivalent
    pref_list = []

    # looping through each row and cell of the worksheet to fill the pref_list and then sort it and assign it to pref_dict
    # for each agent
    for i, row in enumerate(values.rows):
        for idx, cell in enumerate(row):
            pref_list.append((idx+1, cell.value))
        
        # sorting the pref_list by the preference score first, then the alternative value
        sorted_pref = sorted(pref_list, reverse=True, key=lambda x: (x[1], x[0]))
        
        # creating and assigning the values in the pref_dict that contain the ordered alternatives for each agent
        pref_dict[i+1] = [tup[0] for tup in sorted_pref]
        
        # resetting pref_list for next agent
        pref_list = []

    return pref_dict

# the following set of functions are the tie breaker functions and other helper functions that are used throughout 
# the voting functions

def tieBreakMax(alternatives):
    """
        tieBreakMax will break a tie between a list of multiple alternatives by selecting the largest alternative integer.
        Example: a list of the following alternatives: [2,4,1], will return 4 because 4>2>1

        Parameters:
            alternatives: list - list of the alternatives that are tied
        
        Return:
            max value of alternatives: int 
    """

    return max(alternatives)

def tieBreakMin(alternatives):
    """
        tieBreakMin will break a tie between a list of multiple alternatives by selecting the smallest alternative integer.
        Example: a list of the following alternatives: [2,4,1], will return 1 because 4>2>1

        Parameters:
            alternatives: list - list of the alternatives that are tied
        
        Return:
            min value of alternatives: int 
    """

    return min(alternatives)

def tieBreakAgent(alternatives, agent, pref_dict):
    """
        tieBreakAgent will break a tie between a list of multiple alternatives by selecting the highest ranked alternative 
        of the tie breaking agent that is in the list.
        Example: a list of the following alternatives: [2,4,1], will return 1 because the tie breaking agent has the
        following preferences: [3,1,4,2,5] and 1 is the highest ranked preference of the tied alternatives

        Parameters:
            alternatives: list - list of the alternatives that are tied
            
            agent: int - the tie breaking agent
            
            pref_dict: the preference dictionary that has the agents as keys and their ordered alternatives as values. 
            Output of generatePreferences function
        
        Return:
            highest ranked preference of tie breaking agent in alternatives: int 
    """

    # grabs the index of each tied alternative in the ranked preferences of the tie breaking agent, then finds the
    # alternative with the lowest index (highest ranked), and returns that alternative using its index
    return pref_dict[agent][min([pref_dict[agent].index(x) for x in alternatives])]


def tie_breaker(max_list, tieBreak, preferences):
    """
        tie_breaker will return the winning alternative whether a tie breaker is necessary or not. Used in all the voting functions

        Parameters:
            max_list: list - list of the alternative(s) that the voting rules determined to be winners
            
            tieBreak: str or int - the tie break type to use if neccessary. 'min' calls tieBreakMin, 'max' calls tieBreakMax,
            int of tie breaking agent calls tieBreakAgent
            
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function
        
        Return:
            The winning alternative: int
    """
    
    # Error handling for incompatible tieBreak values
    if isinstance(tieBreak, int) and tieBreak not in preferences.keys():
        print('Tiebreaking agent number out of bounds.')
        return False

    elif isinstance(tieBreak, str) and tieBreak.lower() != 'max' and tieBreak.lower() != 'min':
        print('tieBreak string not recognized.')
        return False
    
    else:
        # tieBreakAgent
        if isinstance(tieBreak, int):
            return tieBreakAgent(max_list, tieBreak, preferences)
        
        # tieBreakMax
        elif tieBreak.lower() == 'max':
            return tieBreakMax(max_list)
        
        # tieBreakMin, could be just an else statement, but writing it as elif statement for clarity/readability
        elif tieBreak.lower() == 'min':
            return tieBreakMin(max_list)
        
        # although this else statement is not necessary due to above error handling, including it for clarity/readability/consistency
        else:
            print('tieBreak error.')
            return False
        

def flatten(lst):
    """
        flatten will 'flatten' a list of lists into a single list

        Parameters:
            lst: list - list of lists that will be flattened into single list
        
        Return:
            flattened list: list 
    """

    return [n for sub in lst for n in sub]

def counting(pref_list):
    """
        counting will count the number of times each element appears in a list and return a list of the elements that
        appear most often (the mode(s))

        Parameters:
            pref_list: list - list of elements to be counted
        
        Return:
            max_list: list - list of the mode(s) of pref_list
    """

    # using Counter() and most_common() from collections library to find mode of list, will be a tuple e.g., (alternative, count)
    counts = Counter(pref_list).most_common()

    # find max of counts which will be the value of the mode
    max_val = max(counts, key = lambda x: x[1])[1]

    # add alternative to max_list if it is a mode of pref_list
    max_list = [alt[0] for alt in counts if alt[1] == max_val]

    return max_list


# the rest of the functions are the voting rules

def dictatorship(preferenceProfile, agent):
    """
        dictatorship will return the highest ranked alternative of the dictator

        Parameters:
            preferenceProfile: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function
            
            agent: int - the agent that will be dictator
        
        Return:
            The winning alternative: int
    """

    if agent not in preferenceProfile.keys():
        return 'No corresponding agent with that number.'
    else:
        return preferenceProfile[agent][0]


def scoringRule(preferences, scoreVector, tieBreak='max'):
    """
        scoringRule will return the alternative that has the highest score based on the 
        scoring values for each rank in scoreVector

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            scoreVector: list - list of scores to assign to each rank. The top rank for each agent
            receives the largest score in scorevector, the second choice receives the second largest, and so on

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    # this works with preferences[1], but its not very algorithmic, might be able to use .get()? 
    if len(preferences[1]) != len(scoreVector):
        print('Incorrect input')
        return False

    # sort the scoreVector in descending order
    scoreVector = sorted(scoreVector, reverse=True)

    # create dict with each alternative as keys and total score as the values
    sum_dict = {k:0 for k in preferences[1]}
    
    # loop through each set of agent's alternative rankings and add corresponding score vector to the sum_dict
    # don't want to use flatten() here because I need the index in the sublists of preferences.values() to reset with each agent
    for val in preferences.values():

        for idx, alt in enumerate(val):
            sum_dict[alt] += scoreVector[idx]

    # generate list of alternative(s) that have the largest final score
    max_list = [key for key, value in sum_dict.items() if value == max(sum_dict.values())]
    
    # call and return tie_breaker() function to determine winning alternative
    return tie_breaker(max_list, tieBreak, preferences)

def plurality(preferences, tieBreak='max'):
    """
        plurality will return the alternative that appears the most times in the first position of the agents' prefence orderings

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    alt_len = len(preferences[1])

    # create list of the top ranked alternatives for each agent
    top_ranks = flatten(list(preferences.values()))[::alt_len]

    # use the counting() function to determine the alternative(s) that appears the most in top_ranks
    max_list = counting(top_ranks)

    # call and return tie_breaker() function to determine winning alternative
    return tie_breaker(max_list, tieBreak, preferences)
    
def veto(preferences, tieBreak='max'):
    """
        veto assigns 0 points to the last ranked alternative in each agents' preference orderings, and 1 point to the rest. 
        The function will then calculate the alternative with the most points and return it

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    alt_len = len(preferences[1])
    flat_prefs = flatten(list(preferences.values()))

    # create a list of each agents' ranked alternatives except the alternative in the last position
    # these alternatives are the 'vote winners'
    vote_winners = [n for idx, n in enumerate(flat_prefs) if (idx+1) % alt_len]

    # from here, it is similar to the plurality function because each alternative receives 1 point for each appearence, 
    # call counting() function on the vote_winners to determine the alternative(s) with the most points/appearances 
    max_list = counting(vote_winners)

    # call and return tie_breaker() function to determine winning alternative
    return tie_breaker(max_list, tieBreak, preferences)


def borda(preferences, tieBreak='max'):
    """
        borda assigns a score of 0 to the least preferred alternative, a score of 1 to the second least-preferred alternative,
        and a score of the length of an agent's preference list minus 1 to the top alternative. 
        The function will then calculate the alternative with the highest score and return it

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    alt_len = len(preferences[1])

    # create dict with each alternative as keys and total score as the values
    sum_dict = {k:0 for k in preferences[1]}

    flat_prefs = flatten(preferences.values())

    # create a list of each agents' ranked alternatives except the alternative in the last position
    # these alternatives are the 'vote winners'
    vote_winners = [n for idx, n in enumerate(flat_prefs) if (idx+1) % alt_len]

    # this counter is also the score value that will be added to each alternative's total score
    counter = alt_len - 1

    # looping through each alternative in vote_winners and adding their score to the corresponding value in sum_dict
    # resets the counter/score value after the loop completes totaling an agent's preferences (not including the last ranked
    # alternative becuase it is not in vote_winners)
    for alt in vote_winners:
        if counter < 1:
            counter = alt_len - 1 
        sum_dict[alt] += counter
        counter -= 1
    
    # generate list of alternative(s) that have the largest final score
    max_list = [key for key, value in sum_dict.items() if value == max(sum_dict.values())]

    # call and return tie_breaker() function to determine winning alternative
    return tie_breaker(max_list, tieBreak, preferences)
    
def harmonic(preferences, tieBreak='max'):
    """
        borda assigns a score of 1/m (m = length of an agent's preference ranking) to the least preferred alternative, 
        a score of 1/(m-1) to the second least-preferred alternative, and a score of 1 to the top ranked alternative. 
        The function will then calculate the alternative with the highest score and return it

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    alt_len = len(preferences[1])

    # create dict with each alternative as keys and total score as the values
    sum_dict = {k:0 for k in preferences[1]}

    # counter will also act as the denomenator of the value to be added to an alternative's score
    counter = 1

    # loop through each agent's alternatives and add their corresponding score to the alternative's total
    # reset counter after completing a loop through all an agent's preferences
    for alt in flatten(preferences.values()):
        if counter > alt_len:
            counter = 1 
        sum_dict[alt] += (1 / counter)
        counter += 1
    
    # generate list of alternative(s) that have the largest final score
    max_list = [key for key, value in sum_dict.items() if value == max(sum_dict.values())]

    # call and return tie_breaker() function to determine winning alternative
    return tie_breaker(max_list, tieBreak, preferences)

def STV(preferences, tieBreak='max'):
    """
        STV works in rounds. In each round, the alternatives that appear least frequently in the first position of agents' rankings
        are removed, and the process is repeated. When the final set of alternatives is removed, then the last set is the set 
        of possible winners. The function will then return the winning alternative

        Parameters:
            preferences: dictionary - the preference dictionary that has the agents as keys and their ordered alternatives 
            as values. Output of generatePreferences function

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """
    
    # purpose of function is to loop through each alternative, count how many times it appears in top-ranked list,
    # then remove the lowest occuring alternatives, then repeat process

    alt_len = len(preferences[1])
    flat_prefs = flatten(preferences.values())

    # top ranked alternatives
    top_ranks = flat_prefs[::alt_len]

    # temporary list that will hold the remaining alternatives after each round, initially holds all preferences
    temp_list = flat_prefs

    # dictionary that will contain the alternatives that appear in the top ranked position as keys and the count of 
    # how many times they appear there as the values
    top_count_dict = {}

    # while loop that loops through each alternative and checks how many times it appears in the top ranked position
    # breaks when all alternatives are removed, saves the final remaining alternatives in final_list
    while True:
        for alt in set(temp_list):
            top_count_dict[alt] = top_ranks.count(alt)
        
        # generate list with the alternatives, to be removed, that appear in the top ranked position the least amount of times
        min_list = [key for key, value in top_count_dict.items() if value == min(top_count_dict.values())]

        # reset top_count_dict for next iteration
        top_count_dict = {}

        # save list of remaining alternatives before removal
        final_list = temp_list

        # generate new temp_list with the alternatives in min_list removed
        temp_list = [i for i in temp_list if i not in min_list]

        # generate new alt_len 
        alt_len = len(set(temp_list))

        # check if list is empty, and if so we break the loop and final_list will be the list of the winning alternative(s)
        if alt_len == 0:
            break
        # generate new list of top ranked alternatives from new temp_list
        top_ranks = temp_list[::alt_len]

    # once loop is finished, call and return tie_breaker
    return tie_breaker(final_list, tieBreak, preferences)

def rangeVoting(values, tieBreak='max'):
    """
        rangeVoting will take an openpyxl worksheet with each agent's preference scores and return the alternative with the largest sum
        of preference scores

        Parameters:
            values: openpyxl worksheet - worksheet where the columns are the alternatives and the rows are the agents.
            Each cell contains that agent's preference score for the corrsponding alternative

            tieBreak: str or int, default='max' - the tie break type to use if neccessary. 
            'min' calls tieBreakMin, 'max' calls tieBreakMax, int of tie breaking agent calls tieBreakAgent
        
        Return:
            The winning alternative: int
    """

    # initiate column sum and empty dictionary. sum_dict will hold alternatives as keys and their preference score sums
    # as the values
    col_sum = 0
    sum_dict = {}

    # loop through each column and sum each cell, add final sums for each alternative to sum_dict
    for i, col in enumerate(values.columns):
        for cell in col:
            col_sum += cell.value
        sum_dict[i+1] = col_sum
        col_sum = 0

    # find alternatives with the maximum sums and add them to list
    max_list = [key for key, value in sum_dict.items() if value == max(sum_dict.values())]

    # call generatePreferences() to input into tie_breaker() function
    preferences = generatePreferences(values)
    
    # call and return winning alternative
    return tie_breaker(max_list, tieBreak, preferences)


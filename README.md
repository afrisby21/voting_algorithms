# voting_algorithms
Voting algorithms that output a winning candidate/alternative. Data must be like image below where the rows are the voters/agents and the columns are the different alternatives/candidates. The numbers represent their preference scores.

<img width="340" alt="voting input data" src="https://user-images.githubusercontent.com/37544097/172617217-97eca51c-8f0b-4da9-8709-0093ad0dbe37.PNG">

Remove agent/alternative labels before inputting.

### Voting algorithms:

#### Dictatorship:
An agent is selected, and the winner is the alternative that this agent ranks first. For example, if the preference ordering of the selected agent is a>b>c>d, then the winner is alternative a.

#### Plurality:
The winner is the alternative that appears the most times in the first position of the agents' preference orderings. In the case of a tie, use a tie-breaking rule to select a single winner.

#### Veto:
Every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings, and 1 point to every other alternative. The winner is the alternative with the most number of points. In the case of a tie, use a tie-breaking rule to select a single winner.

#### Borda:
Every agent assigns a score of 0 to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of  to the second least-preferred alternative, ... , and a score of m - 1 to their favourite alternative. In other words, the alternative ranked at position j receives a score of m - j. The winner is the alternative with the highest score. In the case of a tie, use a tie-breaking rule to select a single winner.

#### Harmonic:
Every agent assigns a score of 1/m to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of 1/(m-1) to the second least-preferred alternative, ... , and a score of 1 to their favourite alternative. In other words, the alternative ranked at position j receives a score of 1/j. The winner is the alternative with the highest score. In the case of a tie, use a tie-breaking rule to select a single winner.

#### Single Transferable Vote (STV):
The voting rule works in rounds. In each round, the alternatives that appear the least frequently in the first position of agents' rankings are removed, and the process is repeated. When the final set of alternatives is removed (one or possibly more), then this last set is the set of possible winners. If there are more than one, a tie-breaking rule is used to select a single winner.

 

### Tie-Breaking Rules:

Here, I assume that the alternatives are represented by integers.


max: Among the possible winning alternatives, select the one with the highest number.

min: Among the possible winning alternatives, select the one with the lowest number.

agent : Among the possible winning alternatives, select the one that agent  ranks the highest in his/her preference ordering. 


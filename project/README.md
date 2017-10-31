# 10,000 Battles

## Abstract
In this project we will better understand one ubiquitous component of war: the battle. We propose to do so by retreiving and studying public data provided by Wikipedia and the UCDP Battle-Related Deaths Dataset about battles located around the world and which happened through the centuries of human history. By combining theses comprehensive battle records, we aim to observe how they evolved in terms of duration, localisation, geography, size, casualties through some exploratory analysis. Moreover, we will extract information on the belligerent forces and victory types (strategic, tactic, ...) for each battle. Our goal is then to find relations between such information and other variables. Leveraging on visualization techniques, we plan to gain knowledge on modern warfare from a data perspective and present these findings in an intuitive way. Our intent is to answer interesting questions such as: is there a repetitive pattern in the history of battles or wars in general? Are the conflicts becoming more deadly or less frequent?...

## Research questions
We intend to determine:
- how the duration of battles changed over time,
- how the battles are spread geographically over time,
- if there is a repetitive pattern in the history of battles,
- how the number of casualties (civilians vs. soldiers) is evolving,
- if we can relate battle-related variables to the victory type.


## Datasets

### Main
We will mainly rely on **en.wikipedia.org** to gather information and statistics about battles around the globe. We have estimated there are around 15,000 wikipedia pages dedicated to distinct battles and not including redirect pages. Random exploration showed that a vast majority of them contain a summary table including dates, locations, result, belligerents, commanders, units and losses. Therefore, we should have between 7000 to 12000 pages containing meaningful and extractable data. One key information provided by this dataset will be the victory type (tactical, strategic, decisive, pyrrhic,...), to which we propose to pay special attention. This may require some interesting natural language processing techniques to exploit, but would also be very interesting to analyse. In the same idea, some battle are specifically labeled as resulting in a territory expansion, another interesting characteristic.

### Enrichment
Preliminary random exploration revealed that the more recent is the battle, the more difficult it is to parse the wikipedia table. This is due to the increase of detailed information (mainly about casualities). For this recent part of history we can leverage on the **UCDP Battle-Related Deaths Dataset** to extract casualties data. This second dataset contains events at a much smaller granularity. It can be used to compare battles in the wider context of "violent Events".

For contextual information about the battles, the **UCDP/PRIO Armed Conflict Dataset** contains usefull information about belligerants and more interestingly about the incompatibility type between them.

To this point of our analysis, all datasets and computations we are considering can be handled by a simple laptop or server. It might however be convenient for us to perform the data extraction from the Wikipedia dataset on the cluster (or at least the page extraction), so we don't have to host large file on our machines.

## Roadmap toward Milestone 2
Oct. 31, 2017: First version of the readme

Nov. 10, 2017: First clear and practical representation of the available data.

Nov. 24, 2017: Exploratory analysis of the data and description of interesting results.

Nov. 28, 2017: Plan for the next steps.

Nov. 28, 2017 (23:59 CET): milestone 2 (20%): the project repo contains a notebook with data collection and descriptive analysis, properly commented, and the notebook ends with a more structured and informed plan for what comes next.

## Questions for TAa
What do you think about this project?

Is our range of topics too broad?

What would be a common pitfall we should avoid in this kind of exploration task?

Regarding the wikipedia dataset, because we will select the pages by their names, isn't it more convenient to retrieve them from the web (API or "human-readable") ?

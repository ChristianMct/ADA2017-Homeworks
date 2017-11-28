


# 10,000 Battles

###Link to milestone 2 notebook: [NBViewer](https://nbviewer.jupyter.org/github/ChristianMct/ADA2017-Homeworks/blob/master/project/milestone_2.ipynb)

## Abstract
In this project we will better understand one ubiquitous component of war: the battle. We propose to do so by retreiving and studying public data provided by Wikipedia about battles located around the world and which happened through the centuries of human history. By combining theses comprehensive battle records, we aim to observe how they evolved in terms of duration, localisation, geography, size, casualties through some exploratory analysis. Moreover, we will extract information on the belligerent forces and victory types (strategic, tactic, ...) for each battle. Our goal is then to find relations between such information and other variables. Leveraging on visualization techniques, we plan to gain knowledge on modern warfare from a data perspective and present these findings in an intuitive way. Our intent is to answer interesting questions such as: is there a repetitive pattern in the history of battles or wars in general? Are the conflicts becoming more deadly or less frequent?...

## Research questions
We intend to determine:
- how the duration of battles changed over time,
- how the battles are spread geographically over time,
- if there is a repetitive pattern in the history of battles,
- how the number of casualties is evolving,
- if we can relate battle-related variables to the victory type.


## Datasets

### Main
#### Milestone 1
We will mainly rely on **en.wikipedia.org** to gather information and statistics about battles around the globe. We have estimated there are around 15,000 wikipedia pages dedicated to distinct battles and not including redirect pages. Random exploration showed that a vast majority of them contain a summary table including dates, locations, result, belligerents, commanders, units and losses. Therefore, we should have between 7000 to 12000 pages containing meaningful and extractable data. One key information provided by this dataset will be the victory type (tactical, strategic, decisive, pyrrhic,...), to which we propose to pay special attention. This may require some interesting natural language processing techniques to exploit, but would also be very interesting to analyse. In the same idea, some battle are specifically labeled as resulting in a territory expansion, another interesting characteristic.
#### Milestone 2
**We have observed that we were able to extract more than 8,000 wikipedia pages about distinct battles. During the retrieving and parsing of the data, we have observed that around 70% of the data were parseable. We have managed to extract and parse the features that we consider interesting for our project, namely the battle's title, date, geographical coordinates, combatants, strength (number of fighters) and casualties.**

### Enrichment
#### Milestone 1
Preliminary random exploration revealed that the more recent is the battle, the more difficult it is to parse the wikipedia table. This is due to the increase of detailed information (mainly about casualities). For this recent part of history we can leverage on the UCDP Battle-Related Deaths Dataset to extract casualties data. This second dataset contains events at a much smaller granularity. It can be used to compare battles in the wider context of "violent Events".
#### Milestone 2
**We have observed that we were able to correctly and efficiently parse about 70% of the data in wikipedia. Even though this part took us more time than expected, we achieved satisfying results and decided to use these information to continue our project. In fact, we consider that we have enough information to compute interesting and meaningful results in order to answer our research questions. Thus, we do not need the UCDP Battle-Related Deaths Dataset.**

To this point of our analysis, all datasets and computations we are considering can be handled by a simple laptop or server. It might however be convenient for us to perform the data extraction from the Wikipedia dataset on the cluster (or at least the page extraction), so we don't have to host large file on our machines.
**We used the cluster and spark jobs to extract battle information from the wikipedia dump. The other operations, such as each battle feature extraction and the parsing of the data can be done locally on a laptop.**

## Roadmap for Milestone 2
Oct. 31, 2017: First version of the readme

Nov. 10, 2017: First clear and practical representation of the available data.

Nov. 24, 2017: Exploratory analysis of the data and description of interesting results.

Nov. 28, 2017: Plan for the next steps.

Nov. 28, 2017 (23:59 CET): milestone 2 (20%): the project repo contains a notebook with data collection and descriptive analysis, properly commented, and the notebook ends with a more structured and informed plan for what comes next.

## Roadmap towards Milestone 3
**Dec. 7, 2017: Exploratory Analysis: after the descriptive analysis of the dataset we constructed from available data, we will do a proper and complete exploratory analysis of the data. This one will be done in multiple steps:**
**- We will create a list of hypothesis, summarizing the correlations and other relations that we will investigate and that we need to answer our resarch questions**
**- We will do the exploratory analysis. In which we will focus on our research questions while still not forgetting to check for other relations that can be interesting.**
**- We will study some related work such as https://ourworldindata.org/war-and-peace/ and https://www.youtube.com/watch?v=DwKPFT-RioU.**
**- We will summarize our foundings and refine the next steps.**
**- We will start to write our report/data story about milestone 2 and beginning of milestone 3.**

**Dec. 12, 2017: Final Results: Based on our exploratory analysis, we will refine our data story by choosing the more meaninful results and decide on how we want to present them.**
**- We will also continue to write our report/data story.**

**Dec. 18, 2017: First complete version of the project**
**- The last day will be devoted to the finalisation of the report/data story.**

**Dec. 19, 2017 (23:59 CET): report (50%): a 4-page PDF document or a data story in a platform of your choice (e.g., a blog post, or directly in GitHub), plus the final notebook (continuation of milestone 2).**

## Questions for TAa
**- For the data that we are studying which contain geographical and temporal dimension, we can directly thing of presenting our results on a map or on a timeline or a mix of the two. Do you have other ideas or related work that we should study to find the best representation ?**

**- According to your experience, when should we start the real and final data/results interpretation ? Compared to the data exploratory, should it be longer or shorter ?**

**- The visualization of the results should be completely finished for the report ? Or the report must contain the result when the vizualisation and presentation has to be ready for the poster session ?**
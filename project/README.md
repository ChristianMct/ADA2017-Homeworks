


# 10,000 Battles

###Link to milestone 2 notebook: [NBViewer](https://nbviewer.jupyter.org/github/ChristianMct/ADA2017-Homeworks/blob/master/project/milestone_2.ipynb)

## Abstract
For centuries, battles have been and still are the most direct tool used by established powers to project or extend their For centuries, battles have been and still are the most direct action taken by established powers to project or extend their influence. By collecting, processing and analyzing data from the open source, collaborative Wikipedia platform, we are able to better understand how battles were fought throughout the last millennium. In this document, we report our findings from an analysis made over more than 7000 battles. We expose trends in duration and casualties over the years. Additionally, we show that the latter is the most important battle’s feature in determining the short-term winner which is not necessarily the long-term one.

## Research questions
We provided the following analyis:
- how the average duration of battles changed over time,
- how the battles are spread geographically over time,
- how the average number of casualties is evolving over time,
- relation between battle-related variables its result,
- can we find actors that are historically more engaged in battles.


## Milestones

#### Milestone 1: Initial dataset exploration and information retrieval:
We relied on **en.wikipedia.org** to gather information and statistics about battles around the globe. Initially we estimated that there were around 15,000 wikipedia pages dedicated to distinct battles, not including redirect pages. Random exploration showed that a vast majority of them contained a summary table including dates, locations, result, belligerents, commanders, units and losses. Thus we estimated that we would be able to work on a dataset of 7000 to 10000 battles containing meaningful and extractable data. From these battles, our aim was to answer the above research questions.

#### Milestone 2: Data extraction and parsing:
We were able to extract more than 7,000 wikipedia pages about distinct battles. We used the cluster and spark job to extract battle-related pages from the English Wikipedia dump, and local processing jobs for the rest of the processing pipeline. We recovered the features that we consider interesting for our project, namely the battle's title, date, geographical coordinates, combatants, strength (number of fighters) and casualties. More challengingly, we extracted and normalized the battles’ result according to well established outcome types, and attributed these to one of the combatant. Generally, the more recent was the battle, the more difficult it was to parse the corresponding wikipedia infobox. Indeed with the rise of digitalization comes the tsunami of detailed information (mainly about casualities in our case). Dealing with "information from the jungle" to make it easy to use and analyze has been a very large part of our project, in fact it took us more time than expected. Anyone can be a wikipedia author which results in heterogenous information. Some parsers exist for certain features like date ranges but not for all features and none of them included all corner cases. After cleaning our gathered information making it "supermaket ready" as would say Prof. West, we obtained a satisfying dataset of 7846 battles on which we could perform some analysis. 

#### Milestone 3: Exploratory Analysis and results:
During this milestone, we initially planned to have two members working on the research questions and one supporting member improving the dataset according to their needs. Unfortunately, we had to rework a lot on our processing pipeline, due to the heterogeneous nature of our base dataset (full text of the pages) and the diversity of our features (dates, coordinates, lists of actors, types of result, description of casualties). Thus, we present more extensively our data processing pipeline in our report, as it was a significant part of the project. We also had to acquire some understanding about military tactics, strategies and the basics of war studies in order to provide context for our analysis. We decided to provide our results as a report, first and foremost because all of us are academics, but also for the reason that we already wrote a lot of code for data processing.



## Work Distribution
#### Christian Mouchet: 
Proposed the initial project idea, acted as coordinator. Took implemented the first pipeline step as a cluster job. Extracted battle results and combatants features and attributed the former to the most likely belligerent. Supported the analysis by continuously enhancing the pipeline. Worked on writing the notebook and the report.
#### David Froelicher:
Worked on extracting the casualties and strengths features. Provided analysis and visualization notably by exploring links between victory types and features, and by attempting to build a predictive model for the battle outcome given its other features. Worked on writing the notebook and the report.
#### Marguerite Delcourt:
Extracted the dates and coordinates features. Performed analysis and plots by finding correlations between dates/durations, dates/geolocalisation, casualties/time, casualties/duration and by improving the predictive model. Worked on writing the notebook, the report and the readme file.
#### Final presentation: 
Christian Mouchet will perform the oral presentation and all will collaboratively work on the poster.

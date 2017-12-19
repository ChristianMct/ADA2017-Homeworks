


# 10,000 Battles

###Link to milestone 2 notebook: [NBViewer](https://nbviewer.jupyter.org/github/ChristianMct/ADA2017-Homeworks/blob/master/project/milestone_2.ipynb)

## Abstract
For centuries, battles have been and still are the most direct tool used by established powers to project or extend their influence. By collecting, processing and analyzing data from the open source and collaborative Wikipedia platform, we are able to better understand how battles were fought throughout the last millennium. In this document, we report our findings from an analysis made over more than 7000 battles. We expose trends in duration and casualties over the years. Additionally, we show that the latter is most important in determining the short-term winner which is not necessarily the long-term one.

## Research questions
We intend to determine:
- how the duration of battles changed over time,
- how the battles are spread geographically over time,
- how the number of casualties is evolving over time,
- if we can relate battle-related variables to the battle result,
- if we can relate the victory type (tactical, strategic, decisive, pyrrhic,...) to opponents's features,
- if we can predict the result given battle and opponents features,
- can we find countries that are historically more battle-active.


## Datasets and Analysis

#### Milestone 1: Initial dataset exploration and information retrieval:
We relied on **en.wikipedia.org** to gather information and statistics about battles around the globe. Initially we estimated that there were around 15,000 wikipedia pages dedicated to distinct battles, not including redirect pages. Random exploration showed that a vast majority of them contained a summary table including dates, locations, result, belligerents, commanders, units and losses. Thus we estimated that we would be able to work on a dataset of 7000 to 10000 battles containing meaningful and extractable data. From these battles, our aim was to answer the above research questions.

#### Milestone 2: Data extraction and parsing:
For milestone 2, we were able to extract more than 8,000 wikipedia pages about distinct battles. We used the cluster and spark job to extract battle information from the wikipedia dump. The relevant information is stored in infoboxes which easily fits in a file on a simple laptop. During the retrieving and parsing of the data, we managed to correctly and efficiently parse around 70% of the data in wikipedia. We recovered the features that we consider interesting for our project, namely the battle's title, date, geographical coordinates, combatants, strength (number of fighters) and casualties. Generally, the more recent was the battle, the more difficult it was to parse the corresponding wikipedia infobox. Indeed with the rise of digitalization comes the tsunami of detailed information (mainly about casualities in our case). Dealing with "infomation from the jungle" to make it easy to use and analyze has been a very large part of our project, in fact it took us more time than expected. Anyone can be a wikipedia author which results in unhomogeneous information. Some parsers exist for certain features like date ranges but not for all features and none of them included all corner cases. After cleaning our gathered infomation making it "supermaket ready" as would say Prof. West, we obtained a satisfying dataset of 7846 battles on which we could perform some analysis. 

#### Milestone 3: Exploratory Analysis and results:
As mentioned above, all datasets and computations could be handled by a simple laptop or server. Thus we did not need the cluster for our exploratory analysis. We used pandas notebooks on jupyter to find correlations between battle features, battle results and battle result types. We used some natural language processing techniques in order to link the result information to the victorious combatant. For instance, a combatant could be named 'France' while the result could be 'French victory'. We also used a machine learning technique to predict the victorious combatant from features such as the number of casualties. From our correlations and findings we made some statistical plots and heatmaps which vary in time and space. You can find interesting code, results and plots in the notebook and resulting analysis with answers to the above research questions in the article.



## Work Distribution
#### Christian Mouchet: 
Found the dataset, retrieved the data from wikipedia and created the file containing all the infoboxes. Parsed results and combatants. Found correlations between them and made some plots. Went through the parsing of the whole dataset again to create a cleaner database to analysze. Worked on writing the notebook and the report. 
#### David Froelicher:
Worked on parsing casualties and strengths. Found correlations between them and created visuals. Exploration analysis on links between victory types and features, tried to build a classifier to give a result prediction. Worked on writing the notebook and the report.
#### Marguerite Delcourt:
Parsed dates and coordinates. Performed analysis and plots by finding correlations between dates/durations, dates/geolocalisation, casualties/time and casualties/duration. Worked on writing the notebook, the report and the readme file.
#### Final: 
Christian Mouchet will do the oral presentation and we will all collaboratively work on the poster.
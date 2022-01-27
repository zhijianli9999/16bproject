# Project Proposal

## Abstract

## Relationship to existing projects

The idea of evaluating water shortage risk is certainly not new. In this section, I detail the existing work relevant to my proposed project.

In 2021, the California Department of Water Resources (DWR) released its [Drought and Water Shortage Risk Explorer](https://tableau.cnra.ca.gov/t/DWR_IntegratedDataAnalysisBranch/views/SmallWaterSystemRisk-March2021/Dashboard?%3Aembed=y&%3AisGuestRedirectFromVizportal=y), containing an interactive web app mapping out their risk assessment score of wells in the state. The main difference between this effort and my proposed project is that the DWR's risk assessment system is not a statistical model. Instead, it is a weighted average of risk "scores" obtained through "an extensive stakeholder participatory process", with the weights similarly determined via discussions. This scoring system is detailed in [Part 2 Appendix 1](https://water.ca.gov/-/media/DWR-Website/Web-Pages/Programs/Water-Use-And-Efficiency/Urban-Water-Use-Efficiency/CDAG/Part-2-Appendix-1-Scoring-Method-Final.pdf) of DWR's [Final Report](https://tableau.cnra.ca.gov/t/DWR_IntegratedDataAnalysisBranch/views/SmallWaterSystemRisk-March2021/methods?%3AshowAppBanner=false&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3AisGuestRedirectFromVizportal=y&%3Aembed=y) regarding their efforts to satisfy Assembly Bill 1668, the legislation that prompted this project. Although the goals and methodology of the DWR's project differ drastically from mine, it incorporates an extensive list of risk factors which can help augment the input data for my model.

A second resource that I came across is Hussein et al. (2020)[^1], which

[^1]: Hussein, Eslam A., Christopher Thron, Mehrdad Ghaziasgar, Antoine Bagula, and Mattia Vaccari. 2020. "Groundwater Prediction Using Machine-Learning Tools" Algorithms 13, no. 11: 300. https://doi.org/10.3390/a13110300
## Planned Deliverables

The most ambitious version of my project would consist of three main components. These are, starting from the user end, an interactive geographic visualization to explore the risk of water shortages, a machine learning model to predict water shortages, and a pipeline to gather up-to-date data on the risk factors. The core component would be the machine learning model, so a partial success would be to build a predictive model with inputs from multiple datasets. The output of the predictive model would be, for each well in the state of California, an estimated probability of water shortage, say, for the next six months. The visualization would display the risk calculations in an interactive map that displays the probability of failure along with information about the risk factors. Potentially, I would like to automatically update the model with periodically collected data, such as [seasonal groundwater level data](https://data.ca.gov/dataset/groundwater-level-seasonal-change-points) measured by the California Department of Water Resources, and other datasets from [data.ca.gov](data.ca.gov). In terms of tools, I plan to build the predictive model in a Jupyter notebook, and do the visualization in a web app.

## Resources Required

The data   [Household Water Supply Shortage Reporting System](https://data.ca.gov/dataset/household-water-supply-shortage-reporting-system-data)

What resources do you need in order to complete your project? Data? Computing power? An account with a specific service?

Please pay special attention to the question of data. If your project idea involves data, include at least one link to a data set you can use. It’s also acceptable to link to a website from which you intend to scrape the data you will use (although note that high-quality scraping is a lot of work).

If you can’t find data for your original idea, that’s ok! Think of something related to your group’s interests for which you can find data.

Most projects should involve data in some way, but certain projects may not require data. Ask me if you’re not sure.

## Tools and Skills Required
What skills will you need? Machine learning, database management, complex visualization, something else? Do a bit of research into which Python packages accomplish the tasks you are going to need. Feel free to look ahead at what we’re going to do in the remainder of the course – you’re likely to find some of the packages you’ll need there!

What You Will Learn
What will you learn by completing this project? Feel free to mention particular techniques, software packages, version control, project management principles, any other learning goals you might have.

## Risks
What are two things that could potentially stop you from achieving the full deliverable above? Maybe it turns out that the signal you thought would be present in the data just doesn’t exist? Or maybe your idea requires more computational power than is available to you? What particular risks might be applicable for your project?

## Ethics
All projects we undertake involve decisions about whose interests matter; which problems are important; and which tradeoffs are considered acceptable. Take some time to reflect on the potential impacts of your product on its users and the broader world. If you can see potential biases or harms from your work, describe some of the ways in which you will work to mitigate them. Remember that even relatively simple ideas can have unexpected and impactful biases. Here’s a nice introductory video for thinking about these questions, and here’s one that goes into somewhat more detail. Here are some relevant examples: - A recipe recommendation app can privilege the cuisines of some locales over others. Will your user search recipes by ingredients? Peanut butter and tomato might seem an odd combination in the context of European cuisine, but is common in many traditional dishes of the African diaspora. A similar set of questions applies to recommendation systems related to style or beauty. - A sentiment analyzer must be trained on specific languages. What languages will be included? Will diverse dialects be included, or only the “standard” version of the target language? Who would be excluded by such a choice, and how will you communicate about your limitations?

A related question is: should this app exist? In a few sentences, discuss the following questions:

What groups of people have the potential to benefit from the existence of our product?
What groups of people have the potential to be harmed from the existence of our product?
Will the world become an overall better place because of the existence of our product? Describe at least 2 assumptions behind your answer. For example, if your project aims to make it easier to predict crime, your assumptions might include:
Criminal activity is predictable based on other features of a person or location.
The world is a better place when police are able to perform their roles more efficiently.

## Tentative Timeline
There will be checkpoints for the project at approximately two-week intervals. With this in mind, please describe what you expect to achieve after two, four, and six weeks. At each stage, you should have “something that works.” For example, maybe in two weeks you’ll ready to demonstrate the data acquisition pipeline, in four weeks you’ll be able to demonstrate some data analysis, and in six weeks you’ll have your full machine learning pipeline set up. Please keep in mind that you’ll be asked to present at each of these checkpoints. Showing “something that works” will usually be necessary for full credit. The “something that works” idea is related to the common concept of “minimum viable products” in software development, and is visually illustrated here:

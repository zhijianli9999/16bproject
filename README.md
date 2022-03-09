#### Questions for pre-submission
- What would be a good medium to present the results/predictions? I originally wanted to build a web app but now I think the only user interaction would be to explore the geographical visualizations, so maybe a blog post would suffice?
- What else should I include? More exploratory data analysis? Better ways to visualize the time trends?

#### To-do
- clean up visualizations (labels, titles, etc)
- add more comments to data processing code
- add more explanations and model results to report

## Project Dry Wells
The `code` folder contains:
- `visualize.ipynb`, which serves as the project report (the geographical visualizations are not included for now and are in the `output` folder).
- `clean.py`, which cleans the data in the `data` folder and outputs them to the `cleaned` folder.
- `predict.py`, which runs the prediction models.

The `data` folder contains the raw data files on wells, shortage reports, and station measurements downloaded from the internet.

The `cleaned` folder contains cleaned datasets for the model.

The `output` folder contains the visualizations in HTML files.

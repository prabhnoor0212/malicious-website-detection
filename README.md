# malicious-website-detection

IMPORTING>>>> In Progress (will be addidng more results and the web extension code as I get time :)

## OBJECTIVE

Build a system to classifiy a url as malicious or safe using machine learning.

## DATASET

![malicious-dataset](https://user-images.githubusercontent.com/43536129/46874523-f5bb4400-ce56-11e8-9e95-e37475d9dd0d.PNG)

* Initially the URLs alongwith Phishing tags were downloaded from: https://www.kaggle.com/simsek/openphishcom-phishing-urls-on-oct-2-2017#dataset.csv
* Many useful parameters (URL-based features, Domain-based features, Page-based features and Content-based features) were extracted using web scraping and some basic computations : [makeDataset.py](https://github.com/prabhnoor0212/malicious-website-detection/blob/master/makeDataset.py) (for the code), [dataset.csv](https://github.com/prabhnoor0212/malicious-website-detection/blob/master/dataset.csv) (for the basic dataset)
* Dataset after preparation and pre-processing: [final_cleaned_dataset.csv] (https://github.com/prabhnoor0212/malicious-website-detection/blob/master/final_cleaned_dataset.csv)

## FLOW
![untitled diagram](https://user-images.githubusercontent.com/43536129/46875273-ee953580-ce58-11e8-9875-e7d76b81b496.png)

## Pre-Processing

* Cleaning: Missing-values by imputation, domain-knowledge, Mean-Mode substitutions and other techniques
* Merging and Joining of datasets
* Standardization of numerical features
* Analysis: Graphs(1-D,2-D,3-D,n-D)
[iPython notebook](https://github.com/prabhnoor0212/malicious-website-detection/blob/master/Analysis_Working.ipynb) / [PDF](https://github.com/prabhnoor0212/malicious-website-detection/blob/master/Analysis_Working.pdf)

### Dimensionality reduction for visualisation using - TSNE (selected over PCA due to better plot)
![tsne](https://user-images.githubusercontent.com/43536129/46878984-729feb00-ce62-11e8-9b0b-3f5ea838b5f0.PNG)

## ML
### K-Nearest Neighbors
* Train data + Cross Val data -> 70%
* kd-tree algorithm for finding optimal-k (for better time performance)
* Accuracy on unseen test data: 94.86%
* Confusion Matrix (Without optimization):

![wogene](https://user-images.githubusercontent.com/43536129/46881008-e7295880-ce67-11e8-869c-0e939f6867a8.PNG)

### Observations
*Kd-tree time complexity

  -> When d (number of features) is small : O(log (n))
  
  -> When d is not small : O(2^d (log (n)))
  
* K-NN interpretibility decreases as dimensionality increases
* K-NN uses Minkowski Distance ( esp. Euclidean distance) which fails in higher dimensions
* #### Curse of Dimensionality [https://en.wikipedia.org/wiki/Curse_of_dimensionality]

  -> Hughes Phenomenon
  
  -> As d increases Overfitting increases (generally)
  
  -> Distance functions (Euclidean)
  
  
![dist formula](https://user-images.githubusercontent.com/43536129/46881478-4fc50500-ce69-11e8-8e0a-72f07bcbdb23.PNG)

### Genetic Algorithms and Bio-inspired algos
* This algorithm short-listed only 7 features (major reduction)
* Thus, simplifying time complexity for productionazing as well as reducing the dimensionality
* Accuracy: 96.89%
* [Code](https://github.com/philipkalinda/GeneticFS/blob/master/geneticfs/algorithm.py) & [Implementation](https://github.com/prabhnoor0212/malicious-website-detection/blob/master/Analysis_Working.ipynb)
* Confusion Matrix:


![withgen](https://user-images.githubusercontent.com/43536129/46882033-f1992180-ce6a-11e8-966e-31b3bb2eaeaf.PNG)

![como](https://user-images.githubusercontent.com/43536129/46885268-1db9a000-ce75-11e8-82de-272c435450fe.PNG)

## Bayes
coming soon..
Will be adding interesting results from other algorithms as soon as I find some time :) 




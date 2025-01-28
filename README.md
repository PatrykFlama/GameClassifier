# GameClassifier
Find fitting tags for your game, based on its description

## [Presentation with results](./presentations/results/main.pdf)

## [Project HackMD](https://hackmd.io/vwPnLpSrQzGLLLdzyfqvCw?view)

## Roadmap
* Create dataset
  * [x] Python program that downloads game descriptions and tags from Steam, then saves them in file or database
  * [x] Python program that creates dictionary of words with their frequency
* Create input encoders
  * [x] Bag of words
  * [x] TF-IDF
  * [x] Hashing vectorizer 
* Create output encoders
  * [x] Multi label binary vector
* Create evaluation functions
  * [x] Recall TP/(TP+FN)
  * [x] F1-score (2 * precision * recall) / (precision + recall)
  * [ ] Experiment with more evaluation functions
* Create models
  * [x] KNN
  * [x] Logistic regression
  * [x] Decision trees
  * [x] Random forest
  * [x] Naive Bayes
  * [x] Simple neural network
  * [x] Support Vector Machine
* [ ] Combine everything into one sandbox notebook
* [ ] Add cross validation to models

# Future work
* [ ] add some fullstack app to wrap entire result model
* [ ] play more with PCA decomposition and reverse-construct dictionary from it (dictionary of words perfectly describing games)


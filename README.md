# GameClassifier
Find fitting tags for your game, based on its description

## [Project HackMD](https://hackmd.io/vwPnLpSrQzGLLLdzyfqvCw?view)

## Roadmap
* [x] Create dataset
  * [x] Python program that downloads game descriptions and tags from Steam, then saves them in file or database
  * [x] Python program that creates dictionary of words with their frequency
* [ ] Create input preprocessors
  * [ ] Bag of words
  * [ ] TF-IDF
  * [ ] Neural network
* [ ] Create output preprocessors
  * [ ] Multi label binary vector
  * [ ] Neural network?
* [ ] Create evaluation functions
  * [ ] Recall TP/(TP+FN)
  * [ ] F1-score (2 * precision * recall) / (precision + recall)
* [ ] Create models
  * [ ] KNN
  * [ ] Logistic regression
  * [ ] Decision trees
  * [ ] Random forest
  * [ ] Naive Bayes
  * [ ] **something more advanced**
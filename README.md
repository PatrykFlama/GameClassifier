# GameClassifier
Find fitting tags for your game, based on its description

## [Project HackMD](https://hackmd.io/vwPnLpSrQzGLLLdzyfqvCw?view)

## Roadmap
* Create dataset
  * [x] Python program that downloads game descriptions and tags from Steam, then saves them in file or database
  * [x] Python program that creates dictionary of words with their frequency
* Create input encoders
  * [x] Bag of words
  * [x] TF-IDF
  * [x] Something more advanced
* Create output encoders
  * [x] Multi label binary vector
  * [ ] Something more advanced?
* Create evaluation functions
  * [x] Recall TP/(TP+FN)
  * [x] F1-score (2 * precision * recall) / (precision + recall)
* Create models
  * [x] KNN
  * [x] Logistic regression
  * [x] Decision trees
  * [ ] Random forest
  * [x] Naive Bayes
  * [ ] **something more advanced** (probably neural network)
* [ ] Combine everything into one sandbox notebook
* [ ] cross validation


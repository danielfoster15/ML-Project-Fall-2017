There are two python scripts here. MLProjectDataProcessing creates all 
the text files in the folder, three of which are used by MLProjectSVM.

MLProjectSVM can be run on the final files: 
shuffledreactionwords 
shuffledloveangrywords 
shuffledsadangrywords

by changing the filename in line 87. 
Running this will print accuracy, top 25 tfidf, and confusion matrices
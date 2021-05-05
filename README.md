poets_QA

## Evaluation
You can test the bot with these pipelines:

`rasa test nlu --config config_spacy.yml --cross-validation --runs 1 --folds 6`

`rasa test nlu --config config_bert.yml --cross-validation --runs 1 --folds 6`

Explanation:

**`--config`** :  Switch between the config files, that you currently want to test.

**`--cross-validation`** : To test your model more extensively, use cross-validation, which automatically creates multiple train/test splits.  (~80% train/~20% test split)

**`--runs`** : Change the number of runs.

**`--folds`** : Number of test in a run.


Here, we compare scores for intent classification, side by side.

|config| precision|accuracy|f1-score|
|:---:|:---:|:---:|:---:|
|config_bert.yml|0.833 |0.867|0.837|
|config_spacy.yml |0.801 |0.821|0.796|
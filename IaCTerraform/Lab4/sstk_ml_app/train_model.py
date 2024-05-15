import os
import json
import joblib
import warnings
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

# ignore warnings
warnings.filterwarnings('ignore')

# load the dataset
print('[INFO] Loading the dataset')
DATASOURCE = ('C:\\Users\\Samsung\\OneDrive\\Ícaro Augusto\\' +
              'Portfolio\\predictive_maintenance_case\\data\\1_raw')
DATA_SET = 'PM_train.txt'
data = pd.read_csv(os.path.join(DATASOURCE, DATA_SET), sep=' ', header=None)

# FUNCTION DEFINITIONS -----------------------------------------------------------------
def label_machine_failure(row: pd.Series, max_cycles_per_id: pd.Series) -> int:
    """
    create the failure class
    1 - the asset will fail in runtime + 30 cycles
    0 - the asset will not fail in runtime + 30 cycles

    Parameters
    ----------
    row : pd.Series
        dataframe row
    max_cycles_per_id : pd.Series
        maximum cycles per id dataset

    Returns
    -------
    int
        failure class
    """
    # business requirement
    CYCLE_THRESHOLD = 30

    # get the maximum cycle for that id
    max_cycle = max_cycles_per_id[row['id']]

    # if the present cycle + threshold surpass the history max, then the
    # asset failed
    if row['cycles'] + CYCLE_THRESHOLD > max_cycle:
        return 1
    
    return 0

def fit_evaluate_models(row: pd.Series, x_train: pd.DataFrame,
                        y_train: pd.DataFrame, x_test: pd.DataFrame, y_test: pd.DataFrame) -> pd.Series:
    """
    fit and evaluate the models

    Parameters
    ----------
    row : pd.Series
        row with the pipeline and hyperparameters
    x_train : pd.DataFrame
        training predictors
    y_train : pd.DataFrame
        training target
    x_test : pd.DataFrame
        test predictors
    y_test : pd.DataFrame
        test target

    Returns
    -------
    pd.Series
        results
    """
    N_ITER = 50

    # fit the model with the hyperparameters
    model = RandomizedSearchCV(
        estimator=row['pipeline'],
        param_distributions=row['hyperparameters'],
        n_iter=N_ITER,
        cv=cv,
        refit=True,
        scoring='matthews_corrcoef',
        n_jobs=-1, 
        random_state=42,
        verbose=3
    )

    # fit the model
    model.fit(x_train, y_train)

    # evaluate the model
    train_score = model.score(x_train, y_train)
    test_score = model.score(x_test, y_test)

    # return the results
    return pd.Series({
        'model': row['model_name'],
        'train_score': train_score,
        'test_score': test_score,
        'best_params': model.best_params_,
        'final_model': model.best_estimator_
    })

# PREPROCESSING ------------------------------------------------------------------------

print('[INFO] Preprocessing the dataset')

# drop null columns
null_cols = [26, 27]
data.drop(null_cols, axis=1, inplace=True)

# create real column names (based on the data dictionary)
real_cols = ['id', 'cycles', 'set1', 'set2', 'set3']
real_cols += [ "(Fan inlet temperature) (deg.R)",
"(LPC outlet temperature) (deg.R)",
"(HPC outlet temperature) (deg.R)",
"(LPT outlet temperature) (deg.R)",
"(Fan inlet Pressure) (psia)",
"(bypass-duct pressure) (psia)",
"(HPC outlet pressure) (psia)",
"(Physical fan speed) (rpm)",
"(Physical core speed) (rpm)",
"(Engine pressure ratio(P50/P2)",
"(HPC outlet Static pressure) (psia)",
"(Ratio of fuel flow to Ps30) (pps/psia)",
"(Corrected fan speed) (rpm)",
"(Corrected core speed) (rpm)",
"(Bypass Ratio) ",
"(Burner fuel-air ratio)",
"(Bleed Enthalpy)",
"(Required fan speed)",
"(Required fan conversion speed)",
"(High-pressure turbines Cool air flow)",
"(Low-pressure turbines Cool air flow)" ]

data.columns = real_cols

# drop low variance columns
VARIANCE_THRESHOLD = 0.001
stats = data.describe().T
stats['CV'] = abs(stats['std'] / stats['mean'])

# select columns with higher variance
low_variance_cols = stats.loc[stats['CV'] >= VARIANCE_THRESHOLD].index
data = data[low_variance_cols]

# drop the rows below 150 cycles
MIN_CYCLES = 150
data = data.loc[data['cycles'] > MIN_CYCLES,:]

# calculate the maximum lifetime - for each id
max_life = data.groupby(by=['id'])['cycles'].max()

# label the failure
target = 'failure(t+30)'
data[target] = data.apply(label_machine_failure,
                          max_cycles_per_id=max_life, axis=1)

# drop the id column
data.drop(columns=['id'], axis=1, inplace=True)

# use hypothesis test to select the best features
# for the sake of simplicity, let's select the 5 features more correlated with the
# classes of failure - this means selecting via an hypothesis test
h_tests = pd.DataFrame(columns=['tag', 'U', 'p'])

for tag in data.columns:
    if tag not in [target, 'cycles']:
        # split groups
        group0 = data.loc[data[target]==0, tag].values
        group1 = data.loc[data[target]==1, tag].values

        # calculate non-parametric mann-whitney's u
        U, p = mannwhitneyu(group0, group1)

        # append to the dataframe
        h_tests.loc[h_tests.shape[0], ['tag', 'U', 'p']] = tag, U, p

# sort by statistic U
h_tests.sort_values(by=['p'], ascending=True, inplace=True)
h_tests

# select the top 5 features
N = 5
selected_features = h_tests['tag'].values[:N]

# get predictors and target
y = data[[target]]
x = data.loc[:, selected_features]

# split train and test sets
print('[INFO] Splitting the dataset')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)

# MODELING ------------------------------------------------------------------------

print('[INFO] Modeling the dataset')
# create the pipeline
pipelines = [
    Pipeline([
        ('selector', SelectKBest(f_classif)),
        ('scaler', RobustScaler()),
        ('model', RandomForestClassifier())
    ]),
    Pipeline([
        ('selector', SelectKBest(f_classif)),
        ('scaler', RobustScaler()),
        ('model', GradientBoostingClassifier())
    ]),
    Pipeline([
        ('selector', SelectKBest(f_classif)),
        ('scaler', RobustScaler()),
        ('model', AdaBoostClassifier())
    ])    
]

# hyperparameters
param_distributions = [
    {
        'selector__k': [3, 4, 5],
        'model__n_estimators': np.random.randint(10, 1000, 500),
        'model__max_depth': [3, 4, 5]
    },
    {
        'selector__k': [3, 4, 5],
        'model__n_estimators': np.random.randint(10, 1000, 500),
        'model__max_depth': [3, 4, 5],
        'model__learning_rate': np.random.uniform(0.01, 0.1, 100)
    },
    {
        'selector__k': [3, 4, 5],
        'model__n_estimators': np.random.randint(10, 1000, 500),
        'model__learning_rate': np.random.uniform(0.01, 0.1, 100),
    }
]

# cross-validation
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# create the results dataframe
experiments = pd.DataFrame(pipelines, columns=['pipeline'])
experiments['hyperparameters'] = param_distributions
experiments['model_name'] = ['RandomForest', 'GradientBoosting', 'AdaBoost']

# apply the function
results = experiments.apply(
    fit_evaluate_models,
    x_train=x_train,
    y_train=y_train.values.ravel(),
    x_test=x_test,
    y_test=y_test.values.ravel(),
    axis=1
)

# order the results
results.sort_values(by=['test_score'], ascending=False, inplace=True)

# get the best model
best_model = results.iloc[0]['final_model']

# save the model
print('[INFO] Saving the model')
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
MODEL_NAME = 'predictive_maintenance_model.pkl'
MODEL_FILE = os.path.join(MODEL_PATH, MODEL_NAME)
joblib.dump(best_model, MODEL_FILE)

# save model metadata
print('[INFO] Saving the model metadata')
METADATA = {
    'features': {},
    'target': target
}
for feature in selected_features:
    METADATA['features'][feature] = {
        'max': round(data[feature].max(), 2),
        'min': round(data[feature].min(), 2)
    }
METADATA_FILE = os.path.join(MODEL_PATH, 'metadata.json')
with open(METADATA_FILE, 'w') as file:
    json.dump(METADATA, file, ensure_ascii=False)
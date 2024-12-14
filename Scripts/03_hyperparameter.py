import os               # import library untuk operasi sistem seperti path folder atau file
import pandas as pd     # import library untuk pengolahan dataframe 
import joblib           # import library untuk simpan hyperparameter ke format joblib 

from sklearn.model_selection import train_test_split, GridSearchCV, KFold          # library untuk setting hyperparameter model 
from sklearn.ensemble import RandomForestClassifier                                # library untuk membuat model random forest 
from sklearn.metrics import accuracy_score, classification_report, roc_curve, auc  # library untuk mengukur akurasi model 

# buat class oop dengan nama Random Forest Tuner 
class RandomForestTuner:
    def __init__(self, data_dir, feature_columns, target_columns):
        self.data_dir = data_dir
        self.feature_columns = feature_columns
        self.target_columns = target_columns

        self.train_data = None
        self.test_data = None
        self.valid_data = None
    
    # Buat fungsi untuk load datasheet train, test dan validation 
    def load_data(self):
        # Load data train, valid dan test 
        self.train_data = pd.read_csv(os.path.join(self.data_dir, 'train.csv')) # load data train.csv 
        self.valid_data = pd.read_csv(os.path.join(self.data_dir, 'valid.csv')) # Load data valid.csv 
        self.test_data  = pd.read_csv(os.path.join(self.data_dir, 'test.csv'))  # Load data test.csv 
    
    # Buat fungsi untuk untuk memilih fitur yang dilatih 
    def select_features(self, data):
        # Load fitur x dan y dari datasheet yang akan digunakan 
        X = data[self.feature_columns]
        y = data[self.target_column]
        return X, y 
    
    # Buat Fungsi untuk tune hyperparameter model
    def tune_hyperparameter(self, X_train, y_train):
        # perform hyperparameter tuning using grid search cv 
        param_grid = {
            'n_estimators' : [50, 100, 200],
            'max_depth' : [None, 10, 20, 30],
            'min_samples_split' : [2, 5, 10],
            'min_smaples_leaf' : [1,2,4], 
        }

        rf = RandomForestClassifier(random_state=42)                # Load model Random Forest Classifier
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)    # Setting KFold Parameter

        # Setting GridSearchCV Parameter
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=kfold, scoring='accuracy', verbose=1, n_jobs=-1)
        grid_search.fit(X_train, y_train) # Fitting model X (Features) and y (Target)
        
        # mencari parameter terbaik untuk model algoritma random forest 
        self.best_model = grid_search.best_estimator_ 
        # tampilkan parameter terbaik 
        print(f'Best Parameters : {grid_search.best_params_}')

        
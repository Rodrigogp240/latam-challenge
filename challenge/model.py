import os
import pandas as pd
import numpy as np
import xgboost as xgb
import logging

from typing import Tuple, Union, List

from utils.features_generator import FeatrueGenerator

MODEL_PATH :str = 'Delay_model.json'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DelayModel:

    def __init__(
        self
    ):
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=4.4402380952380955)

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        threshold_in_minutes:int = 15
        data['period_day'] = data['Fecha-I'].apply(
            FeatrueGenerator.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(
            FeatrueGenerator.is_high_season)
        data['min_diff'] = data.apply(FeatrueGenerator.get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)
        features = FeatrueGenerator.get_important_fetures(data)

        if target_column:
            return features, data[target_column].to_frame()
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        logging.info('Model is been fit')        
        self._model.fit(features, target.values.ravel())  
        try:
            self._model.save_model(MODEL_PATH)
            logging.info("Model saved successfully.")
        except Exception as e:
            logging.error(f"Error saving the model: {e}")
        return None

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        logging.info('is predicting')
        if os.path.exists(MODEL_PATH):
            self._model.load_model(MODEL_PATH)
            logging.error("Model file loaded.")
        else:
            logging.error("Model file does not exist.")
            return []

        try:
            prediction: np.array = self._model.predict(features)
            logging.info('prediction successful')
            return prediction.tolist()
        except Exception as e:
            logging.error(f"An error occurred during prediction: {e}")
            return []
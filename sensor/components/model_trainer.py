from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd 
import numpy as np
from sensor import utils
from xgboost import XGBClassifier
from sklearn.metrics import f1_score


class Model_Trainer:

    def __init__(self,
                    model_trainer_config:config_entity.ModelTrainerConfig,
                    data_transformation_artifact:artifact_entity.DataTransformationArtifact):

        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            logging.debug(str(e))
            raise SensorException(e, sys)


    def fine_tune(self):
        try:
            # Write code for Grid Search CV
            pass

        except Exception as e:
            logging.debug(str(e))
            raise SensorException(e, sys)


    def train_model(self,X,y):
        """
        This function is used to train model

        X: Independent feature
        y: dependent feature
        =====================================
        return: xgb_classifier
        """
        try:
            xgb_classifier = XGBClassifier()
            xgb_classifier.fit(X,y)
            return xgb_classifier

        except Exception as e:
            logging.debug(str(e))
            raise SensorException(e, sys)



    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_test_path)

            logging.info(f"Splitting input and target feature from both train and test array")
            X_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            X_test, y_test = test_arr[:,:-1], test_arr[:,-1]
            
            logging.info(f"Train The Model")
            model = self.train_model(X=X_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(X_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)

            logging.info(f"train score: {f1_train_score} and test score: {f1_test_score}")
            # Check for Overfitting or Underfitting or Expected Score
            logging.info(f"Checking our model is Underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score is {f1_test_score}")

            logging.info(f"Checking our model is Overfitting or not")
            diff = abs(f1_train_score - f1_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test Score difference: {diff} is more than Overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            
            # Save the trained model
            logging.info(f"Saving Model Object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # Prepare Artifact
            logging.info(f"Preparing Artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                f1_train_score=f1_train_score,
                f1_test_score=f1_test_score)

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            logging.debug(str(e))
            raise SensorException(e, sys)

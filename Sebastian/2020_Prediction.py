#Machine learning, array and dataframe libraries.
import pandas as pd
import numpy as np

import tensorflow
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def election_predict(Zip, Occupation, Amount):

    #Load model. 
    model = load_model("election_model.h5")

    #Dictionary to store the inputs. 
    input_dict = {'Zip' : Zip,"Occupation" :  Occupation, 'Amount' : Amount}

    #Since we will only pass 1 prediction at a time, index = [0] (only 1 row)
    input_df = pd.DataFrame(data = input_dict, index = [0])

    #Empty df to create the encoded values. -----------
    encoded_df = pd.DataFrame()

    for column in input_df[['Zip','Occupation','Amount']]:
        
        #Creates the encoder object.
        encoder = LabelEncoder()
        #Imports the encoded attributes from our original model.
        encoder.classes_ = np.load(f'Model Encoders/encoder{column}.npy', allow_pickle=True)
        #Creates a colmn with the encoded values.
        encoded_df[column] = encoder.transform(input_df[column])

    #Scaler improrts the scaler parameters from our original model.
    X_scaler_USER = MinMaxScaler().fit(pd.read_pickle('https://election-data-2020-red-raiders.s3.us-east-2.amazonaws.com/X_scaler.pkl'))
    #Scales the user input parameters.
    X_USER_scaled = X_scaler_USER.transform(encoded_df)
   
    #model prediction.
    encoded_predictions = model.predict_classes(X_USER_scaled)

    #original encoder of campaign.
    encoder_campign = LabelEncoder()
    encoder_campign.classes_ = np.load(f'Model Encoders/encoderCampaign.npy', allow_pickle=True)

    #Decodes the prediction labels.
    prediction_labels = encoder_campign.inverse_transform(encoded_predictions)

    #Returns the prediction.
    return str(prediction_labels[0])
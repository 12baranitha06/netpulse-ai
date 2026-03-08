import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Sample training data
data = {
    "latency":[10,20,30,60,80,120],
    "loss":[0,0,1,2,5,10],
    "health":["Healthy","Healthy","Healthy","Warning","Warning","Critical"]
}

df = pd.DataFrame(data)

X = df[["latency","loss"]]
y = df["health"]

model = RandomForestClassifier()
model.fit(X,y)

def predict_health(latency,loss):

    prediction = model.predict([[latency,loss]])
   

    return prediction[0]
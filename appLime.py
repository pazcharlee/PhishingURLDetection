#importing required libraries
#Lime is integrated and working, shows the features that effected the score but the features are numerically labeled 
from flask import Flask, request, render_template
import numpy as np
import pickle
import lime
from lime.lime_tabular import LimeTabularExplainer
import warnings
from feature import FeatureExtraction

warnings.filterwarnings('ignore')


file = open("pickle/model2.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

feature_names = ["Feature{}".format(i) for i in range(1, 31)]

# Initialize LIME explainer (dummy data for initialization)
explainer = LimeTabularExplainer(
    training_data=np.random.rand(100, 30),  # Fake data to match feature shape
    feature_names=feature_names,
    mode="classification",
    class_names=["Phishing", "Safe"],
    discretize_continuous=True
)

# Function to generate LIME explanations
def get_lime_explanation(features):
    """
    Generates LIME explanations for the given URL features.
    """
    # Reshape input to match model format
    features = np.array(features).reshape(1, -1)

    # Generate explanation
    exp = explainer.explain_instance(features[0], gbc.predict_proba, num_features=5)

    # Extract explanation as a dictionary
    explanation = {feature: round(weight, 4) for feature, weight in exp.as_list()}
    
    return explanation



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        y_pred = gbc.predict(x)[0]  # Model prediction
        y_pro_phishing = gbc.predict_proba(x)[0, 0]  # Probability it is safe
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]  # Probability it is phishing

        # Generate LIME explanation
        lime_explanation = get_lime_explanation(x)

        return render_template(
            "indexLime.html",
            xx=round(y_pro_non_phishing, 2),
            url=url,
            explanation=lime_explanation  # Always pass this variable
        )

    # **Ensure 'explanation' is defined for GET requests**
    return render_template("indexLime.html", xx=-1, explanation={})


if __name__ == "__main__":
    app.run(debug=True)




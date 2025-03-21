#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pickle
import lime
from lime.lime_tabular import LimeTabularExplainer
import warnings
from feature import FeatureExtraction
import pandas as pd

warnings.filterwarnings('ignore')


file = open("pickle/model2.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)


# Feature explanations in simple terms
feature_explanations = {
    "Has_IP": "URL contains an IP address instead of a domain name (e.g., 192.168.1.1).",
    "Has_At": "URL contains '@' symbol, often used in phishing attacks.",
    "URL_Length": "Long URLs are more likely to be suspicious.",
    "Shortening_Service": "URL is shortened (e.g., bit.ly), commonly used in phishing.",
    "Has_Hyphen": "URL has a hyphen ('-'), which is often found in fake sites.",
    "Has_Double_Slash": "Double slashes ('//') in odd places can indicate phishing.",
    "Domain_Age": "Young domains are often used for phishing attacks.",
    "Domain_End_Period": "Short expiration dates are a red flag for phishing domains.",
    "HTTPS_Token": "URL contains 'https' in an unusual position, which may be deceptive.",
    "Favicon": "Missing or incorrect favicon (website icon) is suspicious.",
    "Port": "Unusual port numbers can be a sign of a malicious site.",
    "HTTPS": "Lack of HTTPS can mean the site is insecure.",
    "Request_URL": "Images or resources are loaded from a different domain (a phishing indicator).",
    "Anchor_Tag": "Links on the page may redirect users unexpectedly.",
    "Links_in_Tags": "Number of links inside script, meta, and form tags.",
    "SFH": "Server Form Handling – insecure forms may steal data.",
    "Submitting_to_Email": "Forms submitting data to an email instead of a server.",
    "Abnormal_URL": "The website URL is not consistent with usual patterns.",
    "Redirects": "Excessive redirections can hide phishing attempts.",
    "On_Mouse_Over": "Hovering over a link changes its destination – often a trick used in phishing.",
    "Right_Click": "Right-clicking is disabled – a tactic used to prevent users from checking security details.",
    "PopUp_Window": "Pop-ups are commonly used in phishing scams.",
    "Iframe": "Invisible frames are used to trick users into entering data.",
    "Age_of_Domain": "A new website domain might indicate a fake site.",
    "DNS_Record": "Lack of proper DNS records suggests a suspicious website.",
    "Web_Traffic": "Legitimate websites usually have more web traffic.",
    "Page_Rank": "Phishing sites generally have low or no Google rankings.",
    "Google_Index": "If Google has not indexed the site, it might not be trustworthy.",
    "Links_Pointing_to_Page": "Too many inbound links from unknown sites can be suspicious.",
    "Statistical_Report": "Certain URLs match known phishing patterns."
}

#feature_names = ["Feature{}".format(i) for i in range(1, 31)]


# Initialize LIME explainer (dummy data for initialization)
explainer = LimeTabularExplainer(
    training_data=np.random.rand(100, 30),  # Fake data to match feature shape
    feature_names=feature_explanations,
    mode="classification",
    class_names=["Phishing", "Safe"],
    discretize_continuous=True
)

def get_lime_explanation(features):
    """
    Generates LIME explanations for the given URL features in a user-friendly format.
    """
    features = np.array(features).reshape(1, -1)

    exp = explainer.explain_instance(features[0], gbc.predict_proba, num_features=5)

    # Convert technical feature names to user-friendly descriptions
    explanation = {}
    for feature, weight in exp.as_list():
        description = feature_explanations.get(feature, feature)  # Get user-friendly name
        influence = "⚠️Increases risk" if weight > 0 else "✅Reduces risk"
        explanation[description] = influence
    
    return explanation

@app.route("/explanation/<feature_name>")
def feature_explanation(feature_name):
    # Retrieve the feature explanation for the clicked feature
    explanation = feature_explanations.get(feature_name, "No explanation available for this feature.")
    
    return render_template("/templates/explanations.html", feature_name=feature_name, feature_explanation=explanation)


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
            "indexLime2.html",
            xx=round(y_pro_non_phishing, 2),
            url=url,
            explanation=lime_explanation  # Always pass this variable
        )

    # **Ensure 'explanation' is defined for GET requests**
    return render_template("indexLime2.html", xx=-1, explanation={})


@app.route('/explanations')
def explanations():
    return render_template('explanations.html')  # Links to explanations.html in templates


if __name__ == "__main__":
    app.run(debug=True)




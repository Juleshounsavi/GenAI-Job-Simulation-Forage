import pandas as pd
from flask import Flask, request, jsonify, render_template

# Load financial data
data = pd.read_csv('financial_data.csv')
data['Revenue Growth (%)'] = data.groupby(['Company'])['Total Revenue'].pct_change() * 100
data['Net Income Growth (%)'] = data.groupby(['Company'])['Net Income'].pct_change() * 100

# Flask app setup
app = Flask(__name__)

# Predefined responses based on analyzed financial data
def get_response(user_query):    
    if user_query == "what does the dataset look like?":
        return f"\n\n{data.head()}\n\n"
    
    elif user_query == "how many companies are present in the dataset?":
        return f"The dataset contains {data['Company'].nunique()} companies.\n\n"
    
    elif user_query == "what is the average revenue growth (%) for each company?":
        avg_growth = data.groupby('Company')['Revenue Growth (%)'].mean()
        return f"Here is the average revenue growth (%) for each company:\n\n{avg_growth.to_string()}\n\n"
    
    elif user_query == "what is the correlation between revenue growth and net income growth?":
        if {'Revenue Growth (%)', 'Net Income Growth (%)'}.issubset(data.columns):
            correlation = data[['Revenue Growth (%)', 'Net Income Growth (%)']].corr()
            return f"The correlation matrix between revenue growth and net income growth is:\n\n{correlation}\n\n"
        else:
            return "The columns 'Revenue Growth (%)' or 'Net Income Growth (%)' are not found in the dataset.\n\n"

      
    elif user_query == "which company had the highest total revenue in the dataset?":
        highest_revenue_company = data.groupby('Company')['Total Revenue'].sum().idxmax()
        total_revenue = data.groupby('Company')['Total Revenue'].sum().max()
        return f"The company with the highest total revenue is {highest_revenue_company}, with a total revenue of {total_revenue}.\n\n"
    
    else:
        return "Sorry, I can only provide information on predefined queries.\n\n"


# Route for chatbot interaction
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.form.get("query")
    response = get_response(user_query)
    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

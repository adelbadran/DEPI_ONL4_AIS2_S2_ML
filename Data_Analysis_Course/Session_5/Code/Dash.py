import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# --- Data Preparation ---
# Load the dataset from the local path
data = pd.read_csv(r"D:\Courses\DEPI R4 - Microsoft ML\Technical\Datasets\Data Analysis\Dash.csv")

# Initialize the Dash application
app = Dash(__name__)
app.title = "Interactive Dashboard"

# Get only numeric columns to use in the dropdown menu
num_cols = data.select_dtypes(include="number").columns

# --- App Layout (UI) ---
app.layout = html.Div([
    html.H1("Interactive Dashboard with pie plot"), # Main heading
    
    html.Label("Select a value to show the pie chart"), # Instruction label
    
    # Dropdown to choose which numeric column to visualize
    dcc.Dropdown(
        id="column-dropdown", 
        options=[{"label": col, "value": col} for col in num_cols], 
        value=num_cols[0] # Default selection (first column)
    ),
    
    # Placeholder for the graph
    dcc.Graph(id="pie-chart")
])

# --- Callback (Logic) ---
# This function updates the chart automatically when the dropdown changes
@app.callback(
    Output("pie-chart", "figure"), 
    Input("column-dropdown", "value")
)
def update_pie(select_col):
    # Group the data by 'Area' and calculate the sum for the selected column
    group = data.groupby("Area")[select_col].sum().reset_index()
    
    # Create a Pie chart (Donut style with hole=0.4)
    fig = px.pie(
        group, 
        names="Area", 
        values=select_col, 
        title=f"Distribution of {select_col} by Area", 
        hole=0.4, 
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    return fig # Return the updated figure to the dcc.Graph component

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True)
from IPython.display import display, HTML
import pandas as pd

# Create a dataset
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Edward', 'Fiona'],
        'Age': [24, 27, 23, 29, 25, 30],
        'City': ['NY', 'LA', 'NY', 'LA', 'NY', 'LA']}
df = pd.DataFrame(data)

def display_side_by_side(styler1, caption1, styler2, caption2):
    # Set the captions
    styler1.set_caption(caption1)
    styler2.set_caption(caption2)
    
    # Get the HTML representations of the styler objects
    html1 = styler1.to_html()
    html2 = styler2.to_html()
    
    # Combine the HTML representations and display them
    display(HTML(f"<table><tr><td>{html1}</td><td>{html2}</td></tr></table>"))

# Grouped by city
grouped = df.groupby('City').apply(lambda x: x.sort_values('Age')).reset_index(drop=True)

# Filtered dataset (Age > 25)
filtered = df[df['Age'] > 25]

# Aggregated dataset
agg_functions = {'Age': ['mean', 'max', 'min']}
aggregated = df.groupby('City').agg(agg_functions).reset_index()

# Transformed dataset
transformed = df.copy()
transformed['Age_Centralized'] = transformed.groupby('City')['Age'].transform(lambda x: x - x.mean())
transformed['Age_Centralized'] = transformed['Age_Centralized'].round(2)

# Create styled versions of the dataframes
style_function = lambda x: ['background: #1f1f7a' if x['City'] == 'NY' else 'background: #4b0082' for v in x]
df_styled = df.style.apply(style_function, axis=1)#.format({'Age_Centralized': '{:.2f}'})
grouped_styled = grouped.style.apply(style_function, axis=1)#.format({'Age_Centralized': '{:.2f}'})
filtered_styled = filtered.style.apply(style_function, axis=1)#.format({'Age_Centralized': '{:.2f}'})
aggregated_styled = aggregated.style.apply(lambda x: ['background: #1f1f7a' if 'NY' in str(x['City']) else 'background: #4b0082' if 'LA' in str(x['City']) else '' for v in x], axis=1)
aggregated_styled = aggregated_styled.format({'Age': '{:.2f}'})

# Transformed dataset
transformed_styled = transformed.style.apply(style_function, axis=1).format({'Age_Centralized': '{:.2f}'})

def display_grouped_city():
    display_side_by_side(df_styled, "Original", grouped_styled, "Grouped by City")

def display_filtered():
    display_side_by_side(df_styled, "Original", filtered_styled, "Filtered Dataset (Age > 25)")

def display_aggregated():
    display_side_by_side(df_styled, "Original", aggregated_styled, "Aggregated Dataset")

def display_transformed():
    display_side_by_side(df_styled, "Original", transformed_styled, "Transformed Dataset")

# Display the pairs of styled dataframes side by side with appropriate captions
#display_side_by_side(df_styled, "Original", grouped_styled, "Grouped by City")
#display_side_by_side(df_styled, "Original", filtered_styled, "Filtered Dataset (Age > 25)")
#display_side_by_side(df_styled, "Original", aggregated_styled, "Aggregated Dataset")
#display_side_by_side(df_styled, "Original", transformed_styled, "Transformed Dataset")

############# Broadcasting
# Function to display three styler objects side by side with captions
def display_side_by_side_3(styler1, caption1, styler2, caption2, styler3, caption3):
    # Set the captions
    styler1.set_caption(caption1)
    styler2.set_caption(caption2)
    styler3.set_caption(caption3)
    
    # Get the HTML representations of the styler objects
    html1 = styler1.to_html()
    html2 = styler2.to_html()
    html3 = styler3.to_html()
    
    # Combine the HTML representations and display them
    display(HTML(f"<table><tr><td>{html1}</td><td>{html2}</td><td>{html3}</td></tr></table>"))

# Create a new dataset and a scalar to demonstrate broadcasting operations
data = {'A': [1, 2], 'B': [3, 4]}
df1 = pd.DataFrame(data)
scalar = 5

# Scenario 1: Adding a scalar to a dataframe
# Create a dataframe filled with the scalar value to visualize the broadcasting operation
scalar_df = pd.DataFrame(scalar, index=df1.index, columns=df1.columns)
result1 = df1 + scalar

# Create styled versions of the dataframes for scenario 1
df1_styled = df1.style.apply(lambda x: ['background: #1f1f7a; color: white' for v in x], axis=1)
scalar_df_styled = scalar_df.style.apply(lambda x: ['background: #4b0082; color: white' for v in x], axis=1)
result1_styled = result1.style.apply(lambda x: ['background: #350f7e; color: white' for v in x], axis=1)

# Display the dataframes for scenario 1 side by side with appropriate captions
#display_side_by_side_3(df1_styled, "DataFrame 1", scalar_df_styled, f"Scalar DataFrame ({scalar})", result1_styled, "Result (DF1 + Scalar)")

# Scenario 2: Combining two dataframes with identical row and column indices
data2 = {'A': [5, 6], 'B': [7, 8]}
df2 = pd.DataFrame(data2)
result2 = df1 + df2

# Create styled versions of the dataframes for scenario 2
df2_styled = df2.style.apply(lambda x: ['background: #4b0082; color: white' for v in x], axis=1)
result2_styled = result2.style.apply(lambda x: ['background: #350f7e; color: white' for v in x], axis=1)

# Display the dataframes for scenario 2 side by side with appropriate captions
#display_side_by_side_3(df1_styled, "DataFrame 1", df2_styled, "DataFrame 2", result2_styled, "Result (DF1 + DF2)")

# Scenario 3: Combining a dataframe with intersecting but dissimilar row and column indices
data3 = {'A': [9], 'C': [10]}
df3 = pd.DataFrame(data3)
result3 = df1.add(df3, fill_value=0)

# Create styled versions of the dataframes for scenario 3
df3_styled = df3.style.apply(lambda x: ['background: #4b0082; color: white' for v in x], axis=1)

color1 = '#1f1f7a'
color3 = '#4b0082'
blend_color = '#350f7e'

# Create styled versions of the dataframes for scenario 3 with specific color rules for each column in the result dataframe
def style_function_3(x):
    styles = []
    for col in x.index:
        if col == 'A':
            styles.append(f'background: {blend_color}; color: white')
        elif col == 'B':
            styles.append(f'background: {color1}; color: white')
        elif col == 'C':
            styles.append(f'background: {color3}; color: white')
    return styles

result3_styled = result3.style.apply(style_function_3, axis=1)

# Display the dataframes for scenario 3 side by side with appropriate captions
#display_side_by_side_3(df1_styled, "DataFrame 1", df3_styled, "DataFrame 3", result3_styled, "Result (DF1 + DF3)")

def display_df_scalar():
    display_side_by_side_3(df1_styled, "DataFrame 1", scalar_df_styled, f"Scalar DataFrame ({scalar})", result1_styled, "Result (DF1 + Scalar)")

def display_df_all_index():
    display_side_by_side_3(df1_styled, "DataFrame 1", df2_styled, "DataFrame 2", result2_styled, "Result (DF1 + DF2)")

def display_df_some_index():
    display_side_by_side_3(df1_styled, "DataFrame 1", df3_styled, "DataFrame 3", result3_styled, "Result (DF1 + DF3)")



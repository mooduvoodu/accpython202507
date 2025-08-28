import pandas as pd
from openai import OpenAI # remember to pip -install openai

# Load the pipe-delimited CSV into a DataFrame
df = pd.read_csv('/workspaces/accpython202507/exampledata/orderdetails.csv', sep='|')
print("DataFrame Schema:")
print(df.dtypes)            # Print schema (column types)
print("\nSample Data:")
print(df.head(5))           # Print first 5 rows as sample

# Prompt the user for a natural language transformation instruction
instruction = input("Enter a transformation instruction: ")

# Construct a prompt that includes the instruction, schema, and sample data
schema_info = df.dtypes.to_string()
sample_data = df.head(5).to_dict(orient='records')
prompt_text = (
    f"Perform the following transformation on the DataFrame:\n{instruction}\n\n"
    f"DataFrame schema:\n{schema_info}\n\n"
    f"First 5 rows:\n{sample_data}\n\n"
    "Provide only the Python pandas code (no explanation) to accomplish this."
)

# Initialize the OpenAI API client with your API key
client = OpenAI(api_key="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")

# Define the messages for the chat completion (system prompt for role and user prompt with instructions)
messages = [
    {"role": "system", "content": "You are a Python data assistant. Only output Python code."},
    {"role": "user", "content": prompt_text}
]

# Use the Chat Completions API (new usage in v1.x)
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
    ,temperature=0  # Use a deterministic setting for consistent output
)

# Extract the generated code from the response
generated_code = response.choices[0].message.content

# Remove any Markdown formatting (e.g., leading/trailing triple backticks)
if generated_code.strip().startswith("```"):
    # Strip away ``` markers and language hints
    generated_code = generated_code.strip().strip("```").strip()

# Execute the returned code in a safe namespace
exec_namespace = {"pd": pd, "df": df}
exec(generated_code, exec_namespace)

# Retrieve the transformed DataFrame (assuming code either modified df or created df_transformed)
result_df = exec_namespace.get("df_transformed", exec_namespace.get("df"))

# Print the resulting transformed DataFrame
print("\nTransformed DataFrame:")
print(result_df)

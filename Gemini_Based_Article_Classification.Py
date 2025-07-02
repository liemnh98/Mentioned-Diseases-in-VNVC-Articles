# Import libraries
import pandas as pd
from google import genai
from google.genai import types
from datetime import datetime

# Configs
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
mapping_output_dir = f"data_demo/output/mapping_results_test.csv"

model_id = 'gemini-2.5-flash-preview-04-17'
diseases_dir = 'data_demo/input/TenNhomBenh.xlsx'
urls_dir = 'data_demo/input/urls_test.csv'

# load key
with open("keys/Gemini_API_Key.txt", "r") as file:
    GEMINI_API_KEY = file.read()

# Load list of diseases
diseases = pd.read_excel(diseases_dir)

# Transform diseases to a list, separated by semi-colon
diseases_list = diseases['TenNhomBenh'].tolist()
diseases_list = ';'.join(diseases_list)

# Load list of urls
urls = pd.read_csv(urls_dir)
urls.rename(columns={0: 'url'}, inplace=True)
urls['url'] = urls['destinationURL_cleaned'].str.strip()

# Slicing the urls to get a subset for testing
urls = urls.iloc[401:800].reset_index(drop=True)

# Define prompt template
PROMPT_TEMPLATE = """
You are a classification assistant.

Given the blog at this URL:
{url}

Check only the following diseases:
{diseases_list}

INSTRUCTIONS:
- Mark a disease only if the article has at least 1000 words of real content about it (e.g. symptoms, treatment, prevention, vaccines).
- The disease MUST relevant to the article's main content.
- Ignore diseases that are only listed, briefly mentioned, or appear in ads, footers, package listings, catalogs, price tables, or promotional content.
- Focus only on the main body of the article.
- Ignore the whole url if the page contents is a product catalog, summary list, or pricing page.
- Do not guess. If unsure, exclude it.

OUTPUT FORMAT:
Return only a semicolon-separated list of matching disease names exactly as written above.
If none match, return: "none"

DO NOT explain. DO NOT add notes. ONLY return the list.
"""


# Generate Answer
def generate_answer(url):
    # format the prompt with the URL and diseases list
    prompt = PROMPT_TEMPLATE.format(url=url, diseases_list=diseases_list)

    # create client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Enable the ability to browse the url content
    tools = [
        types.Tool(url_context=types.UrlContext()),
    ]

    # Define the content generation configuration
    generate_content_config = types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0,
        top_p=0.99,
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
        tools=tools,
        response_mime_type="text/plain",
    )

    # generate answer
    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=generate_content_config,
    )
    return response.text


# indentify diseases mentioned in each url
def diseases_identifier(url_series):
    total = len(url_series)

    answered_diseases = []
    for idx, url in enumerate(url_series, 1):
        answer = generate_answer(url)
        answered_diseases.append(answer)
        percent = 100 * idx / total
        print(f"\rProcessed: {idx}/{total} ({percent:.1f}%)", end='', flush=True)
    print()  # Move to next line after completion
    return pd.DataFrame({'url': url_series, 'mentioned_diseases': answered_diseases})


results_df = diseases_identifier(urls['url'])

# Pre-process the results_df
result_cleanned = results_df.copy()
result_cleanned = result_cleanned.assign(
    mentioned_diseases=result_cleanned['mentioned_diseases'].str.split(';')
).explode('mentioned_diseases')
result_cleanned['mentioned_diseases'] = (
    result_cleanned['mentioned_diseases'].str.strip().str.lower()
)

# Pre-process the diseases data
diseases_cleaned = diseases.copy()
diseases_cleaned['disease_lower'] = (
    diseases_cleaned['TenNhomBenh'].str.strip().str.lower()
)

# Merge the results
mapping_df = pd.merge(
    diseases_cleaned,
    result_cleanned,
    left_on='disease_lower',
    right_on='mentioned_diseases',
    how='inner',
)
mapping_df.rename(columns={'TenNhomBenh': 'disease'}, inplace=True)
mapping_df = mapping_df[['url', 'disease']]

# Sort the mapping_df by url
mapping_df = mapping_df.sort_values(by='url').reset_index(drop=True)

# Add a column for total diseases mentioned per url
mapping_df['total_diseases'] = mapping_df.groupby('url')['url'].transform('count')

# Save the mapping results to a CSV file
mapping_df.to_csv(mapping_output_dir, index=False)
print(f"Mapping results saved to {mapping_output_dir}")

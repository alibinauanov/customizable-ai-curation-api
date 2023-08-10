import openai
import apikey

# Set your OpenAI API key
openai.api_key = apikey.api

def curate_content(input_data):
    curation_methods = input_data['curation_methods']
    content_to_curate = input_data['content_to_curate']

    # Process curation methods into a structured prompt
    curation_prompt = "\n".join([f"- {method}" for method in curation_methods])

    # Generate a single prompt for GPT-3.5 Turbo
    prompt = f"Given the following curation methods:\n{curation_prompt}\n\nCurate the following content:\n{content_to_curate}\n\nCurated Result:\n"

    # Call the OpenAI API to generate curated content
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=300
    )

    curated_result = response.choices[0].text.strip()
    return curated_result

# Example input data
input_data = {
    "curation_methods": [
        "filter out tweets that are irrelevant to business",
        "summarize the rest into one paragraph",
        "each business related tweet should be summarized briefly into one sentence",
        "remove duplicated content"
    ],
    "content_to_curate": "40 urls Twitter accounts"
}

# Call the curate_content function with the example input
curated_output = curate_content(input_data)

# Print the curated result
print(curated_output)

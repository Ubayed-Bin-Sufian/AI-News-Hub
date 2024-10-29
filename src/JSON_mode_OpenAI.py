# documentation url: https://platform.openai.com/docs/guides/structured-outputs/json-mode
# youtube tutorial: https://www.youtube.com/watch?v=UtwDAge75Ag

from openai import OpenAI
import json  # for JSON handling

OPENAI_KEY=""
client = OpenAI(api_key=OPENAI_KEY)

# Example JSON format for expected output to guide the model's response
example_json = {
  "ski_resorts": [
    {
      "name": "Les Portes du Soleil",
      "slope_kilometers": 600
    }
  ]
}

# Defining the prompt to instruct the model on what data to generate
prompt = "Provide valid JSON output. Provide the top 10 largest ski resorst in Europe. Rankin them on slope kilometers (descending) Provide one column 'name' and a column 'slope_kilometers' representing the total slope kilometers"

chat_completion = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type":"json_object"},  # Specifies that the response should be a JSON object
    messages = [
        {
            "role": "system",

            # the json.dumps(example_json) function call is used to convert the example_json dictionary into a JSON-formatted string
            "content": "Provide output in valid JSON. The data schema should be like this: " + json.dumps(example_json)
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# # To find what model we are using
# print(chat_completion.model)

# Checking if the completion was successful based on the finish reason
finish_reason = chat_completion.choices[0].finish_reason


# The following code snippet is helpful for limiting the use of tokens
# If the completion was successful, parse and display the data
if(finish_reason == "stop"):
    data = chat_completion.choices[0].message.content
    print(data)

    # Parsing the JSON data into a Python dictionary
    ski_resorts = json.loads(data)
    print(ski_resorts)

    # Iterating through the list of ski resorts and printing their names and slope kilometers
    for ski_resort in ski_resorts['ski_resorts']:
      print(ski_resort['name'] + " : " + str(ski_resort['slope_kilometers']) + "km")

else :
    print("Error! provide more tokens please")
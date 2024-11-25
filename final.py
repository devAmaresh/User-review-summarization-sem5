from initial_summary import *
from using_reward_models import *
from templates import *
from sentiment import *

input_file_path = 'input_text.txt'

try:
    with open(input_file_path, 'r', encoding='UTF-8') as file:
        input_text = file.read().strip() 
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    
# Step 1: Create pipeline
pipeline = create_pipeline("./llama_model")
print(f"Pipeline created: {pipeline}")

# Step 2: Extract entity name (topic) from the input text
topic = extract_entity_name(pipeline, input_text)
print(f"Extracted topic: {topic}")

# Step 3: Generate aspect polarity sentence prompt
aspect_polarity_sentence_prompt = aspect_polarity_template().format(topic=topic, review=input_text)
print(aspect_polarity_sentence_prompt)
aspect_polarity_sentence_prompt = f"{aspect_polarity_sentence_prompt}\n Topic is :{topic} \n Review is:{input_text}"


# Step 4: Generate aspect polarity sentence using the pipeline
aspect_polarity_sentence = generate_aspect_polarity_sentence(pipeline, aspect_polarity_sentence_prompt)
print(f"Aspect polarity sentence: {aspect_polarity_sentence}")

# Step 5: Generate initial summary prompt
initial_summary_prompt = initial_summary_template().format(topic=topic, text=aspect_polarity_sentence)

# Step 6: Generate the initial summary dictionary using the pipeline
initial_summary = generate_summary(pipeline, initial_summary_prompt)
print("Positive/Neutral Summary:")
print(initial_summary["positive_neutral"])
print("\nNegative/Neutral Summary:")
print(initial_summary["negative_neutral"])

positive_summary = initial_summary['positive_neutral']
negative_summary = initial_summary['negative_neutral']

# Step 7: Create a refined prompt using the initial summary
positive_prompt = prompt_for_refinement(input_text, positive_summary, topic)
negative_prompt = prompt_for_refinement(input_text, negative_summary, topic)

if positive_prompt == True:
    # If no refinement is needed, skip refinement and directly jump to Step 9
    print("Initial positive summary is correct, proceeding to final summary.")
    positive_summary = initial_summary  # Use the initial summary directly as the final summary
else:
    # If refinement is needed, proceed with generating the final summary
    print(f"Refinement prompt: {positive_prompt}")
    # Step 8: Generate the final summary using the pipeline
    positive_summary = generate_summary(pipeline, positive_prompt)
    print(f"Final positive summary: {positive_summary}")

if negative_prompt == True:
    # If no refinement is needed, skip refinement and directly jump to Step 9
    print("Initial negative summary is correct, proceeding to final summary.")
    negative_summary = initial_summary  # Use the initial summary directly as the final summary
else:
    # If refinement is needed, proceed with generating the final summary
    print(f"Refinement prompt: {negative_prompt}")
    # Step 8: Generate the final summary using the pipeline
    negative_summary = generate_summary(pipeline, negative_prompt)
    print(f"Final negative summary: {negative_summary}")


summary = positive_summary + negative_summary
# Step 9: Get the sentiment of the final summary
review_sentiment = get_sentiment(summary)
print(f"Review sentiment: {review_sentiment}")


# Step 10: Save the summary to a text file
output_file_path = './summary_output.txt'
with open(output_file_path, 'w', encoding='UTF-8') as f:
    f.write(summary)


print(f"Summary has been saved to {output_file_path}")

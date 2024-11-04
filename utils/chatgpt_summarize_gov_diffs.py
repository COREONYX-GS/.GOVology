import os
import base64
from openai import OpenAI

OPENAI_MODEL="gpt-4o-mini"
OPENAI_MODEL="gpt-4o"

def load_diff_from_env_var(diff_contents):
    decoded_diff = base64.b64decode(diff_contents).decode('utf-8')
    return decoded_diff

def load_prompt(prompt_file_path, diff_string):
    # Load the prompt from the specified file
    with open(prompt_file_path, 'r') as file:
        prompt = file.read()

    # Insert the diff content into the prompt   
    prompt = prompt.replace("{{DIFF}}", diff_string)

    return prompt

def summarize_diff(diff, prompt):
    client = OpenAI()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Output Markdown Only"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    diff = os.getenv("ISSUE_BODY", "")
    prompt_path = os.getenv("PROMPT_FILE_PATH", "utils/chatgpt_summarize_gov_diffs - prompt.txt")

    diff_content = load_diff_from_env_var(diff)
    
    prompt_content = load_prompt(prompt_path, diff_content)   
    print(prompt_content)

    summary = summarize_diff(diff_content, prompt_content)
    print(summary)

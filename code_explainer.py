#@title Gradio App
import gradio as gr
import os
import google.generativeai as palm

# load model
# PaLM API Key here
palm.configure(api_key='Api_Key') #REPLACE WITH YOUR ACTUAL KEY

# define completion function
def get_completion(code_snippet):

    python_code_examples = f"""
    ---------------------
    Example 1: Code Snippet
    x = 10
    def foo():
        global x
        x = 5
    foo()
    print(x)
    Correct output: 5
    Code Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
    So, print(x) outside the function prints the modified value, which is 5.
    ---------------------
    Example 2: Code Snippet
    def modify_list(input_list):
        input_list.append(4)
        input_list = [1, 2, 3]
    my_list = [0]
    modify_list(my_list)
    print(my_list)
    Correct output: [0, 4]
    Code Explanation: Inside the modify_list function, an element 4 is appended to input_list.
    Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
    So, print(my_list) outputs [0, 4].
    ---------------------
    """

    prompt = f"""
    Your task is to act as a Python Code Explainer.
    I'll give you a Code Snippet.
    Your job is to explain the Code Snippet step-by-step.
    Break down the code into as many steps as possible.
    Share intermediate checkpoints & steps along with results.
    Few good examples of Python code output between #### separator:
    ####
    {python_code_examples}
    ####
    Code Snippet is shared below, delimited with triple backticks:
    ```
    {code_snippet}
    ```
    """

    try:
        completion = palm.generate_text(
            model="models/text-bison-001", # Specify the model
            prompt=prompt,
            temperature=0,
            max_output_tokens=500,
        )

        # Correct way to access the generated text
        response = completion.candidates[0]["output"] if completion.candidates else "No response from the model."
        return response
    except Exception as e:
        return f"An error occurred: {e}"


# define app UI
iface = gr.Interface(
    fn=get_completion,
    inputs=[gr.Textbox(label="Insert Code Snippet", lines=5)],
    outputs=[gr.Textbox(label="Explanation", lines=10)], # Increased lines for better display
    title="Python Code Explainer"
)

iface.launch(share=True)

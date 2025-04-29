import ollama
import json

def analyze_goal(project_idea: str) -> list[str]:
    """
    Analyzes the project idea using a local LLM to identify necessary agent roles.

    Args:
        project_idea: A string describing the user's project idea.

    Returns:
        A list of strings, where each string is the name of an identified agent role.
        Returns an empty list in case of errors or no roles identified.
    """
    try:
        # Craft a prompt for the LLM to identify roles
        prompt = f"""Analyze the following project idea and identify the key agent roles required to build it. List the roles as a JSON array of strings. Only output the JSON array.

Project Idea: {project_idea}

Examples of roles: Planner Agent, Coder Agent, UI Agent, Data Agent, Testing Agent, Documentation Agent.

JSON Array of Roles:"""

        # Call the local Mistral LLM via Ollama
        # Ensure you have the 'mistral' model pulled locally (e.g., by running 'ollama pull mistral' in your terminal)
        response = ollama.chat(
            model='mistral',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            format='json'
        )

        # Parse the JSON response
        # The response structure might vary slightly based on Ollama version/model
        # We expect the content to be a JSON string representing a list of roles
        content = response['message']['content']
        roles = json.loads(content)

        # Ensure the parsed result is a list of strings
        if isinstance(roles, list) and all(isinstance(role, str) for role in roles):
            return roles
        else:
            print(f"Warning: LLM response was not a list of strings: {roles}")
            return []

    except ollama.ResponseError as e:
        print(f"Error calling Ollama: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Example usage (for testing purposes, can be removed later)
if __name__ == '__main__':
    test_idea = "Build a web application that allows users to upload CSV files, visualize the data, and perform basic statistical analysis."
    identified_roles = analyze_goal(test_idea)
    print(f"Identified Roles for '{test_idea}': {identified_roles}")

    test_idea_2 = "Create a command-line tool that converts markdown files to HTML."
    identified_roles_2 = analyze_goal(test_idea_2)
    print(f"Identified Roles for '{test_idea_2}': {identified_roles_2}")

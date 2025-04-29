import ollama

def visualize_call_chain(project_idea: str, agent_roles: list[str]) -> str:
    """
    Describes the logical call chain and interaction flow between identified agents.

    Args:
        project_idea: A string describing the user's project idea.
        agent_roles: A list of strings, where each string is the name of an agent role.

    Returns:
        A string containing a human-readable description of the agent call chain.
        Returns an empty string in case of errors or no description generated.
    """
    try:
        # Craft a prompt for the LLM to describe the call chain
        roles_list_str = ', '.join(agent_roles)
        prompt = f"""Based on the following project idea and the identified agent roles, describe the logical flow and interaction between these agents using a call chain mechanism (like calling subordinates). Explain which agent would likely initiate tasks, which agents it would call upon, and for what purpose, to achieve the overall project goal. Illustrate the potential dependencies and the overall orchestration. Provide a clear, human-readable explanation.

Project Idea: {project_idea}

Identified Agent Roles: {roles_list_str}

Describe the Agent Call Chain:"""

        # Call the local Mistral LLM via Ollama
        response = ollama.chat(
            model='mistral',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )

        # Extract the generated description text
        call_chain_description = response['message']['content'].strip()

        return call_chain_description

    except ollama.ResponseError as e:
        print(f"Error calling Ollama for call chain visualization: {e}")
        return "Error generating call chain description."
    except Exception as e:
        print(f"An unexpected error occurred during call chain visualization: {e}")
        return "Error generating call chain description."

# Example usage (for testing purposes, can be removed later)
if __name__ == '__main__':
    test_idea = "Build a simple task management command-line application."
    test_roles = ["Planner Agent", "Coder Agent", "Testing Agent"]
    call_chain = visualize_call_chain(test_idea, test_roles)
    print(f"\n--- Agent Call Chain Description ---")
    print(call_chain)
    print("----------------------------------")

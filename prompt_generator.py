import ollama
import json

def generate_prompts(project_idea: str, agent_roles: list[str]) -> dict[str, str]:
    """
    Generates detailed system prompts for each identified agent role based on the project idea.

    Args:
        project_idea: A string describing the user's project idea.
        agent_roles: A list of strings, where each string is the name of an agent role.

    Returns:
        A dictionary where keys are the agent role names (strings) and values are the generated system prompts (strings).
        Returns an empty dictionary in case of errors or no prompts generated.
    """
    generated_prompts = {}

    for role in agent_roles:
        try:
            # Craft a prompt for the LLM to generate the system prompt for a specific role
            prompt = f"""Based on the following project idea, generate a detailed system prompt for the '{role}'. The system prompt should clearly define the agent's purpose, specific responsibilities related to the project, any constraints it must follow, and the expected format or type of output. The output should be the system prompt text only, without any introductory or concluding remarks.

Project Idea: {project_idea}

Agent Role: {role}

Generate System Prompt for '{role}':"""

            # Call the local Mistral LLM via Ollama
            response = ollama.chat(
                model='mistral',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                # We don't request JSON format here as we want the raw prompt text
            )

            # Extract the generated prompt text
            system_prompt_text = response['message']['content'].strip()

            if system_prompt_text:
                generated_prompts[role] = system_prompt_text
            else:
                print(f"Warning: LLM generated empty prompt for role: {role}")

        except ollama.ResponseError as e:
            print(f"Error calling Ollama for role {role}: {e}")
            # Continue to the next role even if one fails
        except Exception as e:
            print(f"An unexpected error occurred for role {role}: {e}")
            # Continue to the next role even if one fails

    return generated_prompts

# Example usage (for testing purposes, can be removed later)
if __name__ == '__main__':
    test_idea = "Build a simple task management command-line application."
    test_roles = ["Planner Agent", "Coder Agent", "Testing Agent"]
    generated = generate_prompts(test_idea, test_roles)
    for role, prompt in generated.items():
        print(f"\n--- System Prompt for {role} ---")
        print(prompt)
        print("--------------------------")

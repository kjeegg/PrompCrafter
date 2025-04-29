import streamlit as st
import json

# Import the other components
from goal_analyzer import analyze_goal
from prompt_generator import generate_prompts
from call_chain_visualizer import visualize_call_chain

st.title('PromptCrafter: Local LLM Agent Chain Generator')

st.write('Enter your project idea below to generate a prompt chain for local LLM agents.')

project_idea = st.text_area('Project Idea', height=200, help='Describe the project you want to build with local LLM agents.')

# Initialize session state for storing results if needed across reruns
# if 'roles' not in st.session_state:
#     st.session_state.roles = None
# if 'prompts' not in st.session_state:
#     st.session_state.prompts = None
# if 'call_chain' not in st.session_state:
#     st.session_state.call_chain = None

if st.button('Generate Prompt Chain'):
    if not project_idea:
        st.warning('Please enter a project idea.')
    else:
        st.info('Analyzing project idea and generating prompt chain...')

        # 1. Analyze Goal to get Agent Roles
        agent_roles = analyze_goal(project_idea)
        # st.session_state.roles = agent_roles # Store in session state if needed

        if agent_roles:
            st.subheader('Identified Agent Roles')
            st.text_area('Roles', value=', '.join(agent_roles), height=100, key='roles_output', disabled=True)

            # 2. Generate System Prompts for each role
            system_prompts = generate_prompts(project_idea, agent_roles)
            # st.session_state.prompts = system_prompts # Store in session state

            st.subheader('Generated System Prompts')
            # Display prompts in a readable format
            prompts_display = ""
            for role, prompt_text in system_prompts.items():
                prompts_display += f"--- {role} ---\n{prompt_text}\n\n"
            st.text_area('System Prompts', value=prompts_display.strip(), height=400, key='prompts_output', disabled=True)

            # 3. Visualize Call Chain
            call_chain_description = visualize_call_chain(project_idea, agent_roles)
            # st.session_state.call_chain = call_chain_description # Store in session state

            st.subheader('Agent Call Chain')
            st.text_area('Call Chain Description', value=call_chain_description, height=200, key='chain_output', disabled=True)

            # 4. Exporter Functionality
            st.subheader('Exporter')
            st.write('Copy the generated prompt chain details below:')

            # Combine all output into a structured format for easy copying
            full_output = {
                "project_idea": project_idea,
                "identified_agent_roles": agent_roles,
                "generated_system_prompts": system_prompts,
                "agent_call_chain_description": call_chain_description
            }

            # Display as JSON in a text area
            st.text_area(
                'Full Prompt Chain (JSON)',
                value=json.dumps(full_output, indent=4),
                height=500,
                key='full_output_json',
                disabled=True # Disable editing, only for copying
            )
            st.info('Copy the content from the text area above.')

        else:
            st.warning('Could not identify agent roles for the given project idea.')

else:
    st.info('Enter your project idea and click "Generate Prompt Chain" to begin.')

# Optional: Display results if they exist in session state (useful if not regenerating every time)
# if st.session_state.roles:
#     st.subheader('Identified Agent Roles')
#     st.text_area('Roles', value=', '.join(st.session_state.roles), height=100, key='roles_output_display', disabled=True)
#
# if st.session_state.prompts:
#     st.subheader('Generated System Prompts')
#     prompts_display = ""
#     for role, prompt_text in st.session_state.prompts.items():
#         prompts_display += f"--- {role} ---\n{prompt_text}\n\n"
#     st.text_area('System Prompts', value=prompts_display.strip(), height=400, key='prompts_output_display', disabled=True)
#
# if st.session_state.call_chain:
#     st.subheader('Agent Call Chain')
#     st.text_area('Call Chain Description', value=st.session_state.call_chain, height=200, key='chain_output_display', disabled=True)
#
#     st.subheader('Exporter')
#     st.write('Copy the generated prompt chain details below:')
#     full_output = {
#         "project_idea": project_idea, # Note: project_idea might be empty on rerun if not in session state
#         "identified_agent_roles": st.session_state.roles,
#         "generated_system_prompts": st.session_state.prompts,
#         "agent_call_chain_description": st.session_state.call_chain
#     }
#     st.text_area(
#         'Full Prompt Chain (JSON)',
#         value=json.dumps(full_output, indent=4),
#         height=500,
#         key='full_output_json_display',
#         disabled=True
#     )
#     st.info('Copy the content from the text area above.')

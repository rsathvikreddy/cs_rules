import streamlit as st
import yaml
import subprocess
from pathlib import Path

# GitHub repository information
GITHUB_REPO = 'https://github.com/rsathvikreddy/cs_rules.git'

def main():
    st.title('Coding Standard Rule Viewer')

    st.markdown("""
    ## Paste your coding standard rules below:
    """)

    # Create a text area for the user to paste the rules
    rules_text = st.text_area('Paste rules here', height=800)

    if st.button('Submit'):
        try:
            # Parse the YAML content to get the rules and id
            rules_list = yaml.safe_load(rules_text)
            for rule in rules_list['rules']:
                # Extract the id field
                rule_id = rule.get('id')
                if rule_id:
                    # Store each rule in a YAML file with the id as filename
                    save_to_yaml(rule, filename=f"rules/{rule_id}.yaml", original_yaml=rules_text)
                    st.success(f'Rule saved successfully with ID: {rule_id}')

                    # Commit changes to GitHub
                    commit_to_github(f"Added rule {rule_id}")

                else:
                    st.error('ID field not found or empty in the YAML content.')

            # Clear the text area after processing
            rules_text = ''

        except yaml.YAMLError as e:
            st.error(f'Error parsing YAML: {e}')

def save_to_yaml(rule_dict, filename, original_yaml):
    yaml_path = Path(filename)
    with yaml_path.open('w') as file:
        file.write(original_yaml)

def commit_to_github(commit_message):
    try:
        # Change directory to the repository
        subprocess.run(['git', 'checkout', 'main'], check=True)
        subprocess.run(['git', 'pull'], check=True)  # Ensure we have the latest changes

        # Add and commit changes
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        # Push changes to the remote repository
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)

        st.info('Changes committed and pushed to GitHub successfully.')

    except subprocess.CalledProcessError as e:
        st.error(f'Error committing to GitHub: {e}')

if __name__ == '__main__':
    main()

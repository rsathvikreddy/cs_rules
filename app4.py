import streamlit as st
import yaml
from pathlib import Path

def main():
    st.title('Coding Standard Rule Viewer')

    st.markdown("""
    ## Paste your coding standard rules below:
    """)

    # Create a text area for the user to paste the rules
    rules_text = st.text_area('Paste rules here', height=500)

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

if __name__ == '__main__':
    main()

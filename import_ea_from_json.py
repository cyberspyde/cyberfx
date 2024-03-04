no_comment_data_path = "path"  # Replace with the actual folder path

with open(no_comment_data_path, 'r') as f:
    data = json.load(f)
    for ea_data in data:
    # Create an instance of the ExpertAdvisor model
        advisor = ExpertAdvisor(
            number=ea_data['Number'],
            ea_name=ea_data['EA Name'],
            personal_review=ea_data['Review'],
            lessons_learned=ea_data['Lessons Learned']
        )
        advisor.save()
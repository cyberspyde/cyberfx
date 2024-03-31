with open('cyberfx/eas.csv', 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:            
        advisor = ExpertAdvisor(ea_name=row[0])
        advisor.save()
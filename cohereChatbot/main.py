from cohereAI import invoke_model

while 1:
    query = str(input("\nYour question: "))
    if query.lower() == "exit" or query.lower() == "good bye":
        invoke_model(query, "ab1")
        break;
    invoke_model(query, "ab1")

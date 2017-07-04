




def clearMemory():
    print("""
    Would you like to clear the memory of all of the data parsed so far"""+
    """, or keep all data to be placed into a single Excel spreadsheet """+
    """later?""")
    answer2 = input("> ").lower()
    if 'clear' in answer2 or 'empty' in answer2 or 'y' in answer2:
        g.itemsToBeParsed[:] = []
        g.items[:] = []
        g.projects[:] = []
        g.fiscalYears[:] = []
        g.onTheFlyParsing[:] = []
        print("""
    Memory Cleared.""")
        return
    elif 'keep' in answer2 or 'save' in answer2 or 'n' in answer2:
        print('''
    Ok. Memory contents kept.''')
        return
    else:
        clearMemory()

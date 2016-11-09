input_object = 'input.csv'
output_object = 'output.csv'
settings_file = 'settings_file'
training_file = 'training_file.json'

if os.path.exists(settings_file):
    print 'reading from', settings_file
    deduper = dedupe.StaticDedupe(settings_file)

else:
    fields = [
        {'field':'city', 'type':'Exact'}
    ]

    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)

    # To train dedupe, we feed it a random sample of records.
    deduper.sample(data_d, 150000)


    # If we have training data saved from a previous run of dedupe,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
    if os.path.exists(training_file):
        print 'reading labeled examples from ', training_file
        deduper.readTraining(training_file)

    # ## Active learning
    # Dedupe will find the next pair of records
    # it is least certain about and ask you to label them as duplicates
    # or not.
    # use 'y', 'n' and 'u' keys to flag duplicates
    # press 'f' when you are finished
    print 'starting active labeling...'

    dedupe.consoleLabel(deduper)

    deduper.train()

    # When finished, save our training away to disk
    deduper.writeTraining(training_file)

    # Save our weights and predicates to disk.  If the settings file
    # exists, we will skip all the training and learning next time we run
    # this file.
    deduper.writeSettings(settings_file)

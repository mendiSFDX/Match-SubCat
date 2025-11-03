import csv

def match_sentences(sheet1_path, sheet2_path, output_path):
    # Read sentences from sheet2 and store them
    with open(sheet2_path, 'r', newline='') as sheet2_file:
        reader = csv.reader(sheet2_file)
        next(reader)  # Skip header
        sheet2_sentences = [row[0] for row in reader]

    # Prepare to write the output
    with open(sheet1_path, 'r', newline='') as sheet1_file, \
         open(output_path, 'w', newline='') as output_file:

        reader = csv.reader(sheet1_file)
        writer = csv.writer(output_file)

        # Read header from sheet1
        header1 = next(reader)[0]
        
        # Find the maximum number of matches to determine the number of columns
        max_matches = 0
        
        # First pass to determine the number of columns
        sheet1_file.seek(0) # Reset file pointer
        next(reader) # Skip header again
        for row in reader:
            sheet1_sentence = row[0]
            sheet1_words = set(sheet1_sentence.split())
            
            matches = []
            for sheet2_sentence in sheet2_sentences:
                sheet2_words = set(sheet2_sentence.split())
                if sheet1_words.intersection(sheet2_words):
                    matches.append(sheet2_sentence)
            
            if len(matches) > max_matches:
                max_matches = len(matches)

        # Prepare the output header
        output_header = [header1] + [f'Match {i+1}' for i in range(max_matches)]
        writer.writerow(output_header)

        # Second pass to write the data
        sheet1_file.seek(0) # Reset file pointer
        next(reader) # Skip header
        for row in reader:
            sheet1_sentence = row[0]
            sheet1_words = set(sheet1_sentence.split())
            
            matches = []
            for sheet2_sentence in sheet2_sentences:
                sheet2_words = set(sheet2_sentence.split())
                if sheet1_words.intersection(sheet2_words):
                    matches.append(sheet2_sentence)
            
            writer.writerow([sheet1_sentence] + matches)


if __name__ == "__main__":
    sheet1 = 'sheet1.csv'
    sheet2 = 'sheet2.csv'
    output = 'output.csv'
    match_sentences(sheet1, sheet2, output)
    print(f"Processing complete. Output written to {output}")
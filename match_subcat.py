import csv

def match_sentences_two_columns_case_insensitive(sheet1_path, sheet2_path, output_path):
    # Read sentences from sheet2 and store them
    with open(sheet2_path, 'r', newline='') as sheet2_file:
        reader = csv.reader(sheet2_file)
        sheet2_header = next(reader)
        sheet2_data = [row for row in reader]

    # Prepare to write the output
    with open(sheet1_path, 'r', newline='') as sheet1_file, \
         open(output_path, 'w', newline='') as output_file:

        reader1 = csv.reader(sheet1_file)
        writer = csv.writer(output_file)

        header1 = next(reader1)[0]
        
        # Process data and store results in memory to determine max_matches
        results = []
        max_matches = 0
        sheet1_file.seek(0)
        next(reader1)
        for row in reader1:
            sheet1_sentence = row[0]
            sheet1_words = {word.lower() for word in sheet1_sentence.split()}
            
            current_matches = []
            for sheet2_row in sheet2_data:
                col_a = sheet2_row[0] if len(sheet2_row) > 0 else ""
                col_b = sheet2_row[1] if len(sheet2_row) > 1 else ""
                
                col_a_words = {word.lower() for word in col_a.split()}
                col_b_words = {word.lower() for word in col_b.split()}

                if sheet1_words.intersection(col_a_words) or sheet1_words.intersection(col_b_words):
                    current_matches.append((col_a, col_b))
            
            results.append((sheet1_sentence, current_matches))
            if len(current_matches) > max_matches:
                max_matches = len(current_matches)

        # Prepare and write the output header
        output_header = [header1]
        for i in range(max_matches):
            output_header.extend([f'{sheet2_header[0]}_{i+1}', f'{sheet2_header[1]}_{i+1}'])
        writer.writerow(output_header)

        # Write the data from results
        for sheet1_sentence, matches in results:
            output_row = [sheet1_sentence]
            for match in matches:
                output_row.extend(match)
            # Pad the row if necessary
            output_row.extend([''] * (2 * (max_matches - len(matches))))
            writer.writerow(output_row)


if __name__ == "__main__":
    sheet1 = 'sheet1.csv'
    sheet2 = 'sheet2.csv'
    output = 'output.csv'
    match_sentences_two_columns_case_insensitive(sheet1, sheet2, output)
    print(f"Processing complete. Output written to {output}")

import re
import csv
import re


def fix_broken_csv(input_file, output_file):
    id_timestamp_pattern = re.compile(r"^\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8", newline=""
    ) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        buffer = []
        first_line = True

        # Read the header from the input file and write it to the output file
        header = next(reader)
        writer.writerow(header)

        for line in infile:
            line = line.rstrip("\n")  # Retain trailing newlines by using rstrip('\n')

            # Check if the line matches the pattern for a new entry
            if id_timestamp_pattern.match(line):
                # If buffer is not empty, process the previous buffered entry
                if not first_line:
                    combined_line = "\n".join(buffer)
                    # Add closing quote if the previous entry was not closed properly
                    if combined_line.count('"') % 2 != 0:
                        combined_line += '"'
                    writer.writerow(csv.reader([combined_line]).__next__())

                # Start a new buffer with the current line
                buffer = [line]
                first_line = False
            else:
                # Continue the buffer
                buffer.append(line)

        # Handle the last buffer if not empty
        if buffer:
            combined_line = "\n".join(buffer)
            # Add closing quote if the last entry was not closed properly
            if combined_line.count('"') % 2 != 0:
                combined_line += '"'
            writer.writerow(csv.reader([combined_line]).__next__())


# Replace 'input.csv' and 'output.csv' with your file paths
fix_broken_csv("test/data.csv", "test/output.csv")

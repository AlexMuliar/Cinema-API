import csv
import io


def report_query_to_csv(data) -> str:
    fields = ["Movie", "Date", "Tickets sold"]
    with io.StringIO() as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(fields)
        current_movie = None
        for movie, date, count in data:
            if current_movie != movie:
                writer.writerow([movie, date, count])
                current_movie = movie
            else:
                writer.writerow(["", date, count])
        return csv_file.getvalue()

from googleapiclient.discovery import build

# Hard coded variables. These should never change.
GOOGLE_API_KEY = open('credentials/google_api_key.txt').read()
SPREADSHEET_ID = "1ppRCtwky1qtUGSNIne_OGmf0mqLjegcnBZs7u1Y9sSI"
RANGE = 'Ratings!A2:E'


# pull in data
service = build('sheets', 'v4', developerKey= GOOGLE_API_KEY)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range= RANGE).execute()

table = sorted(result['values'],  key=lambda x: x[4], reverse=True) # sort by 4th element which is score

table = [value for value in table if float(value[4]) >= 4.0]

# update html
current_index = open('index.html').read()

output_front = current_index[0:current_index.index("</tr>\n")]
output_middle = ""
output_end = current_index[current_index.index("</table>"):]

for line in table:
    # unpack the data

    restaurant_name, focus, drink_focus, diet, score = line
    restaurant_name = restaurant_name.lower()
    focus = focus.lower()
    score = float(score)

    print(line)

    # update data in output
    output_middle = output_middle + "\n\t\t<tr>"
    output_middle = output_middle + "\n\t\t\t<td>" + str(score) + "</td>"
    if len(diet) > 0: # vegan or veg friendly
        output_middle = output_middle + "\n\t\t\t<td><i>" + restaurant_name + "</i></td>"
        output_middle = output_middle + "\n\t\t\t<td><i>" + focus + "</i></td>"
    else:
        output_middle = output_middle + "\n\t\t\t<td>" + restaurant_name + "</td>"
        output_middle = output_middle + "\n\t\t\t<td>" + focus + "</td>"
    output_middle = output_middle + "\n\t\t</tr>"
    

output_file = open("index.html", "w")
output_file.write(output_front + "</tr>" + output_middle + "\n\t" + output_end)
output_file.close()

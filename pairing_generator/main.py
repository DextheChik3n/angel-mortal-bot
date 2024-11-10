import csv
import pandas

participants = pandas.read_csv("participants.csv")
unpicked_df = participants.loc[participants['Picked'] == False]
unpicked_count = len(unpicked_df)

write_fields = ['Player', 'Angel']
write_rows = []

month = 'November'

while unpicked_count > 0:
    mortal = unpicked_df.sample(1)
    mortal_group = mortal['Group'].iloc[0]

    eligible_angels = unpicked_df.loc[unpicked_df['Group'] != mortal_group]
    eligible_angels_count = len(eligible_angels)

    # if eligible_angels_count == 0:
    #     print("No eligible angels available for pairing.")
    #     break

    angel = eligible_angels.sample(1)
    mortal_handle = mortal['Telegram Handle'].iloc[0]
    angel_handle = angel['Telegram Handle'].iloc[0]
    write_rows.append([mortal_handle, angel_handle])

    participants.loc[participants['Telegram Handle'] == mortal_handle, 'Picked'] = True
    participants.loc[participants['Telegram Handle'] == angel_handle, 'Picked'] = True

    unpicked_df = participants.loc[participants['Picked'] == False]
    unpicked_count = len(unpicked_df)


print(write_rows)
with open(f'{month} Pairings.csv', 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(write_fields)
    write.writerows(write_rows)

# Tribecar Locater

Tribecar Locater is python app that will traverse through tribecar and churn out all the phv cars and locations in an excelsheet.

## Description

For tribecar users, it can be quite frustrating when one needs to locate cars that are most fuel efficient as the search system does not have any filter for that.

Users often need to go thru every single car in the system to locate the exact type of car and address.

This project seeks to address that problem.

Upon running the the program, it will first load all the cars and store the urls to each car in an array.

After all urls have been found, it will go to each car page and get the car name and address.

Once every car has been searched, the car and addresses will be generated in
an excel sheet directly in the same folder as the program.

Took 320seconds to find 265 cars. Average search time of slightly more than a second for
each car.

## Installation

1. Ensure system have python3 and do a pip install
2. Ensure system have chrome installed

After that, run program directly from compiler, I use a visual studio code.

```bash
pip3 install -r requirement.txt
```

## How to use

1. type your tribecar email in username.send_keys("youremail@gmail.com")
2. type your password in password.send_keys("mysuperduperhardtocrackpassword")
3. click the play button or type python3 navPageSele.py to run the program

optional:

4. Look for end_date = str(date_1 + datetime.timedelta(days=21)) and replace 21 with number of days you want to search ahead. 21 means search 21 days from today. Note the most you can search and book ahead is around 30 days.

## Contributing

If you have any idea how to improve the search time, feel free to ping me.

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

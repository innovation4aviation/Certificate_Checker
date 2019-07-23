# Certificate_Checker
This code will allow you to compare information from two different sources: a txt file and a json file.
The objective is to know which information must be absolutely verified with precision and which information is correct.

You will find:
- the python document with the code
- two txt files to test the code
- two jpg files to see the real certificate. The txt files are created by reading these two jpg files
- a json file that represents the database with the certificate information

#Test 1

Input : json_file = "test.json" , row_nb = 1, txt_file = "test2"

Output : [[['UNITEDSTATESOFAMERICA', 'UNITEDSTATESOFAMERICA', 100.0], ['N12345', 'NI2345', 90.0], ['NONE', 'NONE', 100.0], ['19960129', '1996-01-29', 100], ['6969', '6969', 100.0], ['CESSNA', 'CESSNA', 100.0], ['1960', '1996', 0.0]], 84.28571428571429]
You should verify the year of build.

#Test 2

Input : json_file = "test.json" , row_nb = 0, txt_file = "test"

Output : [[['UNITEDSTATESOFAMERICA', 'UNITEDSTATESOFAMERICA', 100.0], ['N2631A', 'N2631A', 100.0], ['NONE', 'NONE', 100.0], ['19951010', 'R101995M', 72.22222222222221], ['22903', '22903', 100.0], ['PIPER', 'PIPER', 100.0], ['1960', '2290', 0.0]], 81.74603174603173]
You should verify the date of registry.
You should verify the year of build.

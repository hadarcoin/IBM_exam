# IBM_exam
Hey,

import pandas | numpy | os | seaborn* | matplotlib*
* no necessary

Please ensure you have the following in the current python file folder:
1 - people.csv
2 - phonecalls folder (includes all CSV files)

I created an interactive file that contains parameters and weights.
Each one of the suspects get a final score range ("0" for innocent and "100" for Probably a terrorist).

The user can control and change those parameter values and their weights.

outputs:
1. people_chance_terror.csv --> contains the summary column "chance_of_a_terrorist"
	1.1 I included many new features in the file.
2. phonecalls_match.csv --> This table unites all rows from all the files in the phonecalls directory.
	The data was filtered according to "chance_of_a_terrorist" (with a benchmark score higher than '65').

If I had more time I would add Seaborn graphs and show some informative information combines several parameters.
More time would also allow me to create this file as a scheduled task, as asked.

Thanks
Hadar

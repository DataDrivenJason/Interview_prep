# Introduction
To whom this may concern reading this (potentially future employers), this is just a file I made for interview prep using SQL quering and generated data I made in python. 

# SQL, Boeing and Tariffs 
This query was actually submitted last, but I thought I’d include it first as it's the most interesting and valuable. This simple query examined which aircraft parts are manufactured in the USA and how tariffs could affect the cost function of the fleet. Even though the 1997 Commercial Aircraft Agreement is supposed to protect against tariffs on aircraft parts and sales, nothing seems certain anymore. Therefore, this is useful information to have when considering alternative suppliers who can offer fixed prices, allowing this to be aligned with routine maintenance schedules.

# SQL code 
The queries I used for this project allowed me to answer questions such as which aircraft is most commonly used in the fleet, as well as which aircraft models were most likely to be delayed (Answer: Embraer E190, Boeing 737, and Boeing 737 MAX). I also analyzed how many flights arrived in Dublin using a CASE WHEN function, which allowed me to calculate that Dublin accounted for approximately 8.7% of all flights.

Additionally, I calculated the average flight time for flights where the "status" column was not equal to "delayed". Conversely, I also determined the average delay time for flights marked as delayed. In this dataset, Lisbon had the highest average delay, followed by Paris (please let me know if this aligns with actual performance data).

## Table joins 
I used a LEFT JOIN to calculate which aircraft model in the fleet was the most reliable. In this dataset, the most reliable aircraft was the Embraer E190, followed by the Airbus A320. This analysis also indicated that the Boeing 737 MAX was the most likely to cause delays.


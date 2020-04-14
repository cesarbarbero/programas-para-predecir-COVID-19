# programas-para-predecir-COVID-19
The purpose of this repository is to make public the programs used to adjust COVID-19 mortality data in Argentina.
The object is to make the code (Python 3.7) public to allow verification of the capacity of the programs and test suite to ensure the correction of errors and the possibility of improvements.
The program for the adjustment proposed in the article was generated:
https://www.medrxiv.org/content/10.1101/2020.03.27.20043752v1
Featured on the site:
https://covid19.healthdata.org/united-states-of-america

METHOD
Raw mortality data from COVID-19 (deaths per day) are adjusted with a Gaussian integral function (func). The function was obtained by symbolically integrating (Euler) the Gaussian function and adding an integration constant (norm).
Data (Y) is entered from CSV files as deaths per day that are added to obtain the sum of deaths for that day.
Data (X) is entered as the number of days from an initial date (March 9 for Argentina) in which there were still no deaths.
The program generates an adjustment graph and prediction of the evolution of the total number of deaths.
It also generates a graph that shows the number of deaths per day to detect the moment of maximum mortality and graphs the experimental data. As can be seen, the daily death toll presents a lot of sampling variation. Initially, the daily death toll was adjusted and gives similar results but with worse statistics given the variation.
In addition, the number of infected persons is predicted by dividing the number of deaths with the mortality rate. Two scenarios are proposed: a) low mortality (South Korea) and high mortality (Italy).
The written output contains the input details and relevant parameters:
- Total number of deaths
- Day of maximum number of deaths
- Zero mortality day
- Maximum and minimum number of total infected.
The program: “Adjust COVID M with Gaussian integral ARG” was written in the IDE Spyder launched by Anaconda. The file: Mpordia.csv is used with data obtained by reading (¡) the daily reports of the nation's Ministry of Health (Argentina).

TEST SUITE
Since on the site:
https://covid19.healthdata.org/italy
The adjustments for different countries (and states of the USA) are shown. The results for Italy were used to test the program because the peak of deaths per day has passed, so it is possible to check the predictive capacity of the adjustment.
It is tested with two data files. One contains all the data ((ItaliaMd.csv, after the peak of deaths per day) and the other (ItaliaMd35.csv) contains the same amount of data as there is in Argentina.
The data was manually obtained from the site: https://covid19.healthdata.org/italy.
The heart code is the same, changing the graphics signs and the start day, etc.
It is called: “Fit COVID M with Gaussian integral ITALY”

USE
It is possible to use the program for any country or jurisdiction for which there are data on deaths per day.

CORRECTIONS / SUGGESTIONS
As any Python programmer will be able to detect, the code is not elegant or concise since I have programmed in Z80 assemblers, Fortran, Basic, Pascal and now Python but I am a researcher in chemistry and I code by necessity, not professionally. The reason for using Python is the excellent “open source” calculation and graph libraries, not for the love of the language that seems idiosyncratic to me and I couldn't write without IDE.
I request that calculation errors be pointed out or, in the best tradition of open source, it is corrected and improved as desired, but I do not have time (I am teaching classes at the university remotely) to improve it.

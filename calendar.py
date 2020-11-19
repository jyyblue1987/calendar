import re
import copy

class Calendar:
    def __init__(self):
        self.month_dict = {}

    def parse_date(self, date_string):
        '''
        Extract the month, day, and year from a date string.  Acceptable formats are
          'Jour de la Révolution, 1792'  =>  month = 'Jour de la Révolution', day = None, year = 1792'
          '3/1/2020'                     =>  month = 3, day = 1, year = 2020
          '2 Lithe, 1418'                =>  month = '2 Lithe', day = None, year = 1418
          '2 Lithe 1418'                 =>  month = '2 Lithe', day = None, year = 1418
          'Sep 30, 2020'                 =>  month = 'Sep', day = 30, year = 2020
        The day and year are returned as ints, while the month is a string (as in 'Mar 1, 2020') or an int
        (as in 3/1/2020).
        '''
        date_string = date_string.replace(',', ' ').lstrip().rstrip()
        date_string = date_string.replace('/', ' ')
        # Unless you understand the following line you should experiment with this method until
        # you have a clear idea of what it does...
        p = re.compile(r'[ ]*(?P<month>[0-9]*[ ]*[\D ]+)[ ]*(?P<num1>[0-9]*)[ ]*(?P<num2>[0-9]*$)')
        match = p.match(date_string)
        if match:
            month = match.group('month').lstrip().rstrip()
            num1  = match.group('num1').lstrip().rstrip()
            num2  = match.group('num2').lstrip().rstrip()

            # Convert the month to an int if appropriate.
            if month.isdigit():
                month = int(month)

            if num1 and num2:  # Both day and year are present.
                day  = int(num1)
                year = int(num2)
            elif num1:         # Only one of day and year is present; we take it to be the year.
                day   = None
                year  = int(num1)
            else:
                day  = None    # Neither day or year is present (e.g., 'Midyear's Day').
                year = None

            return (month, day, year)
        else:
            # This branch indicates a malformed date string.
            raise ValueError(f'I cannot make sense of this date: {date_string}.')


    def is_leap_year(self, year):
        # Use this version for the Gregorian and French revolutionary calendars.
        pass


    def date_to_day_of_year(self, date_string):
        # Return the day of the year (int) given a date.
        #
        # This can be called with strings such as
        #   obj.date_to_day_of_year("Messidor, 14, 1789")
        # and
        #   obj.date_to_day_of_year("Midyear"s Day, 1418")
        # You need to determine the form by parsing the string.
        month, day, year = self.parse_date(date_string)

        month_dict = copy.deepcopy(self.month_dict)
        if self.is_leap_year(year) == False:
            del month_dict['Overlithe']
        
        total_days = 0
        for k,v in month_dict.items():
            if k == month:                
                if day == None:
                    total_days += 1
                else:
                    total_days += day
                break
            
            total_days += v
             
        return total_days, year

    def day_of_year_to_date(self, day_of_year, year):
        '''
        Convert day of year to date.
        '''
        day_of_year = int(day_of_year)
        total_days = 0   

        shire_month_dict = copy.deepcopy(self.shire_month_dict)
        if self.is_leap_year(year) == False:
            shire_month_dict['Overlithe']

        for k,v in shire_month_dict.items():
            if total_days < day_of_year and day_of_year <= total_days + int(v):
                sub = day_of_year - total_days
               
                return k, sub, year

            total_days += int(v)
            
        return "", 0, 0

#---------------------------------------------------------------------------------------------------------------

class Gregorian_Calendar(Calendar):
    def __init__(self):
        # Days of the week: 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'
        # Months: 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        pass


    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Messidor, 14, 1789")
        # and
        #   obj.date_to_weekday("Midyear"s Day, 1418")
        # You need to determine the form by parsing the string.
        pass

#---------------------------------------------------------------------------------------------------------------

class Shire_Calendar(Calendar):
    def __init__(self):
        # Days of the week: "Sterday", "Sunday", "Monday", "Trewsday", "Hensday", "Mersday", "Highday"
        # Months and special days: "2 Yule", "Afteryule", "Solmath", "Rethe", "Astron", "Thrimidge", "Forelithe",
        # "1 Lithe", "Midyear"s Day", "Overlithe", "2 Lithe", "Afterlithe", "Wedmath", "Halimath", "Winterfilth",
        # "Blotmath", "Foreyule", "1 Yule"
        self.month_dict = {  
                "2 Yule":1, 
                "Afteryule": 30,
                "Solmath": 30,
                "Rethe": 30,
                "Astron": 30,
                "Thrimidge": 30,
                "Forelithe": 30,
                "1 Lithe": 1,
                "Midyear's Day": 1, 
                "Overlithe": 1,
                "2 Lithe": 1,
                "Afterlithe": 30,
                "Wedmath": 30,
                "Halimath": 30,
                "Winterfilth": 30,
                "Blotmath": 30,
                "Foreyule": 30,
                "1 Yule": 1,
        }
        


    def is_leap_year(self, year):
        if year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True;
        else:
            return False;
        
    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Midyear"s Day, 1418")
        #   obj.date_to_weekday("Solmath 19, 1418")
        # You need to determine the form by parsing the string.
        pass

#---------------------------------------------------------------------------------------------------------------

# Keep the non-ASCII characters in the strings and the class name.
class Calendrier_Républicain(Calendar):
    def __init__(self):
        # Days of the week: "primidi", "duodi", "tridi", "quartidi", "quintidi",
        #                   "sextidi", "septidi", "octidi", "nonidi", "décadi"
        # Months : "Vendémiaire", "Brumaire", "Frimaire", "Nivôse", "Pluviôse", "Ventôse",
        #          "Germinal", "Floréal", "Prairial", "Messidor", "Thermidor", "Fructidor",
        # Days at end of year: "Jour de la vertu", "Jour du génie", "Jour du travail",
        #            "Jour de l'opinion", "Jour des récompenses", "Jour de la Révolution" (leap-year only)
        #
        pass


    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Messidor, 14, 1789")
        #   obj.date_to_weekday("Jour des récompenses, 14, 1789")
        # You need to determine the form by parsing the string.
        pass

#---------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Tests go here.
    cal = Calendar()
    print(cal.parse_date('Aug 15, 2020'))
    print(cal.parse_date("Midyear's Day 1418"))
    print(cal.parse_date("  Overlithe  1418 "))
    print(cal.parse_date("3/1/2020"))
    print(cal.parse_date('bob bob 1'))
    # print(cal.parse_date('bob 1 bob'))

    shire = Shire_Calendar()
    assert not shire.is_leap_year(1400)
    # assert shire.date_to_day_of_year('1 Lithe 1418') == 180
    assert shire.date_to_day_of_year("Midyear's Day 1418") == (183, 1418)

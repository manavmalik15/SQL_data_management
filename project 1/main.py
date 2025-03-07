#
# header comment! Overview, name, etc.
# Manav Malik
# 654488575
# trafic cam data
#
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
#
"""
General Statistics:
Number of Red Light Cameras: 365
Number of Speed Cameras: 184
Number of Red Light Camera Violation Entries: 998,470
Number of Speed Camera Violation Entries: 408,256
Range of Dates in the Database: 2014-07-01 - 2024-11-28
Total Number of Red Light Camera Violations: 6,216,244
Total Number of Speed Camera Violations: 16,767,367

"""
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")    # red light cam
    row = dbCursor.fetchone()
    print("  Number of Red Light Cameras:", f"{row[0]:,}")

    
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras;")    # speed cam
    row = dbCursor.fetchone()
    print("  Number of Speed Cameras:", f"{row[0]:,}")


    dbCursor.execute("SELECT COUNT(*) FROM RedViolations;")    # NUM red voilation
    row = dbCursor.fetchone()
    print("  Number of Red Light Camera Violation Entries:", f"{row[0]:,}")

    
    dbCursor.execute("SELECT COUNT(*) FROM SpeedViolations;")    #  NUM Speed voilation
    row = dbCursor.fetchone()
    print("  Number of Speed Camera Violation Entries:", f"{row[0]:,}")


    dbCursor.execute("SELECT Violation_Date FROM SpeedViolations LIMIT 1;")    # DATES
    row = dbCursor.fetchone()
    print("  Range of Dates in the Database:", row[0], end="")
    dbCursor.execute("SELECT Violation_Date FROM SpeedViolations ORDER BY Violation_Date DESC LIMIT 1;")    # DATES
    row = dbCursor.fetchone()
    print(" -", row[0])


    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations;")    # total red
    row = dbCursor.fetchone()
    print("  Total Number of Red Light Camera Violations:", f"{row[0]:,}")


    dbCursor.execute("SELECT SUM(Num_Violations) FROM SpeedViolations;")    # total speed
    row = dbCursor.fetchone()
    print("  Total Number of Speed Camera Violations:", f"{row[0]:,}")


# option 1

def find_intersection_by_name(dbConn):
    dbCursor = dbConn.cursor()
    val = input("\nEnter the name of the intersection to find (wildcards _ and % allowed): ")
    query = "SELECT Intersection_ID, Intersection FROM Intersections WHERE Intersection LIKE ? ORDER BY Intersection;"
    
    dbCursor.execute(query, (val,))
    results = dbCursor.fetchall()

# showing the results

    if results:
        for row in results:
            print(f"{row[0]} : {row[1]}")
            #print(row)
    else:
        print("No intersections matching that name were found.")

# option 2

def find_all_cameras_at_intersection(dbConn):
    dbCursor = dbConn.cursor()
    val = input("\nEnter the name of the intersection (no wildcards allowed): ")



# the red inforation
    redquery = """
    SELECT Camera_ID, Address FROM Intersections 
    INNER JOIN RedCameras ON Intersections.Intersection_ID = RedCameras.Intersection_ID
    WHERE Intersection = ?
    ORDER BY Camera_ID;
    """

    dbCursor.execute(redquery, (val,))
    results = dbCursor.fetchall()

# showing the results


    if results:
        print("\nRed Light Cameras:")
        for row in results:
            print(f"   {row[0]} : {row[1]}")
    else:
        print("\nNo red light cameras found at that intersection.")

              
# the speed inforation


    speedquery = """
    SELECT Camera_ID, Address FROM Intersections 
    INNER JOIN SpeedCameras ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    WHERE Intersection = ?
    ORDER BY Camera_ID;
    """
    
    dbCursor.execute(speedquery, (val,))
    results = dbCursor.fetchall()

    if results:
        print("Speed Cameras:")
        for row in results:
            print(f"   {row[0]} : {row[1]}")
    else:
        print("\nNo speed cameras found at that intersection.")
        



# option 3

def percentage_of_violations_by_date(dbConn):
    dbCursor = dbConn.cursor()
    val = input("\nEnter the date that you would like to look at (format should be YYYY-MM-DD): ")


# the red inforation


    redquery1 = """
    SELECT SUM(Num_Violations) FROM RedViolations 
    WHERE Violation_Date = ?;
    """

    dbCursor.execute(redquery1, (val,))
    red = dbCursor.fetchone()[0] or 0

    redquery2 = """
    SELECT SUM(Num_Violations) FROM SpeedViolations 
    WHERE Violation_Date = ?;
    """

    dbCursor.execute(redquery2, (val,))
    speed = dbCursor.fetchone()[0] or 0

    

    total = red + speed;

# showing the results


    if total > 0:
        print(f"Number of Red Light Violations: {red:,} ({(red / total) * 100:.3f}%)")
        print(f"Number of Speed Violations: {speed:,} ({(speed / total) * 100:.3f}%)")
        print(f"Total Number of Violations: {total:,}")
    else:
        print("No violations on record for that date.")

# option 4

def number_of_cameras_at_each_intersection(dbCursor):
    dbCursor = dbConn.cursor()

    # Total red
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    total_red = dbCursor.fetchone()[0]

    # Total speed cameras
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras;")
    total_speed = dbCursor.fetchone()[0]

# the red inforation

    red_query = """
    SELECT Intersections.Intersection, Intersections.Intersection_ID, COUNT(RedCameras.Camera_ID) AS c 
    FROM Intersections INNER JOIN RedCameras ON Intersections.Intersection_ID = RedCameras.Intersection_ID
    GROUP BY Intersections.Intersection_ID
    ORDER BY c DESC;
    """
    dbCursor.execute(red_query)
    red_result = dbCursor.fetchall()
        
# the speed inforation


    speed_query = """
    SELECT Intersections.Intersection, Intersections.Intersection_ID, COUNT(SpeedCameras.Camera_ID) AS c 
    FROM Intersections INNER JOIN SpeedCameras ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    GROUP BY Intersections.Intersection_ID
    ORDER BY c DESC;
    """
    dbCursor.execute(speed_query)
    speed_result = dbCursor.fetchall()

# showing the results


    print("\nNumber of Red Light Cameras at Each Intersection")
    for row in red_result:
        intersection, intersection_id, count = row
        percentage = (count / total_red) * 100
        print(f"    {intersection} ({intersection_id}) : {count} ({percentage:.3f}%)")

    print("\nNumber of Speed Cameras at Each Intersection")
    for row in speed_result:
        intersection, intersection_id, count = row
        percentage = (count / total_speed) * 100
        print(f"    {intersection} ({intersection_id}) : {count} ({percentage:.3f}%)")


# option 5
        
def number_of_violations_at_intersection_given_year(dbConn):
    dbCursor = dbConn.cursor()
    year = input("\nEnter the year that you would like to analyze: ")

    dbCursor.execute("""SELECT SUM(Num_Violations) FROM RedViolations WHERE strftime('%Y', Violation_Date) = ?;""", (year,))
    total_red = dbCursor.fetchone()[0] or 0  # error case

    dbCursor.execute("""SELECT SUM(Num_Violations) FROM SpeedViolations WHERE strftime('%Y', Violation_Date) = ?;""", (year,))
    total_speed = dbCursor.fetchone()[0] or 0

# the red inforation


    dbCursor.execute(""" SELECT Intersections.Intersection, Intersections.Intersection_ID, SUM(RedViolations.Num_Violations) AS total 
    FROM RedViolations INNER JOIN RedCameras ON RedViolations.Camera_ID = RedCameras.Camera_ID INNER JOIN Intersections ON RedCameras.Intersection_ID = Intersections.Intersection_ID
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY Intersections.Intersection_ID
    ORDER BY total DESC; """, (year,))
    red_results = dbCursor.fetchall()

    dbCursor.execute("""
    SELECT Intersections.Intersection, Intersections.Intersection_ID, SUM(SpeedViolations.Num_Violations) AS total 
    FROM SpeedViolations INNER JOIN SpeedCameras ON SpeedViolations.Camera_ID = SpeedCameras.Camera_ID INNER JOIN Intersections ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY Intersections.Intersection_ID
    ORDER BY total DESC;
    """, (year,))
    speed_results = dbCursor.fetchall()

# showing the results


    print(f"\nNumber of Red Light Violations at Each Intersection for {year}")
    if total_red > 0 :
        for intersection, intersection_id, count in red_results:
            percentage = (count / total_red) * 100
            print(f"  {intersection} ({intersection_id}) : {count:,} ({percentage:.3f}%)")
        print(f"Total Red Light Violations in {year} : {total_red:,}")
    else:
        print("No red light violations on record for that year.")

    print(f"\nNumber of Speed Violations at Each Intersection for {year}")
    if total_speed > 0 :
        for intersection, intersection_id, count in speed_results:
            percentage = (count / total_speed) * 100
            print(f"  {intersection} ({intersection_id}) : {count:,} ({percentage:.3f}%)")
        print(f"Total Speed Violations in {year} : {total_speed:,}")
    else:
        print("No speed violations on record for that year.")

# option 6
def number_of_violations_by_year_given_camera_id(dbConn):
    dbCursor = dbConn.cursor()

    camera_id = input("\nEnter a camera ID: ").strip()

    # Query for red light violations
    red_query = """
    SELECT strftime('%Y', Violation_Date) AS year, SUM(Num_Violations) 
    FROM RedViolations 
    WHERE Camera_ID = ?
    GROUP BY year
    ORDER BY year;
    """
    dbCursor.execute(red_query, (camera_id,))
    red_results = dbCursor.fetchall()

    # If no results in RedViolations, query SpeedViolations
    if not red_results:
        speed_query = """
        SELECT strftime('%Y', Violation_Date) AS year, SUM(Num_Violations) 
        FROM SpeedViolations 
        WHERE Camera_ID = ?
        GROUP BY year
        ORDER BY year;
        """
        dbCursor.execute(speed_query, (camera_id,))
        speed_results = dbCursor.fetchall()
    else:
        speed_results = []
    
    if red_results:
        results = red_results
    else:
        results = speed_results

    if not results:
        print(f"No cameras matching that ID were found in the database.")
        return
     
# showing the results


    print(f"Yearly Violations for Camera {camera_id}")
    years = []
    violations = []
    for year, count in results:
        years.append(year)
        violations.append(count)
        print(f"{year} : {count:,}")

    plot = input("\nPlot? (y/n) ")
    if plot == 'y':
        plt.plot(years, violations)
        plt.title(f"Yearly voilations for Camera {camera_id}")
        plt.xlabel("Years")
        plt.ylabel("Number of Voilations")
        plt.show()



# option 7


def number_of_violations_by_month_given_camera_id_and_year(dbConn):
    dbCursor = dbConn.cursor()
    camera_id = input("\nEnter a camera ID: ").strip()

    # Query for red light violations
    red_query = """
    SELECT strftime('%m', Violation_Date) AS month, 
    strftime('%Y', Violation_Date) AS year,
    SUM(Num_Violations) AS total_violations
    FROM RedViolations
    WHERE Camera_ID = ?
    GROUP BY month, year
    ORDER BY year;
    """
    dbCursor.execute(red_query, (camera_id,))
    red_results = dbCursor.fetchall()
    
    # If no results in RedViolations, query SpeedViolations
    if not red_results:
        speed_query = """
        SELECT strftime('%m', Violation_Date) AS month, 
        strftime('%Y', Violation_Date) AS year,
        SUM(Num_Violations) AS total_violations
        FROM SpeedViolations
        WHERE Camera_ID = ?
        GROUP BY month, year
        ORDER BY year;
        """
        dbCursor.execute(speed_query, (camera_id,))
        speed_results = dbCursor.fetchall()
    else:
        speed_results = []
    
    
    
    
    
# showing the results


    
    if red_results:
        results = red_results
    else:
        results = speed_results

    if not results:
        print(f"No cameras matching that ID were found in the database.")
        return
    
    
    
    year_selected = input("Enter a year: ").strip()
    
    print(f"Monthly Violations for Camera {camera_id} in {year_selected}")
    months = []
    violations = []
    for month, year, count in results:
        if year == year_selected:
            months.append(month)
            violations.append(count)
            print(f"{month}/{year} : {count:,}")

    plot = input("\nPlot? (y/n) ")
    if plot == 'y':
        plt.plot(months, violations)
        plt.title(f"Monthly voilations for Camera {camera_id} ({year})")
        plt.xlabel("Month")
        plt.ylabel("Number of Voilations")
        plt.show()
    
    
    
    


# option 8


def compare_red_light_and_speed_violations_given_year(dbConn):
    dbCursor = dbConn.cursor()
    year = input("\nEnter a year: ")

# the red inforation


    red_query = """
    SELECT strftime('%Y-%m-%d', Violation_Date) AS date, SUM(Num_Violations) AS total_violations
    FROM RedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date ASC;
    """
    dbCursor.execute(red_query, (year,))
    red_results = dbCursor.fetchall()
        
# the speed inforation


    speed_query = """
    SELECT strftime('%Y-%m-%d', Violation_Date) AS date, SUM(Num_Violations) AS total_violations
    FROM SpeedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date ASC;
    """
    dbCursor.execute(speed_query, (year,))
    speed_results = dbCursor.fetchall()
    
# showing the results


# showing the results


    
    print("Red Light Violations:")
    for date, count in red_results[:5] + red_results[-5:]:
        print(f"{date} {count:}")

    print("Speed Violations:")
    for date, count in speed_results[:5] + speed_results[-5:]:
        print(f"{date} {count:}")


    # list to dict
    red_dict = dict(red_results)
    speed_dict = dict(speed_results)

    start_date = datetime(int(year), 1, 1)
    end_date = datetime(int(year), 12, 31)
    date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

    red_daily = [(date, red_dict.get(date, 0)) for date in date_list]
    speed_daily = [(date, speed_dict.get(date, 0)) for date in date_list]


    plot = input("\nPlot? (y/n) ")
    if plot == 'y':
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dict(red_daily).keys()]
        red_violations = list(dict(red_daily).values())
        speed_violations = list(dict(speed_daily).values())


        day_numbers = [(date - dates[0]).days for date in dates]

        plt.plot(day_numbers, red_violations, label="Red Light", color="red")
        plt.plot(day_numbers, speed_violations, label="Speed", color="orange")

        plt.xlabel("Day of the Year")
        plt.ylabel("Number of Violations")
        plt.title(f"Violations Each Day of {year}")

        plt.xticks(range(0, len(day_numbers), 50))

        plt.show()




# option 9

def find_cameras_on_street(dbConn):
    dbCursor = dbConn.cursor()
    street_name = input("\nEnter a street name: ")
    
# the red inforation


    red_query = """
    SELECT Camera_ID, Address, Latitude, Longitude
    FROM RedCameras
    WHERE Address LIKE ?
    ORDER BY Camera_ID ASC;
    """
    dbCursor.execute(red_query, ('%' + street_name + '%',))
    red_cameras = dbCursor.fetchall()
        
# the speed inforation


    speed_query = """
    SELECT Camera_ID, Address, Latitude, Longitude
    FROM SpeedCameras
    WHERE Address LIKE ?
    ORDER BY Camera_ID ASC;
    """
    dbCursor.execute(speed_query, ('%' + street_name + '%',))
    speed_cameras = dbCursor.fetchall()
    
    if not red_cameras and not speed_cameras:
        print(f"There are no cameras located on that street.")
        return
    
    print(f"\nList of Cameras Located on Street: {street_name}")
    
    
    
# showing the results


    
    print("  Red Light Cameras:")
    if red_cameras:
        for cam_id, address, lat, lon in red_cameras:
            print(f"     {cam_id} : {address} ({lat}, {lon})")
    
    
    print("  Speed Cameras:")
    if speed_cameras:
        for cam_id, address, lat, lon in speed_cameras:
            print(f"     {cam_id} : {address} ({lat}, {lon})")
    
    plot = input("\nPlot? (y/n) ")
    if plot.lower() == 'y':
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
        
        plt.imshow(image, extent=xydims)
        plt.title(f"Cameras on Street: {street_name}")
        
        x_red = [cam[3] for cam in red_cameras]
        y_red = [cam[2] for cam in red_cameras]
        x_speed = [cam[3] for cam in speed_cameras]
        y_speed = [cam[2] for cam in speed_cameras]


        plt.scatter(x_red, y_red, c='red', label='Red Light Cameras')
        plt.scatter(x_speed, y_speed, c='orange', label='Speed Cameras')
        
        for cam_id, _ , lat, lon in red_cameras + speed_cameras:
            plt.annotate(str(cam_id), (lon, lat), fontsize=8, ha='right')
        
        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()
    
    
##################################################################
#
# main
#
dbConn = sqlite3.connect('chicago-traffic-cameras.db')

print("Project 1: Chicago Traffic Camera Analysis")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the Chicago traffic camera database.")
print()
print_stats(dbConn)



# Main loop

while True:
    print("\nSelect a menu option: ")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")

    choice = input("Your choice --> ")  # input

    # calling the function
    
    if choice == '1':
        find_intersection_by_name(dbConn)
        
    elif choice == '2':
        find_all_cameras_at_intersection(dbConn)
        
    elif choice == '3':
        percentage_of_violations_by_date(dbConn)
        
    elif choice == '4':
        number_of_cameras_at_each_intersection(dbConn)
        
    elif choice == '5':
        number_of_violations_at_intersection_given_year(dbConn)
        
    elif choice == '6':
        number_of_violations_by_year_given_camera_id(dbConn)
        
    elif choice == '7':
        number_of_violations_by_month_given_camera_id_and_year(dbConn)
        
    elif choice == '8':
        compare_red_light_and_speed_violations_given_year(dbConn)
        
    elif choice == '9':
        find_cameras_on_street(dbConn)
        
    elif choice == 'x':
        break
    else:
        print("Error, unknown command, try again...")



print("Exiting program.")
#
# done
#

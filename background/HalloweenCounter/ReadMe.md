Halloween Counter:

This script is used to count the people you meet on Halloween. I'll describe the structure now:
   1. There is a "Person" class, which contains information about a person's
      name (first, last), age, gender, what time they visited, number of candy
	  pieces received, and what their halloween costum was.
   2. There is a "Group" class, which is simply a collection of "Person" objects.
      The group does NOT need to all have arrived at the same time, but it is likely.
   3. There is a "ManyGroup" (poorly named) class. This class is a collection of
      groups. Essentially, this class becomes the "day" of Halloween, and you can
	  enter how many people arrive when they arrive at your house for sweets.
	     i.e. 5 kids approach your house - you can enter a "5" during data
		      collection and it will "create" 5 "Person" objects, and those Person
			  objects are stored within a "Group" object.
			  
   NOTE: ONLY the time at which people/groups arrived is tracked - there is NO way
         for users to enter names, ages, genders, etc. into the program to track.
		 This script is VERY MINIMAL, however it presents the opportunity to collect
		 significant amounts of data if you desired. HOWEVER, let's be honest - you
		 aren't going to get names and ages, and maybe not genders - the only viably
		 trackable statistics is how many people and the time at which they visited.

		 
To run this script, type "python HalloweenCounter.py"


Written by CMJ (chasem.juneau@gmail.com), 10/2018. Feel free to contact with any questions.
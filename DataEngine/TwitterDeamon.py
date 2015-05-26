#!/usr/bin/env python
 
import tweepy, time, sys
import MySQLdb as mdb
from pygeocoder import Geocoder, GeocoderError
import calendar

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'iWMygTF8nk4PbqrcRtwK82vb6'
CONSUMER_SECRET = 'G46hb9lQsSJDXVshMvpTa4NxxhXh8PQ1fbGvScsfKWizsesK3C'
ACCESS_KEY = '2521309568-a2WnyZ6vFVgmvYrPDmEOn71lGm4GvWnrE8sU4xX'
ACCESS_SECRET = '6Prl3r01rYNXJuFNIUJmy4f1kx4pLXjBWTDF6gMCWr8R7'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# connect to database
con = mdb.connect('localhost', 'root', 'root', 'feedmapdb')

#############
# Functions #
#############

def writeToDB(location, profile, profilepic, favourites, retweets, body, feedId, feedCreationTimestamp, source):
	try:
		result = Geocoder.geocode(location)
		(lat, lon) = result[0].coordinates
		cur.execute( "INSERT INTO feeds(lon, lat, profile, profilepic, favourites, retweets, body, location, feedID, feedCreationTimestamp, feedInsertionTimestamp, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)",  (str(lon), str(lat), profile, profilepic, favourites, retweets, body, location, feedId, feedCreationTimestamp, source))
	except GeocoderError: 
		print "The location given by twitter returns error when given to Geocoder"



with con:
	con.autocommit(True) 
	# Creates table if it doesn't exist
	cur = con.cursor()
	#cur.execute("DROP TABLE IF EXISTS feeds")
	cur.execute( "CREATE TABLE IF NOT EXISTS feeds (id INT PRIMARY KEY AUTO_INCREMENT, lon VARCHAR(255) NOT NULL, lat VARCHAR(255) NOT NULL, profile VARCHAR(255) NOT NULL, profilepic TEXT NOT NULL, favourites VARCHAR(255) NOT NULL, retweets VARCHAR(255) NOT NULL, body TEXT NOT NULL, location VARCHAR(255) NOT NULL, feedID VARCHAR(255) NOT NULL, feedCreationTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, feedInsertionTimestamp TIMESTAMP NOT NULL, source VARCHAR(255) NOT NULL)" )

	# List of cities
	cityList = ["Sukkur", "Larkana", "Rahim Yar Khan", "Gujrat", "Mardan", "Kasur", "Mingora", "Wah", "Dera Ghazi Khan", 
	"Sahiwal", "Nawabshah", "Mingaora", "Okara", "Mirpur Khas", "Chiniot", "Kamoke", "Sadiqabad", "Burewala", "Jacobabad", 
	"Muzaffargarh", "Muridke", "Jhelum", "Shikarpur", "Khanpur", "Khanewal", "Hafizabad", "Kohat", "Khuzdar", "Dadu", "Gojra", 
	"Mandi Bahauddin", "Daska", "Pakpattan", "Bahawalnagar", "Tando Adam", "Khairpur", "Chishtian Mandi", "Abbottabad", "Jamshoro", 
	"Jaranwala", "Ahmadpur East", "Vihari", "Kamalia", "Kot Addu", "Khushab", "Wazirabad", "Dera Ismail Khan", "Chakwal", "Swabi", 
	"Lodhran", "Nowshera", "Charsadda", "Jalalpur Jattan", "Mianwali", "Chaman", "Hasilpur", "Arifwala", "Chichawatni", "Bhakkar", 
	"Kharian", "Kambar", "Moro", "Mian Channun", "Turbat", "Shahdadkot", "Bhalwal", "Dipalpur", "Badin", "Pano Aqil", "Kotri", 
	"Tando Muhammad Khan", "Harunabad", "Pattoki", "Kahror Pakka", "Attock", "Gujar Khan", "Chuhar Kana", "Toba Tek Singh", "Narowal", 
	"Shahdadpur", "Shabqadar", "Mansehra", "Shujaabad", "Haveli", "Mailsi", "Ghotki", "Sibi", "Jampur", "Sambrial", "Sanghar", "Kabirwala", 
	"Chunian", "Haripur", "Nankana Sahib", "Pasrur", "Gwadar", "Rajanpur", "Rohri", "Zhob", "Matli", "Rabwah", "Mirpur Mathelo", "Bannu", 
	"Dullewala", "Hala", "Ratodero", "Jatoi", "Jauharabad", "Dina", "Bat Khela", "Kot Radha Kishan", "Kahna Nau", "Mustafabad", "Hasan Abdal", 
	"Talagang", "Taunsa", "Thatta", "Sarai Alamgir", "Usta Muhammad", "Kamra", "Umarkot", "Basirpur", "Sehwan", "Fort Abbas", "Havelian", "Dinga", 
	"Khalabat", "Badah", "Tank", "Tandlianwala", "Chak Azam Sahu", "Loralai", "Jalalpur Pirwala", "Pabbi", "Chak Jhumra", "Renala Khurd", "Risalpur", 
	"Lakki Marwat", "Topi", "Hangu", "Chitral", "Kundian", "Khurianwala", "Mehrabpur", "Pindi Bhattian", "Narang", "Malakwal", "Thul", "Pindi Gheb", 
	"Zahir Pir", "Dunyapur", "Gambat", "Kashmor", "Alipur", "Naudero", "Pasni", "Sukheke", "Setharja", "Khewra", "Karak", "Mamu Kanjan", "Sharqpur", 
	"Digri", "Bhera", "Sakrand", "Tando Jam", "Raiwind", "Lalian", "Kharan", "Mehar", "Khangah Dogran", "Khairpur Nathan Shah", "Dir", "Ghauspur", 
	"Tangi", "Utmanzai", "Minchinabad", "Garh Maharaja", "Mastung", "Khipro", "Fazalpur", "Kunjah", "Jhawarian", "Nasirabad", "Nushki", "Sujawal", 
	"Sita Road", "Dijkot", "Sillanwali", "Kandiaro", "Zaida", "Kunri", "Kalat", "Mitha Tiwana", "Daud Khel", "Liaqatabad", "Hazro", "Dunga Bunga", 
	"Amangarh", "Kot Diji", "Kalur Kot", "Murree", "Faqirwali", "Ahmadpur Sial", "Phalia", "Yazman", "Raja Jang", "Samasatta", "Warburton", "Pishin", 
	"Kamir", "Uch", "Chawinda", "Ubauro", "Mithi", "Akora", "Zafarwal", "Kot Samaba", "Eminabad", "Kahuta", "Ranipur", "Kulachi", "Hingorja", "Naukot", 
	"Pind Dadan Khan", "Kanganpur", "Faruka", "Kotli Loharan","Shahpur Chakar", "Talhar", "Qadirpur Ran", "Bela", "Muzaffarabad", "Khangarh", "Sarai Naurang", 
	"Gharo", "Bhit Shah", "Matiari", "Warah", "Lachi", "Baddomalhi", "Jand", "Fatehpur", "Dera Bugti", "Naushahro Firoz", "Dajal", "Isa Khel", "Daur", 
	"Bhopalwala", "Paharpur", "Bhan", "Mach", "Radhan", "Uthal", "Kaleke", "Jiwani", "Johi", "Chor", "Tando Ghulam Ali", "Mangla", "Bhawana", "Jhol", 
	"Sodhra", "Kalabagh", "Sinjhoro", "Harnoli", "Sarai Sidhu", "Hunza", "Choa Saidan Shah", "Dhadar", "Darya Khan", "Garhi Yasin", "Madeji", "Dokri", 
	"Thano Bula Khan", "Dalbandin", "Daulatpur", "Bhag", "Rasulnagar", "Chak", "Baffa", "Garhi Khairo", "Lakhi", "Surab", "Rojhan", "Karachi", "Lahore", 
	"Faisalabad", "Rawalpindi", "Multan",	"Hyderabad", "Gujranwala", "Peshawar", "Sheikhupura", "Jhang", "Quetta", "Islamabad", "Bahawalpur", "Sargodha", 
	"Sialkot"]

	# Address of User so we can get all mentions
	mentionAddress = '@CevdetSyed'
	# Hashtags that we created that have special meaning to us e.g. hashtags of all polling station
	specialTags = ["#AzadiSquare","#karachi"]
	tagLocation= { "#AzadiSquare" : "Islamabad", "#karachi":"karachi"}
	# All of the keywords we are searching including all Tweets that mention us, all tweets that use our specialHashTags and 
	# all tweets that have an hashtag that we are interested in but we will need to be stricter with these
	hashTags = ["#AzadiDharna","#rigging","#pakathon", mentionAddress] + specialTags

	class TweepyListener(tweepy.StreamListener):
		def on_status(self, status):
			if ( 'RT @' in status.text ):
				print "Retweet, increment count of tweet by one\n"
			if ( status.user.screen_name == "ACompany007" ):
				print "Blacklisted User\n"
			else:
				try:	
				# Three different ways of collecting data therefore 
					# First way using special tags i.e. predefined tags for which we already know what the locations are 
					location = None
					for keyword in specialTags:
						if keyword.lower() in status.text.lower():
							location = tagLocation[keyword]

					if location is not None:
						writeToDB( str(location), str(status.user.screen_name), str(status.user.profile_image_url), str(0), str(0), str(status.text), str(status.id), status.created_at, 'twitter') 
						print "1- " + status.text + " - " + status.created_at.strftime("%B %d, %Y") + " - " + str(status.id) + " - " + location +" - "+ status.user.screen_name + " - " +status.user.profile_image_url + " \n"
						
					else: 
						# Second way is to search the text of the tweet for a known location
						for city in cityList:
							if city.lower() in status.text.lower():
								location = city

						if location is not None:

							writeToDB( str(location), str(status.user.screen_name), str(status.user.profile_image_url), str(0), str(0), str(status.text), str(status.id), status.created_at, 'twitter') 
							print "2- " + status.text + " - " + status.created_at.strftime("%B %d, %Y") + " - " + str(status.id) + " - " + location + " - " + status.user.screen_name + " - " + status.user.profile_image_url + "\n"
							
						else:
							# Third and final way is to attempt to grab the location from the JSON data sent by twitter 
							if status.user.location is not None:
	
								writeToDB( str(status.user.location), str(status.user.screen_name), str(status.user.profile_image_url), str(0), str(0), str(status.text), str(status.id), status.created_at, 'twitter') 
								print "3- " + status.text + " - " + status.created_at.strftime("%B %d, %Y") + " - " + str(status.id) + " - " + status.user.location + " - " + status.user.screen_name + " - " + status.user.profile_image_url + "\n"
							else:
								print "Could not get a valid location"
				except UnicodeEncodeError: 
					print "Rejected cause the feed body or profile name wasn't ascii\n"

		def on_error(self, status_code):
			print >> sys.stderr, "Encountered error with status code: " + str(status_code)

		def on_timeout(self):
			print >> sys.stderr, "Timeout..."
			return True

	htAPI = tweepy.streaming.Stream(auth, TweepyListener())
	htAPI.filter(track=hashTags)
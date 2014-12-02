import json  
import urllib2
import requests
import MySQLdb as mdb
from pygeocoder import Geocoder, GeocoderError

BASE_URL = "https://graph.facebook.com/"
ACCESS_TOKEN = "778691262189893|OBbkU1zooaAds-v9IccORHMtj0M"
cityList = ["Sukkur", "Larkana", "Rahim Yar Khan", "Gujrat", "Mardan", "Kasur", "Mingora", "Wah", "Dera Ghazi Khan", "Sahiwal", "Nawabshah", "Mingaora", "Okara", "Mirpur Khas", "Chiniot", "Kamoke", "Sadiqabad", "Burewala", "Jacobabad", "Muzaffargarh", "Muridke", "Jhelum", "Shikarpur", "Khanpur", "Khanewal", "Hafizabad", "Kohat", "Khuzdar", "Dadu", "Gojra", "Mandi Bahauddin", "Daska", "Pakpattan", "Bahawalnagar", "Tando Adam", "Khairpur", "Chishtian Mandi", "Abbottabad", "Jamshoro", "Jaranwala", "Ahmadpur East", "Vihari", "Kamalia", "Kot Addu", "Khushab", "Wazirabad", "Dera Ismail Khan", "Chakwal", "Swabi", "Lodhran", "Nowshera", "Charsadda", "Jalalpur Jattan", "Mianwali", "Chaman", "Hasilpur", "Arifwala", "Chichawatni", "Bhakkar", "Kharian", "Kambar", "Moro", "Mian Channun", "Turbat", "Shahdadkot", "Bhalwal", "Dipalpur", "Badin", "Pano Aqil", "Kotri", "Tando Muhammad Khan", "Harunabad", "Pattoki", "Kahror Pakka", "Attock", "Gujar Khan", "Chuhar Kana", "Toba Tek Singh", "Narowal", "Shahdadpur", "Shabqadar", "Mansehra", "Shujaabad", "Haveli", "Mailsi", "Ghotki", "Sibi", "Jampur", "Sambrial", "Sanghar", "Kabirwala", "Chunian", "Haripur", "Nankana Sahib", "Pasrur", "Gwadar", "Rajanpur", "Rohri", "Zhob", "Matli", "Rabwah", "Mirpur Mathelo", "Bannu", "Dullewala", "Hala", "Ratodero", "Jatoi", "Jauharabad", "Dina", "Bat Khela", "Kot Radha Kishan", "Kahna Nau", "Mustafabad", "Hasan Abdal", "Talagang", "Taunsa", "Thatta", "Sarai Alamgir", "Usta Muhammad", "Kamra", "Umarkot", "Basirpur", "Sehwan", "Fort Abbas", "Havelian", "Dinga", "Khalabat", "Badah", "Tank", "Tandlianwala", "Chak Azam Sahu", "Loralai", "Jalalpur Pirwala", "Pabbi", "Chak Jhumra", "Renala Khurd", "Risalpur", "Lakki Marwat", "Topi", "Hangu", "Chitral", "Kundian", "Khurianwala", "Mehrabpur", "Pindi Bhattian", "Narang", "Malakwal", "Thul", "Pindi Gheb", "Zahir Pir", "Dunyapur", "Gambat", "Kashmor", "Alipur", "Naudero", "Pasni", "Sukheke", "Setharja", "Khewra", "Karak", "Mamu Kanjan", "Sharqpur", "Digri", "Bhera", "Sakrand", "Tando Jam", "Raiwind", "Lalian", "Kharan", "Mehar", "Khangah Dogran", "Khairpur Nathan Shah", "Dir", "Ghauspur", "Tangi", "Utmanzai", "Minchinabad", "Garh Maharaja", "Mastung", "Khipro", "Fazalpur", "Kunjah", "Jhawarian", "Nasirabad", "Nushki", "Sujawal", "Sita Road", "Dijkot", "Sillanwali", "Kandiaro", "Zaida", "Kunri", "Kalat", "Mitha Tiwana", "Daud Khel", "Liaqatabad", "Hazro", "Dunga Bunga", "Amangarh", "Kot Diji", "Kalur Kot", "Murree", "Faqirwali", "Ahmadpur Sial", "Phalia", "Yazman", "Raja Jang", "Samasatta", "Warburton", "Pishin", "Kamir", "Uch", "Chawinda", "Ubauro", "Mithi", "Akora", "Zafarwal", "Kot Samaba", "Eminabad", "Kahuta", "Ranipur", "Kulachi", "Hingorja", "Naukot", "Pind Dadan Khan", "Kanganpur", "Faruka", "Kotli Loharan","Shahpur Chakar", "Talhar", "Qadirpur Ran", "Bela", "Muzaffarabad", "Khangarh", "Sarai Naurang", "Gharo", "Bhit Shah", "Matiari", "Warah", "Lachi", "Baddomalhi", "Jand", "Fatehpur", "Dera Bugti", "Naushahro Firoz", "Dajal", "Isa Khel", "Daur", "Bhopalwala", "Paharpur", "Bhan", "Mach", "Radhan", "Uthal", "Kaleke", "Jiwani", "Johi", "Chor", "Tando Ghulam Ali", "Mangla", "Bhawana", "Jhol", "Sodhra", "Kalabagh", "Sinjhoro", "Harnoli", "Sarai Sidhu", "Hunza", "Choa Saidan Shah", "Dhadar", "Darya Khan", "Garhi Yasin", "Madeji", "Dokri", "Thano Bula Khan", "Dalbandin", "Daulatpur", "Bhag", "Rasulnagar", "Chak", "Baffa", "Garhi Khairo", "Lakhi", "Surab", "Rojhan", "Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Multan",	"Hyderabad", "Gujranwala", "Peshawar", "Sheikhupura", "Jhang", "Quetta", "Islamabad", "Bahawalpur", "Sargodha", "Sialkot"]
con = mdb.connect('localhost', 'root', 'root', 'feedmapdb')


def facebookScrapper():
    cur = con.cursor()
    #cur.execute("DROP TABLE IF EXISTS feeds")
    cur.execute( "CREATE TABLE IF NOT EXISTS newsfeeds (id INT PRIMARY KEY AUTO_INCREMENT, lon VARCHAR(255) NOT NULL, lat VARCHAR(255) NOT NULL, source VARCHAR(255) NOT NULL, headline TEXT NOT NULL, city VARCHAR(255) NOT NULL)" )
    
    pageList   =['dawndotcom']
    
    #fetch data from fb
    for page in pageList:
        url = BASE_URL +page+"/links?access_token="+ACCESS_TOKEN
	newsList = []
        print url
        response = requests.get(url)
        jsonResponse= response.json()
        print response
	data =  jsonResponse['data']
	for allnews in data:
	    print allnews
	    news= allnews['message']
	    newsList.append(news)
	    for news in newsList:
		for word in news.split(' '):
		    for city in cityList:
			if word.lower() == city.lower():
			    print 'match found: '+city
			    writeToDB(city, news, page)
		       
		   
def writeToDB(location, source, headline):
    try:
	con.autocommit(True) 
	cur = con.cursor()
	result = Geocoder.geocode(location)
	(lat, lon) = result[0].coordinates
	query ="INSERT INTO newsfeeds(lon, lat, source, headline, city) VALUES (%s, %s, %s, %s,  %s) ON DUPLICATE KEY UPDATE headline="+headline
	cur.execute( query,(str(lon), str(lat), source, headline, location))
    except GeocoderError: 
	print "The location given by twitter returns error when given to Geocoder"



if __name__ == '__main__':facebookScrapper()

#https://graph.facebook.com/dawndotcom/links?access_token=CAALENzASkUUBAJlIytExlZBzec8DVJjNqkmUarw48oZBkw6ObZBHZCnmzwmhGCtLnwkowpSE30EfoQbqN900roXgpu2mXTWkIEp9OOfibjVQ2zMgze6GCfXmbIU35jAfhm5lAlHCgZCZB8sbrriDW8pCVBZATOGyshwbtjoQumbNvYnntRoV0OvEqhszRsVxewIZAqfDS21ahkBChudLctwQ
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import re
from datetime import datetime

st.set_page_config(layout="wide")
#st.image("./VOXlogo.jpeg",width=500,)
#cf1,cf2,cf3 = st.columns(3)
#with cf2:
# st.title("VOX INDIA") 

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="Vendors", usecols=list(range(17)), ttl=5)
existing_data2 = conn.read(worksheet="Received", usecols=list(range(8)), ttl=5)
existing_data = existing_data.dropna(how="all")

main_data = conn.read(worksheet="AUG", usecols=list(range(14)), ttl=5)
main_data = main_data.dropna(how="all")
total_rows = len(main_data)



if "Name" not in st.session_state:
    st.session_state.Name = ""
if "Phone" not in st.session_state:
    st.session_state.Phone = ""
    
    
def clear_form():
    st.session_state.Name = ""
    st.session_state.Phone = ""
    
# List of Business Types and Products
STATE = [
    " ",
   "Andhra Pradesh",
"Arunachal Pradesh",
"Assam",
"Bihar",
"Chhattisgarh",
"Delhi",
"Goa",
"Gujarat",
"Haryana",
"Himachal Pradesh",
"Jharkhand",
"Jammu & Kashmir",
"Karnataka",
"Kerala",
"Madhya Pradesh",
"Maharashtra",
"Manipur",
"Meghalaya",
"Mizoram",
"Nagaland",
"Odisha",
"Punjab",
"Rajasthan",
"Sikkim",
"Tamil Nadu",
"Telangana",
"Tripura",
"Uttar Pradesh",
"Uttarakhand",
"West Bengal",
]
CITY = [
    " ",
    "Bangalore",
    "Mangalore",
"Mumbai",
"Hyderabad",
"Pune",
"Jaipur",
"Chennai",
"Lucknow",
"Indore",
"Delhi",
"Noida",
"Gurgaon",
"Ahmedabad",
"Kolkata",
"Dehradun",
"Bhopal",
"Thane",
"Nashik",
"Mysore",
"Coimbatore",
"Srinagar",
"Varanasi",
"Tiruchirappalli",
"Ghaziabad",
"Thrissur",
"Visakhapatnam",
"Sangli",
"Rajkot",
"Shimoga",
"Madurai",
"Malappuram",
"Kadapa",
"Jammu",
"Vijayawada",
"Patna",
"Tiruppur",
"Raipur",
"Solapur",
"Kodagu",
"Ludhiana",
"Jalgaon",
"Kollam",
"Jodhpur",
"Bhubaneswar",
"Davangere",
"Bikaner",
"Dindigul",
"Anantapuram",
"Chittoor",
"Gwalior",
"Pudukkottai",
"Shillong",
"Tirunelveli",
"Salem",
"Udaipur",
"Sundargarh",
"Thiruvananthapuram",
"Srikakulam",
"Pondicherry",
"Kochi",
"Muzaffarpur",
"Kanyakumari",
"Kannur",
"Kakinada",
"Kanpur",
"Mohali",
"Karimnagar",
"Ahmednagar",
"Belagavi",
"Ernakulam",
"Amritsar",
"Guntur",
"Banswara",
"Eluru",
"Hanamkonda",
"Chandrapur",
"Shimla",
"Shahjahanpur",
"Yavatmal",
"Sagar",
"Tiruvarur",
"Pathanamthitta",
"West Godavari",
"Purba Bardhaman",
"Osmanabad",
"Sultanpur",
"Ranchi",
"Rampur",
"Trichy",
"Tenkasi",
"Udupi",
"Port Blair",
"Vellore",
"Sangrur",
"Virudhunagar",
"Prakasam",
"Solan",
"Prayagraj",
"Yadadri Bhuvanagiri",
"Mehsana",
"Haveri",
"Kangra",
"Jalna",
"Hooghly",
"Khordha",
"Moradabad",
"Hoshiarpur",
"Muzaffarnagar",
"Jammu & Kashmir",
"Nagpur",
"Jamnagar",
"Mandi",
"Jamshedpur",
"Haryana",
"Kota",
"Morbi",
"Kottayam",
"Munger",
"Leh",
"Jabalpur",
"Jind",
"Nagapattinam",
"Hubli",
"Narmadapuram",
"Haridwar",
"Nellore",
"Kaithal",
"Kashmir",
"Kozhikode",
"Churu",
"Firozabad",
"Alwar",
"Aravalli",
"Godhra",
"Aurangabad",
"Cuttack",
"Bagalkote",
"Dwarka",
"Banaskantha",
"Gandhinagar",
"Bareilly",
"Guna",
"Barnala",
"Cuddalore",
"Begusarai",
"Dakshina Kannada",
"Bemetra",
"Durg",
"Bhuj",
"Erode",
"Bilaspur",
"Gajapati",
"Chandauli",
"Ghaya",
"Aligarh",
"Gujarat",
"Chikmagalur",
"Alipurduar",
"Guwahati",
"Sultanganj",
"Vidisha",
"Tirupati",
"Purba Medinipur",
"Sonepur",
"Puri",
"Tezpur",
"Purnia",
"Ujjain",
"Purulia",
"West Delhi",
"Puruliya",
"South Sikkim",
"Raebareli",
"Suryapet",
"Rafiganj",
"Thoothukudi",
"Rahtas",
"Tripura",
"Raichur",
"Uttara Kannada",
"Raigad",
"Vizianagaram",
"Raigarh",
"West Sikkim",
"Palwal",
"South Andaman",
"Raisen",
"Sri Sathya Sai",
"Rajahmundry",
"Surajpur",
"Rajasthan",
"Tawang",
"Rajgarh",
"Thirunelveli",
"Rajgir",
"Tinsukia",
"Panaji",
"Tiruvannamalai",
"Rajnandgaon",
"Udalguri",
"Rajouri",
"Unakoti",
"Rajsamand",
"Vaishali",
"Ramanathapuram",
"Vikarabad",
"Ramban",
"Washim",
"Ramgarh",
"West Kameng",
"Ramnagar",
"Odisha",
"Panchkula",
"Sonitpur",
"Panchmahal",
"South Dinajpur",
"Ranga Reddy",
"South West Delhi",
"Rangia",
"Pathsala Bajali",
"Ranipet",
"Pakur",
"Ratlam",
"Surendranagar",
"Ratnagiri",
"Tapi",
"Raxaul",
"Telangana",
"Rayagada",
"Thanjavur",
"Reasi",
"Perambalur",
"Rewa",
"Pernem",
"Rewari",
"Pilibhit",
"Ribhoi",
"Pakyong",
"Rohtak",
"Tonk",
"Rohtas",
"Tuticorin",
"Rudraprayag",
"Udhampur",
"Rupnagar",
"Umaria",
"Sabarkantha",
"Uttar Dinajpur",
"Panipat",
"Uttarkashi",
"Sagara",
"Pratapgarh",
"Saharanpur",
"Vijayapura",
"Saharsa",
"Pulwama",
"Sahibganj",
"Warangal",
"Sajapur",
"West Bengal",
"Panna",
"Punjab",
"Samastipur",
"West Midnapore",
"Samba",
"West Tripura",
"Sambalpur",
"Sonbhadra",
"Sambhal",
"Sonipat",
"Sanga Reddy",
"South 24 Parganas",
"Papum Pare",
"South Delhi",
"Parbhani",
"South Goa",
"Sant Kabir Nagar",
"South Tripura",
"Sarajpur",
"Sri Ganganagar",
"Saran",
"Pathankot",
"SAS Nagar",
"Subansiri",
"Sasaram",
"Patiala",
"Satara",
"Supaul",
"Satna",
"Surat",
"Sawai Madhopur",
"Surguja",
"Sehore",
"Tamil Nadu",
"Senapati",
"Tarn Taran",
"Seoni",
"Tehri Garhwal",
"Seraikela-Kharsawan",
"Pauri Garhwal",
"Serchhip",
"Peddapalli",
"Shahdol",
"Theni",
"Parvathipuram",
"Thiruvallur",
"Shajapur",
"Thiruvarur",
"Shamli",
"Thoubal",
"Sharanpur",
"Tikamgarh",
"Sheikhpura",
"Tiptur",
"Sheopur",
"Pithoragarh",
"Paschim Bardhaman",
"Tirupattur",
"Paschim Medinipur",
"Tiruvallur",
"Pashchim Champaran",
"Poonch",
"Shivpuri",
"Porbandar",
"Shopian",
"Tumkur",
"Shrawasti",
"Palakkad",
"Shujapur",
"Udham Singh Nagar",
"Wokha",
"Palamu",
"Yadgir",
"Ukhrul",
"Pashchimi Singhbhum",
"Una",
"Nuh",
"Unnao",
"Sidhi",
"Uttar Pradesh",
"Sikar",
"Uttarakhand",
"Sikkim",
"Vadodara",
"Silapathar",
"Valsad",
"Silchar",
"Palghar",
"Simdega",
"Vijayanagara",
"Sindhudurg",
"Pali",
"Singhbhum ",
"Viluppuram",
"Singrauli",
"Palia Kalan",
"Sirmaur",
"Wanaparthy",
"Sirohi",
"Wardha",
"Sirsa",
"Wayanad",
"Sirsi",
"West Champaran",
"Sitamarhi",
"West Garo Hills",
"Sitapur",
"West Jaintia Hills",
"Sitarganj",
"West Khasi Hills",
"Siva Ganga",
"West Siang",
"Sivasagar",
"West Singhbhum",
"Siwan ",
"Palnadu",
"Patan",
"Siaha",
"Yamunanagar",
"Sibsagar",
"Zunheboto",
"Siddharthnagar",
"Siddipet",
"Mancherial",
"Narayanpet",
"Morena",
"Jharsuguda",
"Madsaur",
"Jhunjhunu",
"Mayiladuthurai",
"Hoskote",
"Nagaland",
"Hosur",
"Nirmal",
"Jogulamba Gadwal",
"Mainpuri",
"Jorhat",
"Mangan",
"Junagadh",
"Mirzapur",
"Kabri Anglong",
"Jangaon",
"Kachchh",
"Nalbari",
"Howrah",
"Naugachhia",
"Kaimur ",
"Madhepura",
"Hardoi",
"Maharashtra",
"Hazaribagh",
"Malerkotla",
"Kalaburagi",
"Mandsaur",
"Kalahandi",
"Margao",
"Kalimpong",
"Meerut",
"Kallakurichi",
"Mokameh",
"Kamareddy",
"Mujafferpur",
"Kamrup",
"Jayashankar Bhupalpalli",
"Kamrup Metro",
"Nagaur",
"Kanchipuram",
"Namsai",
"Kangpokpi",
"Narmada",
"Idukki",
"Nayagarh",
"Kanker",
"North Dinajpur",
"Kannauj",
"Madhya Pradesh",
"Imphal",
"Mahabub Nagar",
"Himachal Pradesh",
"Mahisagar",
"Itanagar",
"Jamalpur",
"Kapurthala",
"Malwa",
"Karauli",
"Hassan",
"Karbi Anglong",
"Manendragarh",
"Kargil",
"Mankachar",
"Karimganj",
"Mathura",
"Hingoli",
"Medak",
"Karnal",
"Hooghly ",
"Karur",
"Moga",
"Karwar",
"Hathras",
"Kasargod",
"Mormugao",
"Kasganj",
"Jamui",
"Jagatsinghpur",
"Janjgir-Champa",
"Kathua",
"Nadia",
"Katihar",
"Jehanabad",
"Katni",
"Nainital",
"Kaushambi",
"Namakkal",
"Kawardha",
"Nandurbar",
"Kendrapara",
"Narayanpur",
"Keonjhar",
"Narsinghpur",
"Kerala",
"Nawada",
"Khagaria",
"Jhansi",
"Khammam",
"Jhargram",
"Khandwa",
"North Sikkim",
"Khargone",
"Madhubani",
"Kheda",
"Madikeri",
"Jagtial",
"Jalpaiguri",
"Khowai",
"Maharajganj",
"Khunti",
"Mahendragarh",
"Kinnaur",
"Mahoba",
"Kiphire",
"Majuli",
"Kishanganj",
"Malda",
"Kishtwar",
"Malkangiri",
"Jaintia Hills",
"Mamit",
"Hisar",
"Mandal",
"Koderma",
"Mandla",
"Kohima",
"Mandya",
"Kokrajhar",
"Mangaldoi",
"Kolar",
"Manipur",
"Kolhapur",
"Mansa",
"Jaisalmer",
"Margherita",
"Jajpur",
"Mau",
"Komaram Bheem",
"Mayurbhanj",
"Kondagaon",
"Medchal Malkajgiri",
"Koppal",
"Meghalaya",
"Koraput",
"Mirganj",
"Korba",
"Mizoram",
"Koriya",
"Hoshangabad",
"Jalandhar",
"Mokokchung",
"Jalaun",
"Jamtara",
"North Tripura",
"Morigaon",
"North West Delhi",
"Motihari",
"Harda",
"Muktsar",
"Kulgam",
"Mungeli",
"Kulgam ",
"Murshidabad",
"Kullu",
"Jaunpur",
"Kupwara",
"Nabarangpur",
"Kurnool",
"Nadiad",
"Kurukshetra",
"Nagaon",
"Kushinagar",
"Nagarkurnool",
"Ladakh",
"Jhabua",
"Lahaul and Spiti",
"Nalanda",
"Lakhimpur",
"Nalgonda",
"Lakhimpur Kheri",
"Namchi",
"Lakhisarai",
"Nanded",
"Lalitpur",
"Narasinghpur",
"Lanka",
"Narayanpeta",
"Latehar",
"Narkatiaganj",
"Latur",
"Jhajjar",
"Hissar",
"Jhalawar",
"Lohardaga",
"Navsari",
"Lohit",
"Nawanshahr",
"Lower Dibang Valley",
"Neemuch",
"Lower Siang",
"Nilgiris",
"Lower Subansiri",
"Nizamabad",
"Hojai",
"North 24 Parganas",
"Jalore",
"North Goa",
"Lumding",
"Jharkhand",
"Lunglei",
"Nuapada",
"Krishna",
"Krishnagiri",
"Dhalai",
"Ghazipur",
"East Sikkim",
"Balangir",
"Damoh",
"Balasore",
"Dindori",
"Ballari",
"Badaun",
"Ballia",
"Ambalapuzha",
"Balrampur",
"Allahabad",
"Anantapur",
"Dholpur",
"Banda",
"Amroha",
"Bandipora",
"Faridabad",
"Adilabad",
"Anand",
"Banka",
"Gonda",
"Bankura",
"Dahod",
"Agarmalwa",
"Darjeeling",
"Bapatla",
"Deoghar",
"Barabanki",
"Dharmapuri",
"Baramulla",
"Dima Hasao",
"Baran",
"Dohad",
"Bardhaman",
"East Godavari",
"Agra",
"Azamgarh",
"Bargarh",
"Fatehgarh Sahib",
"Barmer",
"Gadarwar",
"Anantnag",
"Gautam Buddha Nagar",
"Barpeta",
"Goalpara",
"Barwani",
"Bahraich",
"Bastar",
"Arwal",
"Basti",
"Ashok Nagar",
"Bathinda",
"Darbhanga",
"Beed",
"Datia",
"Andaman and Nicobar",
"Almora",
"Aizawl",
"Devbhumi Dwarka",
"Andhra Pradesh",
"Dhanbad",
"Bettiah",
"Dhemaji",
"Betul",
"Dhule",
"Bhadohi",
"Dinajpur",
"Bhadrachalam",
"Diu Island",
"Bhadradri Kothagudem",
"Dungarpur",
"Bhadrak",
"East Champaran",
"Bhagalpur",
"East Midnapore",
"Bhandara",
"Amaravati",
"Bharatpur",
"Etawah",
"Bharuch",
"Farrukhabad",
"Bhavnagar",
"Fathehabad",
"Bhilwara",
"Forbesganj",
"Bhind",
"Bagaha",
"Bhiwani",
"Garhwa",
"Bhojpur",
"Bageshwar",
"Ajmer",
"Giridih",
"Akola",
"Baghpat",
"Angul",
"Gopalganj",
"Bidar",
"Gumla",
"Bihar",
"Balaghat",
"Bijnor",
"Dadra and Nagar Haveli",
"Alamganj",
"Dakshin Dinajpur",
"Annamayya",
"Daman & Diu",
"Birbhum",
"Dantewada",
"Biswanath",
"Daria",
"Bokaro",
"Darrang",
"Bolangir",
"Dausa",
"Bongaigaon",
"Alluri Sitharamaraju",
"Botad",
"Deogarh",
"Boudh",
"Deoria",
"Budaun",
"Dewas",
"Budgam",
"Dhamtari",
"Bulandshahr",
"Dhar",
"Buldhana",
"Dharwad",
"Bundi",
"Dhenkanal",
"Burdwan",
"Dhubri",
"Burhanpur",
"Dibrugarh",
"Buxar",
"Dimapur",
"Cachar",
"Assam",
"Calicut",
"Diphu",
"Chamarajanagar",
"Doda",
"Chamba",
"Dumka",
"Chamoli",
"Auraiya",
"Champaran",
"East Bardhaman",
"Champawat",
"East Delhi",
"Anuppur",
"East Khasi Hills",
"Chandel",
"East Siang",
"Chandigarh",
"East Singhbhum",
"Alappuzha",
"Ambajipeta",
"Hanumangarh",
"Etah",
"Mon",
"Faizabad",
"Charaideo",
"Faridkot",
"Charkhi Dadri",
"Fatehabad",
"Chatra",
"Fatehpur",
"Chengalpattu",
"Fazilka",
"Araria",
"Firozpur",
"Chhapra",
"Gadag",
"Chhatarpur",
"Gadchiroli",
"Ambedkar Nagar",
"Ganderbal",
"Amethi",
"Ganjam",
"Hajipur",
"Garhwal",
"Amreli",
"Gaya",
"Chikkaballapur",
"Ambala",
"Agartala",
"Gir Somnath",
"Chitradurga",
"Goa",
"Chitrakoot",
"Godda",
"Ariyalur",
"Golaghat",
"Chittorgarh",
"Gondia",
"Churachandpur",
"Gorakhpur",
"Arrah",
"Gulbarga",
"Alirajpur",
"Baksa",
"Cooch Behar",
"Gurdaspur",
"Coorg",
"Arunachal Pradesh",
"Chhattisgarh",
"Hailakandi",
"Chhindwara",
"Hamirpur",
"Chhota Udaipur",
"Chhtarpur",
"Hapur",
"Changlang",
"Chapra",

]
SENTTO = [
    " ",
    "Urban Interior",
    "U k Trader",
    "Sahibzada Ply World",
    "Sri Sai Mantra",
    "Srikanth M",
"JAK arts",
"Vijay Agency",
"Brightway Associates",
"Sai Sales Corporation",
"Shivlaxmi Enterprises",
"Vasant &Sons",
"Haven D",
"Laxdeep Allumimium",
"Sai Wallpaper Home Décor",
"Shiv Shambhu Enterprises",
"Wood galary",
"Sadana interior",
"Moselle interio",
"Unity Enterprises",
"Step up Construction",
"Sachin enterprises",
"Unique Enterprsise",
"Meraki engineering",
"KHEMKA MARKETING",
"DEFINE DESIGNER",
"GANPATI DÉCOR",
"ANNAPURNA TRADERS",
"ARIHANT INTERIOR",
    "Prithavi Infra",
    "Daga Marketing",
    "Aakrishing Infra",
    "Sri Sai Laxmi Enterprise",
    "Chandra Traders",
    "Capital Plywood",
    "Urban Stairs",
    "J K Ceremics",
    "D'cora Elegance",
    "Vijaya Trading",
    "R S Plywood",
    "Shree Ram Group",
    "Golden Traders",
    "K K Innovation",
    "Samyak",
    "Dream Enterprises",
    "cosmo",
"Pearl Impex",
"Samrat",
"UP Group",
"Grace Home",
"Polaris",
"Shivam Laminates",
"Fashion Bazar",
"Trident",
"Kumud Naik",
"Real Marketing",
"Niranjana",
"Rama Home Decor",
"Brite Decor",
"Mishka ",
"Naveen",
"Volt & Wattage",
"M S Enterprises",
"Preksha Associates",
"Ecowin",
"Swagat Ply",
"Ojas Interior",
"Birhul Dev",
"Aarif",
"vox punjab",
"K O Entrade",
"Decor Master",
"Nutan ",
"Glady",
"Bansal Ply Palace",
"Parekh ",
"OPMK",
"Elite Flooring",
"concept",
"Shivam interior",
"Shelter Enterprise",
"Vinay Pandey",
"Kuber Enterprises",
"Punjab & Haryana Group",
"Airavata",
"Naresh Dhiman",
"Cuttack Hardware",
"Sujal Enterprises",
"Deco Studio",
"V2B",
"N B Plywood ",
"B U Combine",
"Wood Option",
"Smart Home",
"Royal Metal ",
"Agarwal Agencies",
"govind",
"Balaji resources",
"Singla Traders",
"Arunachal enterprises",
"G R Enterprises",
"Garg Aluminium",
"Prime Impex",
"Decor Line",
"Aristic Décor",
"Ashirwad Traders",
"Bajrang plywood",
"Ronak Associates",
"Sandeep Chandankar ",
"44 Decore",
"KK Sharma",
"Shiva Mangalore ",
"Alagu",
"Jainson Kitchen",
"Atco Interiors",
"Innovative Dezine",
"palette",
"M N Padia",
"M A enterprises",
"Om Traders",
"Bansal Decor",
"Make One Interior",
"Beacon Trade India",
"Poddar Tiles ",
"Chittaranjan",
"ABI Architectural Indus",
"BBS",
"Yashasvi Enterprices",
"Manish pathak",
"M J Kraftech ",
"Expanse Interior Solution",
"Krishna kumar",
"Gupta Peris",
"Ace Decor",
"Euro Architrade",
"JPk Interior",
"S S enterprises",
"Abhijith",
"Mahendra Pillai",
"Anant plywood",
"Krishna Enterprises",
"Patni Traders",
"Sharad Dhumal",
"L & K",
"Parth Interio",
"S S International",
"Kayvos Ply",
"#N/A",
"Rameez ",
"Kaveri",
"Aseem Trading",
"Turning point ",
"Rupesh Dhiman",
"Divyalaxmi Pali",
"Shree ji Trading  ",
"Vansh Enterprises",
"Global Ichalkaranji",
"Radhe Decor",
"Sanjay Agencies",
"Hemanth",
"Status Interior House",
"Arco",
"Sri Krishna ",
"Krishna Eco Plast",
"Novelty warehouse ",
"Bawani Wala",
"kiran Patil",
"vaidhyanathan",
"Alson Marketing",
"Rahul Shinde",
"Windoor Buildtech",
"Oswal Plywood ",
"Hind Mosaic",
"Krishna Mohan & Sons",
"Shahre Alam ",
"Lotus Furnishing",
"Eventena",
"Rajesh Kumar",
"Arihant enterprises",
"True Line Decor",
"Jalan Enterprises",
"National Decorators",
"Bhavesh Gupta",
"Ganpati Home Decor",
"Sidzern",
"Sukesh",
"Aslon Marketing",
"Shasthi plywood",
"General Construction",
"Mahi Enterprises",
"Nitin Patil",
"Rajasthan lime",
"World Tech",
"Namashivaraj",
"Balaji Creation",
"Ayushman Padhee",
"Abhay Singh",
"R R Builder",
"ARA Interiors",
"B R polynet",
"Ankit Uniyal",
"Fine decor",
"Manish Enterprises",
"Bhairava",
"Alif Enterprises",
"Abhilash",
"Budesh Flooring",
"Alpha Building",
"Seven Seas Interior",
"Neelam Udyog",
"Core Line Infra",
"vansh ",
"RSS Traders",
"Elegant Interior",
"Build Interio",
"Shiva Enterprises",
"Bueaty wares",
"Nagaland Alluminium ",
"Rambiwas Hardware",
"Raju DVS",
"VTC Building product",
"Ravindra Pratap Singh",
"Newaged Ji",
"Shree interiors",
"Somashekar",
"Srinivasan",
"Roshni Agartala",
"Amar enterprises",
"Giriraj Enterprises",
"Shree ram sales",
"Anil Parmar",
"Bhubaneshwar",
"Karan",
"Ashu sharma",
"karthik pareek",
"Prathab Singh",
"Yash Interior and Gypsum House",
"J P K",
"Sree Ji trading company",
"The status Interior",
"Vox Artistic decor",
"Praveen",
"North Pearl",
"Shyam Traders",
"Jos Sanitary",
"Saraswathi Glass",
"S A B Trading",
"Jai kumar",
"Avanish Kumar",
"Deval Vyas",
"Home Maker",
"M R Decor",
"Grand Total",

]
PRODUCT = [
    " ",
    "Ceiling",
    "Wall",
    "Flooring",
    "Skirtings",
    "Dealership",
]
SOURCE = [
    " ",
"AdWords form",
"Catalogue form",
"Chat BOT",
"visited HO",
"Email",
"Exhibition",
"Existing customer",
"Facebook - call",
"Facebook campaign",
"Meta form",
"Google Map",
"India Mart",
"Instagram",
"Instagram - call",
"Landline - Call",
"Reference",
"Web BOT",
"Website - form",
"Website - call",
"youtube - call",
"Youtube",
]
USERS = [
    " ",
    "Vikas",
    "Baburao",
    "Priyanka",
    "Nisha",
    "Meghana",
    "Harun",
    "Revathi",
    "Rukmini",
    "Harun",
]
TYPE = [
    " ",
    "Architect",
    "Interior Designer",
    "End Customer",
    "Dealer/Distributor",
    "Builder",
    "Contractor",
]
OWNERS = [
    " ",
    "samrat.mazumder@voxindia.co",
"abhijit.chakraborty@voxindia.co",
"glady.george@voxindia.co",
"kumudchandra.m.nayak@voxindia.co",
"alagu.muthu.kumaran@voxindia.co",
"sandip.chandankar@voxindia.co",
"krishna.kumar@voxindia.co",
"rahul.shinde@voxindia.co",
"nutan.kumar@voxindia.co",
"hemant.tembhurne@voxindia.co",
"naveen.kumar@voxindia.co",
"shahre.alam@voxindia.co",
"shivakumar.s@voxindia.co",
"rajesh.kumar@voxindia.co",
"jayesh.mehta@voxindia.co",
"govind.dewri@voxindia.co",
"anantha.krishnan@voxindia.co",
"anil.gami@voxindia.co",
"suryatarun.k@voxindia.co",
"joyal.selvan@voxindia.co",
"nitin.patil@voxindia.co",
"abhay.singh@voxindia.co",
"sharad.dhumal@voxindia.co",
"shivaraj.r@voxindia.co",
"bhavesh.gupta@voxindia.co",
"rameez.mohd@voxindia.co",
"aarief.khan@voxindia.co",
"pratik.tiwari@voxindia.co",
"ashu.sharma@voxindia.co",
"jai.kumar@voxindia.co",
"vinay.pandey@voxindia.co",
"vansh.jain@voxindia.co",
"kiran.patil@voxindia.co",
"birhul.dev@voxindia.co",
"ravi.krishna@voxindia.co",
"vinit.jawdekar@voxindia.co",
"manish.pathak@voxindia.co",
"avanish.chaubey@voxindia.co",
"naresh.dhiman@voxindia.co",
"ravindra.singh@voxindia.co",
"durgesh.kumar@voxindia.co",
"somashekhar.g@voxindia.co",
"srikanth.m@voxindia.co",
"anil.parmar@voxindia.co",
"mahendran.pillai@voxindia.co",
"anurag.singh@voxindia.co",
"dilip.pandey@voxindia.co",
"kishor.kumar@voxindia.co",
"sanjeev.kumar@voxindia.co",
"chittaranjan.swain@voxindia.co",
"ankit.uniyal@voxindia.co",
"jeet.basu@voxindia.co",
"karan.singh@voxindia.co",
"ravi.kumar@voxindia.co",
"sanket.shinde@voxindia.co",
"biju.mathew@voxindia.co",
"ajay.verma@voxindia.co",
"prabhakar.b@voxindia.co",
"sukesha.hk@voxindia.co",
"sarit.vohra@voxindia.co",
"raju.dvs@voxindia.co",
"akash.m@voxindia.co",
"sateesh.k@voxindia.co",
"manish.kumar@voxindia.co",
"bharat.chavda@voxindia.co",
"venkateswarlu.g@voxindia.co",
"vinod.kumar@voxindia.co",
"sandeep.kumar@voxindia.co",
"dipak.das@voxindia.co",
"sandeep.sisodiya@voxindia.co",
"sravan.reddy@voxindia.co",
"ashish.goel@voxindia.co",
"kamana.sharma@voxindia.co",
"sadab.husain@voxindia.co",
"harsha.pr@voxindia.co",
"sudhir.tiwari@voxindia.co",
"vijaya.kumar@voxindia.co",
"vikram.singh@voxindia.co",
"boopathiraja@voxindia.co",
"paresh.deshmukh@voxindia.co",
"manoj.kumar@voxindia.co",
"danish.kumar@voxindia.co",
"jaswant.das@voxindia.co",
"madhu.r@voxindia.co",
"deepak.ram@voxindia.co",
"kinjal.deb@voxindia.co",
"shubham.ladikar@voxindia.co",
"pankaj.dubey@voxindia.co",
"vikram.kumar@voxindia.co",
"pardeep.sharma@voxindia.co",
"ganesh.rs@voxindia.co",
"arijit.barua@voxindia.co",
"shubham.sharma@voxindia.co",
"deepak.kc@voxindia.co",
]
#SENTTO2 = [' ','Pearl Impex', 'Niranjana', 'L&K', 'Alif Enterprises']

pattern = re.compile(r"^[6-9]\d{9}$")

tab1, tab2, tab3 = st.tabs(["Form", "Report", "Dashboard"])
with tab1:
 with st.form(key="vendor_form", clear_on_submit=True):
    ce1, ce2, ce3, ce4 = st.columns(4)
    with ce1:
      Date = st.date_input(label="Date")
    with ce2:
      Name = st.text_input(label="Name*", value=st.session_state.Name)
    with ce3:
     State = st.selectbox(label="State*", options=STATE)
    with ce4: 
     City = st.text_input(label="City*")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
     District = st.selectbox(label="District*", options=CITY)
    with c2:
     Phone = st.text_input(label="Phone No*",value=st.session_state.Phone)
    with c3:
      Altphone = st.text_input(label="Alternate Phone")
    with c4:
      Email = st.text_input(label="Email ID")
    cp1, cp2, cp3, cp4 = st.columns(4) 
    with cp1:
      Type = st.selectbox(label="Customer Type*", options=TYPE)
    with cp2:
      Product = st.multiselect(label="Product*", options=PRODUCT)
    with cp3: 
      Sqft = st.text_input(label="Square feet")
    with cp4:
      Source = st.selectbox(label="Source*", options=SOURCE)
    ch1, ch2, ch3, ch4 = st.columns(4)
    with ch1:
      Sentto = st.selectbox(label="Sent To*", options=SENTTO)
    with ch2:
      Sentby = st.selectbox(label="Sent By*", options=USERS)
    with ch3:
      Owner = st.selectbox(label="Owner", options=OWNERS)
    with ch4:
     campaign = st.text_input(label="Source Campaign")  
    cs1, cs2, cs3 = st.columns(3)
    with cs1:
      Notes = st.text_area(label="Notes")
    ic1, ic2, ic3 = st.columns([1,1,2])
    with ic3:  
      ct1, ct2 = st.columns([1,1])
      with ct1:
         submit_button = st.form_submit_button(label="Submit Details")
      with ct2:
         clear_button = st.form_submit_button(label="Clear form", on_click=clear_form)

    is_valid = bool(pattern.match(Phone))
    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        is_valid = bool(pattern.match(Phone))
        if not Name and not Phone and not State and not City and not Sentto and not Product and not Source and not Sentby:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif not is_valid:
            st.warning("Incorrect Phone Number")      
            st.stop()
        else:
            vendor_data = pd.DataFrame(
                [
                    {
                        "DATE": Date,
                        "NAME": Name,
                        "STATE": State,
                        "CITY":City,
                        "DISTRICT": District,
                        "PHONE": Phone,
                        "ALTERNATE PHONE": Altphone,
                        "EMAIL": Email,
                        "TYPE": Type,
                        "PRODUCT": ", ".join(Product),
                        "SQFT": Sqft,
                        "SOURCE":Source,
                        "SENT TO": Sentto,
                        "SENT BY": Sentby,
                        "NOTE": Notes,
                        "OWNER": Owner,
                        "CAMPAIGN": campaign,
                    }
                ]
            )
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Details successfully submitted!")
    #if clear_button:
     #     clear_form()
with tab2:
 existing_data['DATE'] = pd.to_datetime(existing_data['DATE'], format='%d/%m/%Y', errors='coerce')
 today = datetime.today().strftime('%d/%m/%Y')
 current_date_data = existing_data[existing_data['DATE'].dt.strftime('%d/%m/%Y') == today]
 existing_data2['DATE'] = pd.to_datetime(existing_data2['DATE'], format='%d/%m/%Y', errors='coerce')
 #rdata = existing_data2[existing_data2['DATE'].dt.strftime('%d/%m/%Y') == today]
 #rdatarow = ['DATE', 'Website call',	'Meta form', 'Instagram', 'Facebook campaign','Youtube','Website form',	'Youtube call']
 with st.container(border=True):
  st.header(f"{today} QUALIFIED REPORT-------")    
  cxf1, cxf2 = st.columns(2)
  with cxf1: 
   cxxf1, cxxf2 = st.columns(2)            
   with cxxf1:
    if 'SENT BY' in existing_data.columns:
     current_date_data = current_date_data.dropna(subset=['SENT BY'])
     sentby_counts = current_date_data['SENT BY'].value_counts().reset_index()
     sentby_counts.columns = ['SENT BY', 'LEADS']
     total_count = sentby_counts['LEADS'].sum()
     total_row = pd.DataFrame([['TOTAL', total_count]], columns=['SENT BY', 'LEADS'])
     sentby_counts = pd.concat([sentby_counts, total_row], ignore_index=True)
     st.table(sentby_counts)
   with cxxf2:
    if 'SOURCE' in existing_data.columns:
        current_date_data = current_date_data.dropna(subset=['SOURCE'])
        source_count = current_date_data['SOURCE'].value_counts().reset_index()
        source_count.columns = ['SOURCE', 'LEADS']
        tc = source_count['LEADS'].sum()
        tr = pd.DataFrame([['TOTAL', tc]], columns=['SOURCE', 'LEADS'])
        source_count = pd.concat([source_count, tr], ignore_index=True)
        st.table(source_count)
  with cxf2:
   if 'CAMPAIGN' in existing_data.columns:
        current_date_data = current_date_data.dropna(subset=['CAMPAIGN'])
        camp = current_date_data['CAMPAIGN'].value_counts().reset_index()
        camp.columns = ['META CAMPAIGN', 'LEADS']
        ttc = camp['LEADS'].sum()
        ttr = pd.DataFrame([['TOTAL', ttc]], columns=['META CAMPAIGN', 'LEADS'])
        camp = pd.concat([camp, ttr], ignore_index=True)
        st.table(camp)
        
with tab3:
   with st.container(border=True):
    s1, s2, s3 = st.columns(3)
    with s1:
     st.header("Qualified Leads")
     st.header(f"{total_rows}")
    with s2:
      st.header("Closed Leads")
      st.header("95")
    with s3:
     st.header("SQFT closed") 
     st.header("63,051")
   with st.container(border=True):
    sc1, sc2 = st.columns(2)
    with sc1: 
      main_data=main_data.dropna(subset=['Source'])
      zeta = main_data['Source'].value_counts().reset_index()
      zeta.columns = ['SOURCE', 'LEADS']
      tzc = zeta['LEADS'].sum()
      tzc = pd.DataFrame([['TOTAL', tzc]], columns=['SOURCE', 'LEADS'])
      zeta = pd.concat([zeta, tzc], ignore_index=True)
      st.table(zeta)
    with sc2:
      main_data=main_data.dropna(subset=['SENTBY'])
      beta = main_data['SENTBY'].value_counts().reset_index()
      beta.columns = ['SENTBY', 'LEADS']
      tac = beta['LEADS'].sum()
      tac = pd.DataFrame([['TOTAL', tac]], columns=['SENTBY', 'LEADS'])
      beta = pd.concat([beta, tac], ignore_index=True)
      st.table(beta)
    

 
        
 #source_all = existing_data['SOURCE'].value_counts().reset_index()
 #st.bar_chart(source_all, x="SOURCE",y="LEADS")


st.sidebar.image('zIntro.jpeg', use_column_width=True)
st.sidebar.title(f"Total Lead: {total_rows}")          
products = ', '.join(Product)
sidebar_text = f"""
{Name}
{Phone}
{State}
{City}
{products} {Sqft}sqft 
{Source}
{Sentto}
{Notes}
"""
st.sidebar.text_area("Entered LEAD Details:", sidebar_text, height=250)




            
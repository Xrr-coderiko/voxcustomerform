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

existing_data = conn.read(worksheet="Vendors", usecols=list(range(18)), ttl=5)
recdata = conn.read(worksheet="Received", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")
recdata = recdata.dropna(how="all")

campdata = conn.read(worksheet="Daily", usecols=list(range(19)), ttl=5)
campdata = campdata.dropna(how="all")

main_data = conn.read(worksheet="AUG", usecols=list(range(14)), ttl=5)
main_data = main_data.dropna(how="all")
total_rowx = len(main_data)


disdata = conn.read(worksheet="Dealer", usecols=list(range(3)), ttl=5)
disdata = disdata.dropna(how="all")
total_rowd = len(disdata)

if 'Name' not in st.session_state:
    st.session_state.Name = ""
if "PHONE" not in st.session_state:
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
"Delhi NCR",
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
    "Bengaluru",
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
    "B S Marketing",
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
"Facebook call",
"Facebook campaign",
"Meta form",
"Google Map",
"India Mart",
"Instagram",
"Instagram call",
"Landline call",
"Reference",
"Web BOT",
"Website form",
"Website call",
"youtube call",
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

tab1, tab2, tab3, tab4 = st.tabs(["Form", "Report", "Dashboard", "Dealer"])
with tab1:
 with st.form(key="vendor_form"):
    cch1, cch2, cch3 = st.columns(3)
    with cch2:
     Date = st.date_input(label="Date")
    ce1, ce2, ce3, ce4 = st.columns(4)
    with ce1:
      Name = st.text_input(label="Name*", value=st.session_state.Name)
    with ce2:
      Firm = st.text_input(label="Firm Name*")
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
        if not Name or not Phone or not State or not City or not District or not Sentto or not Product or not Source or not Sentby:
            st.warning("Ensure all mandatory fields are filled.")
        elif not is_valid:
            st.warning("Incorrect Phone Number")
        elif Phone in existing_data['PHONE']:
            st.warning("Phone number already existed")
            st.write(f"{Name}")      
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
                        "FIRM": Firm,
                    }
                ]
            )
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Details successfully submitted!")

with tab2:
 existing_data['DATE'] = pd.to_datetime(existing_data['DATE'], format='%d/%m/%Y', errors='coerce')
 today = datetime.today().strftime('%d/%m/%Y')
 today2 = datetime.today().strftime('%d-%m-%Y')
 current_date_data = existing_data[existing_data['DATE'].dt.strftime('%d/%m/%Y') == today]
 campdata['DATE'] = pd.to_datetime(campdata['DATE'], format='%d/%m/%Y', errors='coerce')
 current_camp = campdata[campdata['DATE'].dt.strftime('%d/%m/%Y') == today]
 #['DATE', 'Website call',	'Meta form',	'Chat BOT', 'Website form']
 rvalues = [] 
  
 with st.container(border=True):
  #st.markdown(f"<div style='text-align: center;'><h2>{today2} QUALIFIED REPORT</h2></div>", unsafe_allow_html=True)
  Attended = [87, 107, 47, 116, 36, 24, 46]
  

  #st.header(f"{today} QUALIFIED REPORT-------")    
  cxxf1, cxxf2 = st.columns(2)            
  with cxxf1:    
        st.markdown(f"<div style='text-align: center;'><h2>{today2} LEADS REPORT</h2></div>", unsafe_allow_html=True)
        recdata[["RECEIVED", "PENDING",	"ATTENDED",	"QUALIFIED"]] = recdata[["RECEIVED", "PENDING",	"ATTENDED",	"QUALIFIED"]].fillna(0).astype(int)
        recdata_reset = recdata.reset_index(drop=True)
        hide_table_row_index = """
        <style> table {
            width: 100%;
            
          }
         th, td {
            text-align: center !important;
            vertical-align: middle !important;
            padding: 8px;
            border: 1px solid white; 
         }
         th {
           border: 2px solid White;
           background-color: grey; color: white;
          }
          tr th:nth-child(4), th:nth-child(5), th:nth-child(6)
          {
            background-color: deepskyblue; color: white;
          }
          td:nth-child(1){
            text-align: left !important;
            vertical-align: middle !important;
          }
        </style>
       """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.write(recdata_reset.to_html(index=False, float_format="%.1f"), unsafe_allow_html=True)
        #st.bar_chart(recdata_reset.set_index('SOURCE')['RECEIVED'])
 
  with cxxf1:
    if 'SENT BY' in existing_data.columns:
     current_date_data = current_date_data.dropna(subset=['SENT BY'])
     sentby_counts = current_date_data['SENT BY'].value_counts().reset_index()
     #sentby_counts['ATTENDED'] = Attended
     sentby_counts.columns = ['CC-EXECUTIVE', 'QUALIFIED']
     #.reindex(sentby_counts['CC Executives']).fillna(' ').values
     totalcs = sentby_counts['QUALIFIED'].sum()
     #totalca = sentby_counts['ATTENDED'].sum()
     total_row = pd.DataFrame([['TOTAL', totalcs]], columns=['CC-EXECUTIVE', 'QUALIFIED'])
     finldb = pd.concat([sentby_counts, total_row])
     htmltbst = finldb.to_html(index=False)
     st.write(htmltbst, unsafe_allow_html=True)
     #st.table(finaldf)
  with cxxf2:
   cer1, cer2 = st.columns(2)
   with cer2:
    if 'SOURCE' in existing_data.columns:
     st.markdown(f"<div style='text-align: center; padding-bottom: 20px;'><h2>SOURCE WISE</h2></div>", unsafe_allow_html=True)
     current_date_data = current_date_data.dropna(subset=['SOURCE'])
     source_counts = current_date_data['SOURCE'].value_counts().reset_index()
     source_counts.columns = ['SOURCE', 'QUALIFIED']
     #.reindex(sentby_counts['CC Executives']).fillna(' ').values
     totalcss = source_counts['QUALIFIED'].sum()
     total_rows = pd.DataFrame([['TOTAL', totalcss]], columns=['SOURCE', 'QUALIFIED'])
     finldbc = pd.concat([source_counts, total_rows])
     htmltbst = finldbc.to_html(index=False)
     st.write(htmltbst, unsafe_allow_html=True)       
              
 with st.container(border=True):  
  if 'CAMPAIGN' in existing_data.columns:
      st.markdown(f"<div style='text-align: center;'><h2>{today2} META CAMPAIGN REPORT</h2></div>", unsafe_allow_html=True)
      st.markdown(f"<div style='text-align: center;'><h4>Total Meta qualified leads: 45</h4></div>", unsafe_allow_html=True)
      current_camp = current_camp.dropna(subset=['CAMPAIGN', 'ADSET NAME', 'AD NAME'])
      camp = current_camp[['CAMPAIGN', 'ADSET NAME', 'AD NAME']].value_counts().reset_index()
      camp.columns = ['CAMPAIGN NAME','ADSET NAME', 'AD NAME', 'QUALIFIED']
      ttc = camp['QUALIFIED'].sum()
      ttr = pd.DataFrame([['TOTAL','', '', ttc]], columns=['CAMPAIGN NAME','ADSET NAME', 'AD NAME', 'QUALIFIED'])
      campt = pd.concat([camp, ttr], ignore_index=True)
      htmltbcm = campt.to_html(index=False)
      st.write(htmltbcm, unsafe_allow_html=True)
        
  #rdata = rdata.dropna(subset=['DATE', 'Website call',	'Meta form',	'Chat BOT', 'Website form'])  
  #xamp = rdata['DATE', 'Website call',	'Meta form',	'Chat BOT', 'Website form']                 
      
        
with tab3:
   st.markdown("<div style='text-align: center;'><h1>AUGUST 2024</h1></div>", unsafe_allow_html=True)
   with st.container(border=True, height=200):
    s1, s2, s3 = st.columns(3)
    with s1:
     st.markdown(f"<div style='text-align: center;border: 1px solid white; border-radius: 10px;'><h2>Qualified Leads</h2><h3>{total_rowx}</h3></div>", unsafe_allow_html=True)
     #st.header("Qualified Leads")
     #st.header(f"{total_rows}")
    with s2:
      #st.header("Closed Leads")
      st.markdown("<div style='text-align: center;border: 1px solid white; border-radius: 10px;'><h2>Closed Leads</h2><h3>104</h3></div>", unsafe_allow_html=True)
      #st.markdown("<div style='text-align: center;'><h3>95</h3></div>", unsafe_allow_html=True)
      #st.header("95")
    with s3:
      st.markdown("<div style='text-align: center; border: 1px solid white; border-radius: 10px;'><h2>SQFT closed</h2><h3>66,127</h3></div>", unsafe_allow_html=True)
      # st.header("SQFT closed") 
      #st.header("63,051")
   with st.container(border=True, height=500):
    sc1, sc2 = st.columns(2)
    with sc1:
     with st.container(border=True, height=475):
      st.markdown("<div style='text-align: center;'><h3>Source wise</h3></div>", unsafe_allow_html=True)
      main_data=main_data.dropna(subset=['Source'])
      zeta = main_data['Source'].value_counts().reset_index()
      zeta.columns = ['SOURCE', 'LEADS']
      tzc = zeta['LEADS'].sum()
      tzc = pd.DataFrame([['TOTAL', tzc]], columns=['SOURCE', 'LEADS'])
      zeta = pd.concat([zeta, tzc], ignore_index=True)
      htmlz = zeta.to_html(index=False)
      st.write(htmlz, unsafe_allow_html=True)
    with sc2:
     with st.container(border=True, height=475):
      st.markdown("<div style='text-align: center;'><h3>Team wise</h3></div>", unsafe_allow_html=True)
      main_data=main_data.dropna(subset=['SENTBY'])
      beta = main_data['SENTBY'].value_counts().reset_index()
      beta.columns = ['SENTBY', 'LEADS']
      tac = beta['LEADS'].sum()
      tac = pd.DataFrame([['TOTAL', tac]], columns=['SENTBY', 'LEADS'])
      bxeta = pd.concat([beta, tac], ignore_index=True)
      #st.table(bxeta)
      st.bar_chart(beta.set_index('SENTBY'))
   with st.container(border=True, height=600):
    z1, z2 = st.columns(2)
    with z1:
     with st.container(border=True, height=550):
      st.markdown("<div style='text-align: center;'><h3>State wise</h3></div>", unsafe_allow_html=True)
      main_data=main_data.dropna(subset=['State'])
      xeta = main_data['State'].value_counts().reset_index()
      xeta.columns = ['STATE', 'LEADS']
      tic = beta['LEADS'].sum()
      tic = pd.DataFrame([['TOTAL', tic]], columns=['STATE', 'LEADS'])
      xeta = pd.concat([xeta, tic], ignore_index=True)
      htmlx = xeta.to_html(index=False)
      st.write(htmlx, unsafe_allow_html=True)
    with z2:
     with st.container(border=True, height=550):   
      st.markdown("<div style='text-align: center;'><h3>Distributor wise</h3></div>", unsafe_allow_html=True)
      main_data=main_data.dropna(subset=['SENTTO'])
      peta = main_data['SENTTO'].value_counts().reset_index()
      peta.columns = ['SENT TO', 'LEADS']
      toc = beta['LEADS'].sum()
      toc = pd.DataFrame([['TOTAL', toc]], columns=['SENT TO', 'LEADS'])
      peta = pd.concat([peta, toc], ignore_index=True)
      htmlp = peta.to_html(index=False)
      st.write(htmlp, unsafe_allow_html=True)
with tab4:
  cy1, cy2 = st.columns(2)
  with cy1:
    st.header(f"total dealers: {total_rowd}")      
    dcity = st.text_input(label="City")
    disdata = disdata.dropna(subset=['City', 'Dealer', 'Status'])
    if dcity:
       fcity = disdata[disdata['City'].str.contains(dcity, case=False, na=False)]
       if not fcity.empty:
         st.table(fcity[['Dealer','City', 'Status']])
      
       else: 
         st.write('No Dealers found in this city.')
    else: 
       st.write('please enter a city name to search for dealers.')
  with cy2:
    with st.form(key="dealers"):
     st.write("Add dealers")
     DSTATUS = ['Active', 'Inactive']
     ddname = st.text_input(label="Dealer Name: ")
     ddcity = st.text_input(label="City: ")
     ddstatus = st.selectbox(label="Status ", options=DSTATUS)
     add_button = st.form_submit_button(label='Add Dealer')
      # Create a new row for the DataFrame
     if add_button: 
      new_row = pd.DataFrame([{
       "Dealer": ddname,
       "City": ddcity,
       "Status": ddstatus,
      }])
      ddata = pd.concat([disdata, new_row], ignore_index=True)
      conn.update(worksheet="Dealer", data=ddata)
      st.success('Dealer added')
      st.success()

 
        
 #source_all = existing_data['SOURCE'].value_counts().reset_index()
 #st.bar_chart(source_all, x="SOURCE",y="LEADS")
 #st.sidebar.title(f"Total Lead: {total_rows}")  

st.sidebar.image('zIntro.jpeg', use_column_width=True)
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
st.sidebar.text_area("Entered LEAD Details:", sidebar_text, height=350)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}


.footer {

left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: Orange;
text-align: center;
opacity: 0.4;
}
</style>
<div class="footer">
Developed by <a style='display: inline; text-align: right; text-decoration: none; color: Green;' href="https://www.instagram.com/vkas.ptl?igsh=ZGx3cmh0eTY0ZjBq" target="_blank">@Vikas_Patil 🔥</a>
</div>
"""
st.sidebar.markdown(footer,unsafe_allow_html=True)

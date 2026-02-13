from flask import Flask, render_template_string, request, session, redirect
import smtplib
import random
import mysql.connector
import string

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="124BTIT1036",
    database="sports_db"
)
cursor = db.cursor()

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "binisha.khokhani24@sakec.ac.in"
SENDER_PASSWORD = "yffqlqmpsqfaxfds"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


# ---------------- SEND OTP ----------------
def send_otp_email(receiver_email):
    otp = random.randint(100000, 999999)

    email_text = f"""\
From: {SENDER_EMAIL}
To: {receiver_email}
Subject: Smart Sports Management System OTP

Your OTP is: {otp}
"""

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, email_text)

    return otp


# ---------------- GENERATE USER ID ----------------
def generate_user_id():
    return "SSM" + ''.join(random.choices(string.digits, k=5))


# ---------------- LANDING PAGE ----------------
# ---------------- LANDING PAGE ----------------
@app.route("/")
def landing():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
<title>Smart Sports Management System</title>
<style>
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    height: 100vh;
    background-image: url("https://wallpapers.com/images/high/light-black-background-1920-x-1080-zjqqqdb6vvs2yday.webp");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.title {
    margin-top: 80px;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 3px 3px 8px black;
}

.center-button {
    padding: 20px 50px;
    background: linear-gradient(45deg, #ff7eb3, #ff758c);
    color: white;
    font-size: 1.5em;
    border: none;
    border-radius: 30px;
    text-decoration: none;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.center-button:hover {
    transform: scale(1.1);
}

.sports-images {
    display: flex;
    gap: 30px;
    margin-bottom: 50px;
}

.sports-images img {
    width: 350px;
    height: 250px;
    border-radius: 15px;
    box-shadow: 5px 5px 20px black;
    transition: 0.3s;
}

.sports-images img:hover {
    transform: scale(1.05);
}
</style>
</head>
<body>

<div class="title">Smart Sports Management System</div>

<a class="center-button" href="/enter_email">Register / Log In</a>

<div class="sports-images">
    <img src="https://images.livemint.com/img/2021/08/07/original/2021-08-07T113256Z_809576440_SP1EH870W2T9I_RTRMADP_3_OLYMPICS-2020-ATH-M-JAVELIN-FNL_1628339341789.JPG">
    <img src="https://www.tata.com/content/dam/tata/images/newsroom/community/desktop/tata_archery_academy_banner_desktop_1920x1080.JPG">
    <img src="https://etimg.etb2bimg.com/photo/60183928.cms">
</div>

</body>
</html>
''')



# ---------------- ENTER EMAIL ----------------
@app.route("/enter_email", methods=["GET", "POST"])
def enter_email():
    if request.method == "POST":
        email = request.form["email"]
        otp = send_otp_email(email)
        session["otp"] = str(otp)
        session["email"] = email
        return redirect("/verify")

    return '''
    <h2>Enter Email</h2>
    <form method="POST">
    <input type="email" name="email" required>
    <button type="submit">Send OTP</button>
    </form>
    '''


# ---------------- VERIFY OTP ----------------
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        if request.form["otp"] == session.get("otp"):
            return redirect("/enter_name")
        else:
            return "<h3>Invalid OTP</h3>"

    return '''
    <h2>Enter OTP</h2>
    <form method="POST">
    <input type="text" name="otp" required>
    <button type="submit">Verify</button>
    </form>
    '''


# ---------------- ENTER NAME ----------------
@app.route("/enter_name", methods=["GET", "POST"])
def enter_name():
    if request.method == "POST":
        name = request.form["name"]
        email = session.get("email")

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET name=%s WHERE email=%s", (name, email))
            db.commit()
        else:
            user_id = generate_user_id()
            cursor.execute(
                "INSERT INTO users(name,email,user_id) VALUES(%s,%s,%s)",
                (name, email, user_id)
            )
            db.commit()

        return redirect("/dashboard")

    return '''
    <h2>Enter Name</h2>
    <form method="POST">
    <input type="text" name="name" required>
    <button type="submit">Submit</button>
    </form>
    '''


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Sports Dashboard</title>
<style>
body{
margin:0;
padding:0;
font-family:Arial;
height:100vh;
background-image:url("https://png.pngtree.com/thumb_back/fh260/background/20250308/pngtree-black-brown-red-burnt-orange-amber-yellow-gold-color-gradient-ombre-image_17084558.jpg");
background-size:cover;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
}

h1{
color:black;
margin-bottom:40px;
}

.container{
display:grid;
grid-template-columns:repeat(3,200px);
gap:20px;
}

a{
text-decoration:none;
}

button{
background:white;
color:black;
border:none;
padding:20px;
font-size:18px;
border-radius:10px;
cursor:pointer;
box-shadow:0 8px 0 gray;
transition:0.2s;
width:200px;
}

button:active{
box-shadow:0 3px 0 gray;
transform:translateY(5px);
}
</style>
</head>

<body>

<h1>Select Sport</h1>

<div class="container">
<a href="/badminton"><button>Badminton</button></a>
<a href="/chess"><button>Chess</button></a>

<a href="/dodgeball"><button>Dodgeball</button></a>

<a href="/archery"><button>Archery</button></a>

<a href="/kabaddi"><button>Kabaddi</button></a>

<a href="/football"><button>Football</button></a>

<a href="/basketball"><button>basketball</button></a>

<a href="cricket"><button>cricket</button></a>
<a href="tennis"><button>tennis</button></a>
</div>

</body>
</html>
'''


# ---------------- BADMINTON PAGE ----------------
@app.route("/badminton")
def badminton():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Badminton Events</title>

<style>
body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://www.shutterstock.com/image-vector/colored-back-pop-art-style-260nw-536743687.jpg");
background-size:cover;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://www.lta.org.uk/491dd5/siteassets/news/2023/february/badminton-court.jpg");
background-size:cover;
background-position:center;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:black;
color:yellow;
width:80%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

h1{
text-align:center;
color:yellow;
font-style:italic;
margin-top:30px;
}
</style>
</head>

<body>

<div class="top-image"></div>

<h1>Key Local Badminton Tournament & Academy Contacts</h1>

<div class="content">

<div class="event-box">
<b>Greater Mumbai Badminton Association (GMBA)</b><br>
Hosts junior, senior & masters tournaments across Mumbai.
</div>

<div class="event-box">
<b>Navi Mumbai Sports Association (NMSA)</b><br>
State-level tournaments & coaching.<br>
Coach Yogesh Patil: 9004093196
</div>

<div class="event-box">
<b>Kshatriya Badminton Academy – Andheri West</b><br>
Professional training & tournament exposure.<br>
Contact: 9820799705
</div>

<div class="event-box">
<b>Maharashtra Veteran State Championship 2026</b><br>
Masters category competition across Maharashtra.
</div>

</div>

</body>
</html>
'''
# ---------------- CHESS PAGE ----------------
@app.route("/chess")
def chess():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Chess Events</title>

<style>
body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://www.shutterstock.com/image-illustration/abstract-blue-black-wavelike-design-600nw-2609801001.jpg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://i.ytimg.com/vi/8sZuiXKePAk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCuFA3G3wFiTz1cNym1tWdpfmDK-Q");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:grey;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:blue;
color:black;
width:80%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.7);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>All India Chess Federation – Featured Events 2026</h1>

<div class="content">

<div class="event-box">
<b>National Junior Chess Championship 2026</b><br>
Category: Under 19 Boys & Girls<br>
Dates: 12th March – 20th March 2026<br>
Venue: Mumbai, Maharashtra<br>
Contact: +91 9876543210
</div>

<div class="event-box">
<b>Maharashtra State Open FIDE Rating Tournament</b><br>
FIDE Rated Classical Event<br>
Dates: 5th April – 9th April 2026<br>
Venue: Pune, Maharashtra<br>
Contact: +91 9823456789
</div>

<div class="event-box">
<b>National Women Premier Chess Championship 2026</b><br>
Elite Women’s National Championship<br>
Dates: 10th June – 18th June 2026<br>
Venue: Chennai, Tamil Nadu<br>
Contact: +91 9900011122
</div>

<div class="event-box">
<b>All India Rapid & Blitz Chess Championship</b><br>
Open Category Rapid & Blitz Format<br>
Dates: 25th July – 27th July 2026<br>
Venue: Delhi NCR<br>
Contact: +91 9812345678
</div>

</div>

</body>
</html>
'''

# ---------------- DODGEBALL PAGE ----------------
@app.route("/dodgeball")
def dodgeball():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Dodgeball Events</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpsbiTUrnimEgHWZZgfCjfb_E6gWHnK8sApw&s");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://britishdodgeball.org/wp-content/uploads/2025/11/ball-1-scaled-e1764000866470.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:black;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:grey;
color:black;
width:80%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.6);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Mumbai Dodgeball Association – Major Events 2026</h1>

<div class="content">

<div class="event-box">
<b>Regency Khel Mahotsav Dodgeball Tournament</b><br>
Organized by: Mumbai Dodgeball Association (MDA)<br>
Location: Regency Sports Complex, Mumbai<br>
Dates: 15th January – 20th January 2026<br>
Contact: +91 98765 43210
</div>

<div class="event-box">
<b>18th Senior National Dodgeball Championship (2025-26)</b><br>
Category: Senior Men & Women<br>
Location: Pune, Maharashtra<br>
Dates: 10th February – 15th February 2026<br>
Team Mumbai: Silver Medalists<br>
Contact: +91 98230 56789
</div>

<div class="event-box">
<b>DSO Dodgeball Tournament – Mumbai Suburban</b><br>
District Sports Office (School Level)<br>
Categories: Boys & Girls (U14, U17)<br>
Location: Andheri Sports Ground, Mumbai<br>
Dates: 5th August – 8th August 2026<br>
Contact: +91 98111 22334
</div>

<div class="event-box">
<b>Rupantaran Dodgeball Championship 2026</b><br>
Local Inter-Club & Open Category Event<br>
Location: Borivali Indoor Sports Arena, Mumbai<br>
Dates: 18th October – 22nd October 2026<br>
Contact: +91 98989 77665
</div>

<div class="event-box">
<b>Follow for Updates</b><br>
Official Updates & Registration Details:<br>
Mumbai Dodgeball Association (MDA)<br>
Facebook & Instagram Official Pages
</div>

</div>

</body>
</html>
'''

# ---------------- ARCHERY PAGE ----------------
@app.route("/archery")
def archery():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Archery Events 2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://thumb.photo-ac.com/16/16ace9191dd29f7e910b5c7f0dde0a68_t.jpeg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://images.stockcake.com/public/b/0/8/b08e362a-c693-43f6-999f-3b88d633da7b_large/sunset-archery-silhouette-stockcake.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:orange;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:black;
color:orange;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>National & International Archery Events – 2026</h1>

<div class="content">

<div class="event-box">
<b>2nd NTPC National Ranking Archery Tournament</b><br>
Location: Ambaji, Gujarat<br>
Dates: 24th January – 31st January 2026<br>
Category: Olympic/Recurve & Compound<br>
Contact: Archery Association of India – +91 11 2336 3362
</div>

<div class="event-box">
<b>2nd NTPC Khelo India Women's National Ranking Tournament</b><br>
Location: Patiala, Punjab<br>
Dates: 3rd February – 6th February 2026<br>
Category: Women's Recurve & Compound<br>
Contact: +91 175 221 4200
</div>

<div class="event-box">
<b>Para Archery Assessment & National Trial</b><br>
Location: Jawaharlal Nehru Stadium, Delhi<br>
Dates: 9th February – 12th February 2026<br>
Category: Para Archery (All Divisions)<br>
Contact: +91 11 2309 0521
</div>

<div class="event-box">
<b>Nîmes International Archery Tournament 2026</b><br>
Location: Nîmes, France<br>
Dates: 16th January – 18th January 2026<br>
Category: International Indoor Championship<br>
Contact: +33 4 66 29 40 40
</div>

<div class="event-box">
<b>World Archery Field & 3D Championships 2026</b><br>
Location: TBA (International Venue)<br>
Dates: August 2026<br>
Category: Field & 3D Archery Championships<br>
Contact: World Archery Federation – +41 21 614 30 50
</div>

<div class="event-box">
<b>Archery Premier League – India 2025 Highlights</b><br>
Featured international stars including Brady Ellison and leading Indian archers.<br>
Professional Olympic/Recurve & Compound format league.
</div>

<div class="event-box">
<b>Major Competition Types</b><br>
• Olympic/Recurve – Individual, Team & Mixed Team<br>
• Compound – Professional & National Ranking Events<br>
• Para Archery – Adaptive Competitive Format<br>
• Indian Round – Traditional Indian Tournament Format
</div>

</div>

</body>
</html>
'''
# ---------------- KABADDI PAGE ----------------
@app.route("/kabaddi")
def kabaddi():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Kabaddi Events 2025-2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://wallpapers.com/images/featured/green-and-black-background-6o7fi4exq0rbsvtw.jpg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://www.shutterstock.com/image-vector/premium-editable-vector-file-kabaddi-260nw-2401930173.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:green;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:black;
color:green;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Major Kabaddi Events – 2025 & 2026</h1>

<div class="content">

<div class="event-box">
<b>Pro Kabaddi League (PKL) – Season 12</b><br>
Location: Delhi, India<br>
Dates: 29 August – 31 October 2025<br>
Organized by: Mashal Sports & Amateur Kabaddi Federation of India (AKFI)<br>
Contact: AKFI Office – +91 11 2338 7416
</div>

<div class="event-box">
<b>2025 Kabaddi World Cup</b><br>
Location: England, United Kingdom<br>
Dates: 17 March – 23 March 2025<br>
Organized by: World Kabaddi Federation<br>
Contact: +44 20 8742 8500
</div>

<div class="event-box">
<b>Women’s Kabaddi World Cup 2025</b><br>
Location: Rajgir, Bihar, India<br>
Dates: August 2025<br>
Organized by: Amateur Kabaddi Federation of India<br>
Contact: +91 612 221 7955
</div>

<div class="event-box">
<b>6th Senior Asian Kabaddi Championship (Women)</b><br>
Location: Tehran, Iran<br>
Dates: 4 March – 9 March 2025<br>
Organized by: Asian Kabaddi Federation<br>
Contact: +98 21 6670 3000
</div>

<div class="event-box">
<b>Asia-Oceania Kabaddi Championships 2025</b><br>
Location: India<br>
Dates: September 2025<br>
Organized by: Asian Kabaddi Federation<br>
Contact: +91 11 2338 7416
</div>

<div class="event-box">
<b>Beach Kabaddi World Cup 2025</b><br>
Location: Malaysia<br>
Dates: December 2025<br>
Organized by: World Kabaddi Federation<br>
Contact: +60 3 2273 3000
</div>

<div class="event-box">
<b>Regional & National Events (India)</b><br>
Senior National Kabaddi Championship – Maharashtra<br>
Maharashtra State Kabaddi Association Trials<br>
Contact: +91 22 2654 1234
</div>

<div class="event-box">
<b>Other International Leagues</b><br>
British Kabaddi League – October 2025<br>
Kabaddi League Africa – September 2025<br>
International Friendship Matches (Various Locations)<br>
Contact: World Kabaddi Federation – +44 20 8742 8500
</div>

</div>

</body>
</html>
'''
# ---------------- FOOTBALL PAGE ----------------
@app.route("/football")
def football():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Football Events 2024-2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://4kwallpapers.com/images/wallpapers/red-abstract-1920x1080-17394.jpg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://la28.org/content/dam/latwentyeight/olympic-sports/desktop/OLYFootballDesktop.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:black;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:red;
color:black;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Major Football Events – India & International (2024–2026)</h1>

<div class="content">

<div class="event-box">
<b>Indian Super League (ISL) 2025-26</b><br>
Location: Multi-city, India<br>
Season: September 2025 – April 2026<br>
Organized by: All India Football Federation (AIFF)<br>
Contact: AIFF Headquarters – +91 11 2300 0370
</div>

<div class="event-box">
<b>I-League 2025-26</b><br>
Location: India (National League)<br>
Season: October 2025 – May 2026<br>
Organized by: All India Football Federation<br>
Contact: +91 11 2300 0370
</div>

<div class="event-box">
<b>Durand Cup 2025</b><br>
Location: Kolkata & Multi-city, India<br>
Dates: July – August 2025<br>
Organized by: Durand Football Tournament Society & AIFF<br>
Contact: +91 33 2248 9800
</div>

<div class="event-box">
<b>Indian Women's League (IWL) 2025</b><br>
Location: India<br>
Season: October 2025 – April 2026<br>
Organized by: AIFF Women's Committee<br>
Contact: +91 11 2300 0370
</div>

<div class="event-box">
<b>Santosh Trophy 2025</b><br>
Location: Inter-State Championship, India<br>
Dates: December 2025<br>
Organized by: All India Football Federation<br>
Contact: +91 11 2300 0370
</div>

<div class="event-box">
<b>Subroto Cup 2025</b><br>
Location: New Delhi, India<br>
Dates: September 2025<br>
Category: Inter-School National Tournament<br>
Contact: +91 11 2569 3100
</div>

<div class="event-box">
<b>FIFA World Cup 2026 – Asian Qualifiers</b><br>
Location: Home & Away Fixtures (India)<br>
Match Windows: March & June 2025<br>
Organized by: FIFA & AFC<br>
Contact: FIFA Headquarters – +41 43 222 7777
</div>

<div class="event-box">
<b>AFC U-17 Asian Cup 2026</b><br>
Location: Asia (Host TBA)<br>
Qualifiers: 2025<br>
Final Tournament: 2026<br>
Organized by: Asian Football Confederation (AFC)<br>
Contact: +60 3 8994 3388
</div>

<div class="event-box">
<b>National Beach Soccer Championship 2025</b><br>
Location: Coastal Venue, India<br>
Dates: February 2025<br>
Organized by: AIFF Beach Soccer Committee<br>
Contact: +91 11 2300 0370
</div>

<div class="event-box">
<b>AIFF Futsal Club Championship 2025</b><br>
Location: India<br>
Dates: November 2025<br>
Organized by: All India Football Federation<br>
Contact: +91 11 2300 0370
</div>

</div>

</body>
</html>
'''

# ---------------- BASKETBALL PAGE ----------------
@app.route("/basketball")
def basketball():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Basketball Events 2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://img.pikbest.com/wp/202343/dark-brown-background-watercolor-texture-with-a-rich_9989174.jpg!w700wp");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://upload.wikimedia.org/wikipedia/commons/d/dc/2023-24_Brown_Bears_mens_basketball_players.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:black;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:brown;
color:black;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Major Basketball Events – 2026 (India & International)</h1>

<div class="content">

<div class="event-box">
<b>75th Senior National Basketball Championship</b><br>
Location: Chennai, Tamil Nadu<br>
Dates: 4 January – 11 January 2026<br>
Organized by: Basketball Federation of India (BFI)<br>
Contact: BFI Headquarters – +91 80 2221 9444
</div>

<div class="event-box">
<b>76th Junior National Basketball Championship</b><br>
Location: India (Host TBA)<br>
Dates: 22 April – 29 April 2026<br>
Organized by: Basketball Federation of India<br>
Contact: +91 80 2221 9444
</div>

<div class="event-box">
<b>41st Youth National Basketball Championship</b><br>
Location: India<br>
Dates: September / October 2026<br>
Organized by: BFI Youth Division<br>
Contact: +91 80 2221 9444
</div>

<div class="event-box">
<b>71st Sub-Junior National Basketball Championship</b><br>
Location: India<br>
Dates: September / October 2026<br>
Organized by: Basketball Federation of India<br>
Contact: +91 80 2221 9444
</div>

<div class="event-box">
<b>5th 3x3 Senior National Championship</b><br>
Location: New Delhi, India<br>
Date: 31 January 2026<br>
Category: 3x3 Format<br>
Contact: +91 11 2338 7416
</div>

<div class="event-box">
<b>Indian National Basketball League (INBL) & Pro League</b><br>
Category: U-25 & Professional City Leagues<br>
Season: 2026 Calendar Year<br>
Organized by: Basketball Federation of India<br>
Contact: +91 80 2221 9444
</div>

<div class="event-box">
<b>FIBA Asia Cup 2025–2026 Qualifiers</b><br>
Location: Asia (Home & Away Fixtures)<br>
Organized by: FIBA Asia<br>
Contact: FIBA Headquarters – +41 22 545 00 00
</div>

<div class="event-box">
<b>Asian Games 2026</b><br>
Location: Aichi-Nagoya, Japan<br>
Dates: 19 September – 4 October 2026<br>
Organized by: Olympic Council of Asia<br>
Contact: +965 2242 6174
</div>

<div class="event-box">
<b>FIBA U18 Women’s Asia Cup (Division B)</b><br>
Dates: 13 July – 19 July 2026<br>
Category: International Youth Championship<br>
Contact: +41 22 545 00 00
</div>

<div class="event-box">
<b>Other Professional & Regional Leagues</b><br>
Elite Pro Basketball League<br>
Mizoram Super League<br>
3x3 Pro Basketball League<br>
Contact: Basketball Federation of India – +91 80 2221 9444
</div>

</div>

</body>
</html>
'''

# ---------------- CRICKET PAGE ----------------
@app.route("/cricket")
def cricket():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Cricket Domestic Tournaments – 2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://thumbs.dreamstime.com/b/blue-green-background-texture-image-beautiful-elegant-illustration-graphic-art-design-blue-green-background-texture-image-144371007.jpg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://a.espncdn.com/combiner/i?img=/i/cricket/cricinfo/1523688_1296x729.jpg");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:black;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:#0a3d3f;
color:white;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Major Domestic Cricket Tournaments – India (2026)</h1>

<div class="content">

<div class="event-box">
<b>Ranji Trophy Elite Division 2025-26</b><br>
Category: First-Class Championship<br>
Matches: 119 First-Class Matches<br>
Organized by: Board of Control for Cricket in India (BCCI)<br>
Contact: BCCI Headquarters – +91 22 2289 8800
</div>

<div class="event-box">
<b>Col. C K Nayudu Trophy Elite</b><br>
Category: U-23 Multi-Day Tournament<br>
Matches: 112 U23 Multi-Day Matches<br>
Organized by: BCCI Domestic Cricket Committee<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Senior Women’s One Day Trophy – Elite</b><br>
Category: Women’s Domestic 50-Over Championship<br>
Season: 2026<br>
Organized by: BCCI Women’s Division<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Senior Women’s One Day Trophy – Plate Division</b><br>
Category: Women’s Domestic Plate Division<br>
Season: 2026<br>
Organized by: BCCI<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Vizzy Trophy</b><br>
Category: U-19 Multi-Day Tournament<br>
Season: 2026<br>
Organized by: BCCI Junior Cricket Committee<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Women’s Under-23 One Day Trophy – Elite</b><br>
Category: U23 Women’s 50-Over Championship<br>
Season: 2026<br>
Organized by: BCCI<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Women’s Under-23 One Day Trophy – Plate</b><br>
Category: U23 Women’s Plate Division<br>
Season: 2026<br>
Organized by: BCCI<br>
Contact: +91 22 2289 8800
</div>

<div class="event-box">
<b>Senior Women’s Inter-Zonal One Day Trophy</b><br>
Category: Zonal Championship<br>
Season: 2026<br>
Organized by: BCCI Women’s Cricket Board<br>
Contact: +91 22 2289 8800
</div>

</div>

</body>
</html>
'''
# ---------------- TENNIS PAGE ----------------
@app.route("/tennis")
def tennis():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Tennis Tournaments – India 2026</title>

<style>

body{
margin:0;
padding:0;
font-family:cursive;
background-image:url("https://img.freepik.com/premium-photo/vibrant-gradient-background-with-pink-purple-shades-displayed_744423-10355.jpg?semt=ais_user_personalization&w=740&q=80");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.top-image{
width:100%;
height:600px;
background-image:url("https://media.istockphoto.com/id/583853850/photo/family-playing-tennis-holding-rackets-and-ball.jpg?s=612x612&w=0&k=20&c=5G5MrMdJbw2J6BVsiGvQlaoUHPy0gY70Mlz67KUlmOE=");
background-size:cover;
background-position:center;
}

h1{
text-align:center;
color:purple;
font-style:italic;
margin-top:30px;
}

.content{
padding:40px;
display:flex;
flex-direction:column;
align-items:center;
gap:30px;
}

.event-box{
background:black;
color:purple;
width:85%;
padding:25px;
border-radius:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.8);
font-style:italic;
font-size:20px;
}

</style>
</head>

<body>

<div class="top-image"></div>

<h1>Major Tennis Tournaments – India (2026)</h1>

<div class="content">

<div class="event-box">
<b>UTR Pro Tennis Tour – India Series</b><br>
Location: Multiple Cities, India<br>
Category: Professional & Amateur Rankings<br>
Season: 2026 Calendar<br>
Organizer: UTR Sports India<br>
Website: https://app.utrsports.net/india/tennis-tournaments
</div>

<div class="event-box">
<b>AITA National Ranking Championship (Men & Women)</b><br>
Location: All India Venues<br>
Category: National Ranking Tournament<br>
Season: January – December 2026<br>
Organizer: All India Tennis Association (AITA)<br>
Contact: +91 11 2617 6215
</div>

<div class="event-box">
<b>ITF World Tennis Tour – India Leg</b><br>
Location: Delhi / Pune / Bengaluru<br>
Category: International Ranking Event<br>
Season: 2026<br>
Organizer: International Tennis Federation (ITF)<br>
Contact: +44 20 8392 4600
</div>

<div class="event-box">
<b>Junior National Tennis Championship</b><br>
Category: Under-14, Under-16, Under-18<br>
Season: 2026<br>
Organizer: AITA Junior Committee<br>
Contact: +91 11 2617 6215
</div>

<div class="event-box">
<b>National Inter-State Tennis Championship</b><br>
Category: State Team Championship<br>
Season: Mid 2026<br>
Organizer: All India Tennis Association<br>
Contact: +91 11 2617 6215
</div>

<div class="event-box">
<b>Davis Cup / Billie Jean King Cup (India Fixtures)</b><br>
Category: International Team Competition<br>
Season: 2026<br>
Organizer: ITF & AITA<br>
Contact: +44 20 8392 4600
</div>

<div class="event-box">
<b>UTR 3v3 College & Club Tennis League</b><br>
Location: India Regional Centers<br>
Category: Club & Collegiate Competition<br>
Season: 2026<br>
Organizer: UTR Sports<br>
Website: https://app.utrsports.net/india/tennis-tournaments
</div>

</div>

</body>
</html>
'''

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)




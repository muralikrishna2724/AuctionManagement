"""Add the players from the IPL auctions of 2013-2022 to the built-in pool, skipping anyone already in it.

Usage: python3 tools/add_past_players.py <eda-ipl-player-auction-dataset.ipynb> <html with the IPL-DATASET pool> index.html

The notebook (an EDA of the Kaggle "IPL Player Auction Dataset from start to now") only keeps the full list of
player names, not every row, so each player's role, stats, photo and tags come from IPL-DATASET when they are in it
(matched by exact name or a known spelling variant), and from the PAST table below otherwise. Ratings in PAST are
an estimate of how sought-after the player was at those auctions. Rows flagged ? are guesses: they get the
"Check role" tag so the organiser can confirm them on the Players page. Safe to re-run: earlier additions are
replaced, the IPL 2026 players are left as they are.
"""
import ast, json, re, sys
NB, OLD_HTML, OUT_HTML = sys.argv[1], sys.argv[2], sys.argv[3]
pat = re.compile(r'^const IPL = (\{.*?\});$', re.M)
nk = lambda x: re.sub(r'[^a-z]', '', x.lower())

# Spelling variants and full names used in the auction list -> the name we show (same player)
SAME = {
 'Akshar Rajesh Patel': 'Axar Patel', 'Axar Rajesh Patel': 'Axar Patel', 'Dushmanta Chameera': 'Dushmantha Chameera',
 'Kona Srikar Bharat': 'Srikar Bharat', 'K.S. Bharat': 'Srikar Bharat', 'Mohammad Shami': 'Mohammed Shami',
 'Mohd. Arshad Khan': 'Arshad Khan', 'N. Tilak Varma': 'Tilak Varma', 'Nicolas Pooran': 'Nicholas Pooran',
 'Rashid Khan Arman': 'Rashid Khan', 'Shahrukh Khan': 'M Shahrukh Khan', 'Suyash Prabhudesai': 'Suyash Prabhudessai',
 'Syed Khaleel Ahmed': 'Khaleel Ahmed', 'Varun Chakaravarthy': 'Varun Chakravarthy', 'Yuzvendra Singh Chahal': 'Yuzvendra Chahal',
 'Yudhvir Charak': 'Yudhvir Singh', 'Shahbaz Ahamad': 'Shahbaz Ahmed', 'Rahul Ajay Tripathi': 'Rahul Tripathi', 'Praveen Dubey': 'Pravin Dubey',
 'Sarfaraz Naushad Khan': 'Sarfaraz Khan',
 'Akila Dhananjaya': 'Akila Dananjaya', 'Asif K M': 'KM Asif', 'K.M. Asif': 'KM Asif', 'Barinder Singh Saran': 'Barinder Sran',
 'Barinder Singh Sran': 'Barinder Sran', 'C.Hari Nishaanth': 'C Hari Nishaanth', 'Daniel Christian': 'Dan Christian',
 'Jagadeesha Suchith': 'J Suchith', 'K.C Cariappa': 'KC Cariappa', 'K.C. Cariappa': 'KC Cariappa', 'M. Ashwin': 'Murugan Ashwin',
 'N. Jagadeesan': 'N Jagadeesan', 'R. Sanjay Yadav': 'Sanjay Yadav', 'Siddharth Kaul': 'Siddarth Kaul',
 'Tejas Singh Baroka': 'Tejas Baroka', 'Mandeep Hardev Singh': 'Mandeep Singh', 'Ankit Nagendra Sharma': 'Ankit Sharma',
 'Benjamin Stokes': 'Ben Stokes', 'Christopher Gayle': 'Chris Gayle', 'Christopher Morris': 'Chris Morris',
 'Christopher Barnwell': 'Chris Barnwell', 'Steven Smith': 'Steve Smith', 'Kusal Janith Perera': 'Kusal Perera',
 'Ankit Singh Rajpoot': 'Ankit Rajpoot', 'Anirudha Ashok Joshi': 'Anirudha Joshi', 'Apoorv Vijay Wankhade': 'Apoorv Wankhade',
 'Aryaman Vikram Birla': 'Aryaman Birla', 'Akhil Arvind Herwadkar': 'Akhil Herwadkar', 'Gurkeerat Singh Mann': 'Gurkeerat Mann',
 'Ishwar Chandra Pandey': 'Ishwar Pandey', 'Laxmi Ratan Shukla': 'Laxmi Shukla', 'Lukman Hussain Meriwala': 'Lukman Meriwala',
 'Manan Ajay Sharma': 'Manan Sharma', 'Nikhil Shankar Naik': 'Nikhil Naik', 'Nidheesh M D Dinesan': 'MD Nidheesh',
 'Prince Balwant Rai Singh': 'Prince Balwant Rai', 'Ranganath Vinay Kumar': 'Vinay Kumar', 'Rudra Pratap Singh': 'RP Singh',
 'Siddhesh Dinesh Lad': 'Siddhesh Lad', 'Srikkanth Anirudha': 'Anirudha Srikkanth', 'Subramaniam Badrinath': 'S Badrinath',
 'Tirumalasetti Suman': 'T Suman', 'Domnic Joseph Muthuswamy': 'Domnic Muthuswamy', 'Ryan Ten Doeschate': 'Ryan ten Doeschate',
 'Rassie Van Der Dussen': 'Rassie van der Dussen', 'Jean-Paul Duminy': 'JP Duminy', 'K.Bhagath Varma': 'K Bhagath Varma',
 'K.K. Jiyaz': 'KK Jiyaz', 'C.M. Gautam': 'CM Gautam', 'M. Harisankar Reddy': 'Harishankar Reddy', 'R Samarth': 'Ravikumar Samarth',
 'Midhun S': 'S Midhun', 'Obed Mccoy': 'Obed McCoy', 'Javon Searless': 'Javon Searles', 'Sachithra Senanayaka': 'Sachithra Senanayake',
 'Juan Theron': 'Rusty Theron', 'Zahir Khan Pakteen': 'Zahir Khan', 'Philip Hughes': 'Phillip Hughes', 'Darcy Short': "D'Arcy Short",
 'Kishore Pramod Kamath': 'Pramod Kamath', 'Joshua Philippe': 'Josh Philippe', 'Colin De Grandhomme': 'Colin de Grandhomme',
 'Marchant De Lange': 'Marchant de Lange', 'Krismar Santokie': 'Krishmar Santokie', 'Shubam Agrawal': 'Shubham Agrawal',
}

# name | role | overseas | capped | rating | bats | bowls | tags | ? (unsure)
# bowls: rf right-arm fast, rfm fast-medium, rmf medium-fast, rm medium, lf/lfm/lmf/lm left-arm, ob offbreak, lb legbreak,
#        lbg legbreak googly, sla slow left-arm orthodox, lws left-arm wrist-spin
# tags: P Power Hitter, F Finisher, A Anchor, D Death Bowler, X Pace Ace, S Spin Wizard, M Match Winner, G Gun Fielder, V Versatile, K Safe Hands, R Rising Star
PAST = """
Aaron Finch|BAT|1|1|80|R||PA
Abhijeet Tomar|BAT|0|0|55|R||
Abhimanyu Mithun|BOWL|0|1|62|R|rfm|
Abhinav Sadarangani|BAT|0|0|52|R||
Abhishek Nayar|AR|0|1|64|L|rm|
Abu Nechim Ahmed|BOWL|0|0|58|R|lfm|
Aditya Garhwal|BAT|0|0|52|L||
Aditya Tare|WK|0|0|60|R||K
Agnivesh Ayachi|AR|0|0|50|R|ob||?
Aiden Blizzard|BAT|1|0|58|L||
Ajantha Mendis|BOWL|1|1|76|R|ob|S
Akhil Herwadkar|BAT|0|0|52|L||
Akila Dananjaya|BOWL|1|1|66|R|ob|S
Akshay Karnewar|AR|0|0|55|R|ob|
Akshay Wakhare|BOWL|0|0|52|R|ob|
Akshdeep Nath|BAT|0|0|60|R|rm|
Albie Morkel|AR|1|1|78|L|rfm|PF
Alex Carey|WK|1|1|70|L||K
Alex Hales|BAT|1|1|76|R||P
Ambati Rayudu|BAT|0|1|84|R|ob|AF
Amit Paunikar|WK|0|0|50|R||
Andrew Tye|BOWL|1|1|76|R|rfm|D
Aneeshwar Gautam|AR|0|0|50|L|sla||?
Angelo Mathews|AR|1|1|76|R|rm|V
Aniket Choudhary|BOWL|0|0|58|R|lmf|
Anirudha Joshi|AR|0|0|54|R|lb|
Ankeet Bawane|BAT|0|0|55|R||
Ankit Sharma|BOWL|0|0|60|L|sla|
Ankit Rajpoot|BOWL|0|0|64|R|rfm|
Ankush Bains|WK|0|0|52|R||
Ansh Patel|BOWL|0|0|50|R|rm||?
Anunay Singh|BOWL|0|0|52|R|rm|
Anureet Singh|BOWL|0|0|56|R|rmf|
Apoorv Wankhade|BAT|0|0|52|R||
Armaan Jaffer|BAT|0|0|52|R||
Aryaman Birla|BAT|0|0|52|L||
Aryan Juyal|WK|0|0|54|R||
Asela Gunarathna|AR|1|1|62|R|rm|
Ashish Nehra|BOWL|0|1|82|R|lfm|DX
Ashish Reddy|AR|0|0|58|R|rmf|
Ashok Dinda|BOWL|0|1|68|R|rfm|
Ashwin Hebbar|BAT|0|0|54|R||
KM Asif|BOWL|0|0|60|R|rmf|
Baba Aparajith|AR|0|0|56|R|ob|
Baba Indrajith|BAT|0|0|55|R||
Baltej Dhanda|BOWL|0|0|54|R|rmf|
Bandaru Ayyappa|BOWL|0|0|52|R|rmf|
Barinder Sran|BOWL|0|1|64|L|lmf|
Basil Thampi|BOWL|0|0|60|R|rf|
Ben Cutting|AR|1|1|70|R|rf|P
Ben Dunk|WK|1|1|62|L||P
Ben Hilfenhaus|BOWL|1|1|68|R|rfm|
Ben Laughlin|BOWL|1|1|62|R|rmf|D
Ben Stokes|AR|1|1|90|L|rfm|MV
Benny Howell|AR|1|0|60|R|rm|
Beuran Hendricks|BOWL|1|1|62|L|lfm|
Bhanuka Rajapaksa|BAT|1|1|70|L||P
Billy Stanlake|BOWL|1|1|64|L|rf|X
Bipul Sharma|AR|0|0|60|L|sla|
Brad Hodge|BAT|1|1|72|R|ob|F
Brad Hogg|BOWL|1|1|68|L|lws|S
Brendan Taylor|WK|1|1|64|R||
Brendon McCullum|WK|1|1|86|R||PM
C Hari Nishaanth|BAT|0|0|56|L||
CM Gautam|WK|0|0|56|R||
Cameron Delport|BAT|1|0|58|L||P
Carlos Brathwaite|AR|1|1|74|R|rfm|P
Chaitanya Bishnoi|AR|0|0|55|L|ob|
Chama Milind|BOWL|0|0|60|L|lmf|
Chamika Karunaratne|AR|1|1|64|R|rmf|
Cheteshwar Pujara|BAT|0|1|62|R||A
Chirag Suri|BAT|1|1|52|R||
Chris Green|AR|1|0|58|R|ob|
Chris Jordan|BOWL|1|1|74|R|rfm|D
Chris Lynn|BAT|1|1|80|R||P
Chris Barnwell|AR|1|0|54|R|rm|
Chris Gayle|BAT|1|1|92|L|ob|PM
Chris Morris|AR|1|1|86|R|rf|PD
Clinton McKay|BOWL|1|1|58|R|rfm|
Colin de Grandhomme|AR|1|1|70|R|rm|P
Colin Ingram|BAT|1|1|70|L||
Colin Munro|BAT|1|1|70|L||P
Corey Anderson|AR|1|1|76|L|lfm|P
Dale Steyn|BOWL|1|1|88|R|rf|XM
Dan Christian|AR|1|1|72|R|rfm|F
Daniel Sams|AR|1|1|70|R|lfm|
D'Arcy Short|BAT|1|1|70|L|lws|P
Darren Bravo|BAT|1|1|62|L||
Darren Sammy|AR|1|1|74|R|rm|F
David Wiese|AR|1|1|66|R|rmf|
Dawid Malan|BAT|1|1|70|L||
Debabrata Das|BAT|0|0|50|R||
Deepak Punia|BOWL|0|0|50|R|rm||?
Dhawal Kulkarni|BOWL|0|1|72|R|rmf|
Dhruv Shorey|BAT|0|0|56|R||
Digvijay Deshmukh|AR|0|0|54|R|rm|
Dinesh Salunkhe|BOWL|0|0|52|R|lb|
Dirk Nannes|BOWL|1|1|74|R|lf|X
Dishant Yagnik|WK|0|0|54|L||
Dominic Drakes|AR|1|0|60|L|lmf|
Domnic Muthuswamy|BOWL|0|0|50|L|lmf||?
Dwaine Pretorius|AR|1|1|66|R|rmf|
Dwayne Bravo|AR|1|1|89|R|rmf|DM
Dwayne Smith|BAT|1|1|76|R|rm|P
Eklavya Dwivedi|WK|0|0|54|R||
Eoin Morgan|BAT|1|1|78|L||F
Evin Lewis|BAT|1|1|74|L||P
Fabian Allen|AR|1|1|62|R|sla|
Farhaan Behardien|BAT|1|1|58|R|rm|
Fidel Edwards|BOWL|1|1|64|R|rf|X
Gautam Gambhir|BAT|0|1|87|L||AM
George Bailey|BAT|1|1|74|R||F
Gurinder Sandhu|BOWL|1|1|60|R|rfm|
Gurkeerat Mann|AR|0|1|64|R|ob|
Hanuma Vihari|BAT|0|1|64|R|ob|A
Harbhajan Singh|BOWL|0|1|86|R|ob|SM
Hardus Viljoen|BOWL|1|1|60|R|rf|
Harry Gurney|BOWL|1|1|62|R|lmf|
Himmat Singh|BAT|0|0|56|R||
Hrithik Shokeen|AR|0|0|58|R|ob|
HS Sharath|BOWL|0|0|52|R|rmf||?
Imran Tahir|BOWL|1|1|84|R|lbg|S
Iqbal Abdullah|BOWL|0|0|58|L|sla|
Irfan Pathan|AR|0|1|80|L|lmf|V
Ishan Porel|BOWL|0|0|58|R|rfm|
Ishank Jaggi|BAT|0|0|54|R||
Ishwar Pandey|BOWL|0|0|62|R|rmf|
Isuru Udana|AR|1|1|62|L|lmf|
J Suchith|AR|0|0|58|L|sla|
Jacob Oram|AR|1|1|70|L|rmf|
Jacques Kallis|AR|1|1|86|R|rfm|A
Jalaj Saxena|AR|0|0|56|R|ob|
James Faulkner|AR|1|1|80|R|lfm|DF
James Neesham|AR|1|1|70|L|rmf|
Jaskaran Singh|BOWL|0|0|54|R|rmf|
Jatin Saxena|BAT|0|0|52|R||
Javon Searles|AR|1|0|56|R|rmf|
Jaydev Shah|BAT|0|0|54|L||
JP Duminy|AR|1|1|80|L|ob|F
Jeevan Mendis|AR|1|1|58|L|lb|
Jesse Ryder|BAT|1|1|66|L|rm|P
Joe Denly|BAT|1|1|58|R|lb|
Joel Paris|BOWL|1|1|56|L|lfm|
Jofra Archer|BOWL|1|1|90|R|rf|XDM
Johan Botha|AR|1|1|68|R|ob|
John Hastings|BOWL|1|1|62|R|rfm|
Josh Hazlewood|BOWL|1|1|86|L|rfm|X
Josh Philippe|WK|1|1|62|R||
Rusty Theron|BOWL|1|1|58|R|rfm|
K Bhagath Varma|AR|0|0|50|R|ob||?
KC Cariappa|BOWL|0|0|58|R|lb|
KK Jiyaz|BOWL|0|0|50|R|rm||?
Kamlesh Nagarkoti|BOWL|0|0|62|R|rf|R
Kane Richardson|BOWL|1|1|70|R|rfm|D
Kanishk Seth|BOWL|0|0|50|L|lm||?
Karan Sharma|BOWL|0|0|62|R|lb|
Karanveer Singh|BOWL|0|0|54|R|lb|
Karun Nair|BAT|0|1|70|R||
Kedar Jadhav|BAT|0|1|78|R|ob|F
Keemo Paul|AR|1|1|62|R|rfm|
Kevin Pietersen|BAT|1|1|84|R|ob|P
Kevon Cooper|BOWL|1|0|64|R|rmf|D
Kieron Pollard|AR|1|1|90|R|rm|PFM
Pramod Kamath|AR|0|0|50|R|rm||?
Krishmar Santokie|BOWL|1|1|58|L|lfm|
Kshitiz Sharma|BAT|0|0|52|R||
Kuldip Yadav|BOWL|0|0|54|L|lws|
Kulwant Khejroliya|BOWL|0|0|56|L|lmf|
Kusal Perera|WK|1|1|66|L||P
Kyle Abbott|BOWL|1|1|64|R|rfm|
Lakshmipathy Balaji|BOWL|0|1|70|R|rmf|
Lasith Malinga|BOWL|1|1|92|R|rf|DXM
Laxmi Shukla|AR|0|1|64|R|rm|
Luke Pomersbach|BAT|1|0|60|L||
Lukman Meriwala|BOWL|0|0|56|L|lmf|
Luvnith Sisodia|WK|0|0|52|L||
Murugan Ashwin|BOWL|0|0|62|R|lbg|
Harishankar Reddy|BOWL|0|0|56|R|rmf|
Manan Sharma|AR|0|0|52|L|sla|
Manan Vohra|BAT|0|0|62|R||
Mandeep Singh|BAT|0|1|68|R||
Manjot Kalra|BAT|0|0|56|L||
Manoj Tiwary|BAT|0|1|70|R|lb|
Manpreet Gony|BOWL|0|1|64|R|rmf|
Manprit Juneja|BAT|0|0|54|R|ob|
Manvinder Bisla|WK|0|0|64|R||
Manzoor Dar|BAT|0|0|50|R||
Marchant de Lange|BOWL|1|1|62|R|rf|X
Martin Guptill|BAT|1|1|76|R||P
Michael Clarke|BAT|1|1|72|R|sla|
Michael Hussey|BAT|1|1|84|L||AF
S Midhun|BOWL|0|0|52|R|lb|
Milind Kumar|BAT|0|0|52|R||
Milind Tandon|BAT|0|0|50|R||
Mitchell Johnson|BOWL|1|1|84|L|lf|X
Mitchell McClenaghan|BOWL|1|1|78|L|lfm|D
Mithun Manhas|BAT|0|0|60|R|ob|
Mohammed Azharudeen|WK|0|0|54|R||
Moises Henriques|AR|1|1|70|R|rmf|
Monu Singh|BOWL|0|0|50|R|rmf||?
Morne Morkel|BOWL|1|1|84|R|rf|X
Mujeeb Zadran|BOWL|1|1|76|R|ob|S
Munaf Patel|BOWL|0|1|72|R|rmf|
Murali Kartik|BOWL|0|1|70|L|sla|
Murali Vijay|BAT|0|1|78|R||A
Muttiah Muralitharan|BOWL|1|1|82|R|ob|S
N Jagadeesan|WK|0|0|60|R||
Naman Ojha|WK|0|1|70|R||K
Nathan Coulter-Nile|BOWL|1|1|76|R|rf|X
Nathan McCullum|AR|1|1|62|R|ob|
Nathu Singh|BOWL|0|0|56|R|rf|
Nic Maddinson|BAT|1|1|56|L||
MD Nidheesh|BOWL|0|0|52|R|rmf|
Nikhil Naik|WK|0|0|54|R||
Obed McCoy|BOWL|1|1|66|L|lfm|D
Odean Smith|AR|1|1|68|R|rf|P
Oshane Thomas|BOWL|1|1|62|R|rf|X
Pankaj Jaswal|AR|0|0|52|L|lm||?
Pankaj Singh|BOWL|0|1|62|R|rmf|
Paras Dogra|BAT|0|0|58|R||
Pardeep Sahu|BOWL|0|0|56|R|lb|
Parthiv Patel|WK|0|1|76|L||K
Parveez Rasool|AR|0|1|60|R|ob|
Parvinder Awana|BOWL|0|1|62|R|rmf|
Pavan Deshpande|AR|0|0|54|L|ob|
Pawan Negi|AR|0|1|70|L|sla|
Pawan Suyal|BOWL|0|0|56|L|lmf|
Peter Handscomb|WK|1|1|58|R||
Phillip Hughes|BAT|1|1|62|L||
Pradeep Sangwan|BOWL|0|0|62|L|lmf|
Pragyan Ojha|BOWL|0|1|74|L|sla|S
Prasanth Padmanabhan|BOWL|0|0|52|R|lb|
Prasanth Parameswaran|BOWL|0|0|52|L|lmf|
Prashant Chopra|BAT|0|0|54|R||
Pratham Singh|BAT|0|0|54|L||
Pratyush Singh|BAT|0|0|50|R|||?
Praveen Kumar|BOWL|0|1|76|R|rm|
Pravin Tambe|BOWL|0|0|64|R|lb|S
Prayas Ray Barman|BOWL|0|0|54|R|lbg|
Prince Balwant Rai|BAT|0|0|52|R||
Priyam Garg|BAT|0|0|62|R||R
Ravikumar Samarth|BAT|0|0|52|R||
Rahul Buddhi|BAT|0|0|50|L||
Rahul Sharma|BOWL|0|1|66|R|lbg|
Rahul Shukla|BOWL|0|0|54|R|lfm|
Raj Angad Bawa|AR|0|0|62|L|rmf|R
Rajagopal Sathish|AR|0|0|56|R|rm|
Rajat Bhatia|AR|0|0|64|R|rm|
Ramesh Kumar|AR|0|0|52|L|sla|
Vinay Kumar|BOWL|0|1|72|R|rmf|D
Rasikh Dar|BOWL|0|0|56|R|rmf|
Rassie van der Dussen|BAT|1|1|70|R||
Ravi Bopara|AR|1|1|66|R|rm|
Ravi Rampaul|BOWL|1|1|64|R|rfm|
Ricky Ponting|BAT|1|1|78|R||
Riley Meredith|BOWL|1|1|64|R|rf|X
Ripal Patel|BAT|0|0|54|R||P
Robin Uthappa|WK|0|1|84|R||PA
Ronit More|BOWL|0|0|52|R|rmf|
Ross Taylor|BAT|1|1|72|R||
RP Singh|BOWL|0|1|74|L|lmf|
Ryan McLaren|AR|1|1|58|L|rfm|
Ryan ten Doeschate|AR|1|1|64|R|rm|
Sachin Baby|BAT|0|0|58|L||
Sachin Rana|AR|0|0|54|R|rm|
Sachithra Senanayake|BOWL|1|1|60|R|ob|
Sagar Trivedi|AR|0|0|50|R|ob||?
Sam Billings|WK|1|1|66|R||
Samuel Badree|BOWL|1|1|70|R|lbg|S
Sandeep Bavanaka|BAT|0|0|50|R||
Sandeep Lamichhane|BOWL|1|1|68|R|lbg|S
Sanjay Yadav|AR|0|0|54|L|sla|
Sarabjit Ladda|BOWL|0|0|50|R|lb|
Saurabh Dubey|BOWL|0|0|52|L|lmf|
Saurabh Kumar|AR|0|0|56|L|sla|
Saurabh Tiwary|BAT|0|0|68|L||P
Sayan Ghosh|BOWL|0|0|52|R|rmf|
Sayan Sekhar Mandal|AR|0|0|50|L|sla||?
Scott Boland|BOWL|1|1|62|R|rfm|
Sean Abbott|BOWL|1|1|64|R|rfm|
Shadab Jakati|BOWL|0|0|60|L|sla|
Shahbaz Nadeem|BOWL|0|1|68|R|sla|S
Shakib Al Hasan|AR|1|1|82|L|sla|V
Shane Watson|AR|1|1|89|R|rfm|PM
Sharad Lumba|BAT|0|0|50|R||
Shaun Marsh|BAT|1|1|78|L||A
Sheldon Cottrell|BOWL|1|1|68|L|lfm|
Sheldon Jackson|WK|0|0|58|R||
Shelley Shaurya|BAT|0|0|50|R|||?
Shishir Bhavane|BAT|0|0|50|R||
Shivam Sharma|AR|0|0|56|R|lb|
Shivil Kaushik|BOWL|0|0|56|L|lws|
Shreevats Goswami|WK|0|0|62|L||
Shrikant Mundhe|AR|0|0|50|R|rm||?
Shubham Agrawal|BOWL|0|0|50|R|lb||?
Shubham Garhwal|AR|0|0|50|L|sla||?
Shubham Ranjane|AR|0|0|50|R|rm||?
Siddarth Kaul|BOWL|0|1|70|R|rmf|D
Siddhesh Lad|BAT|0|0|54|R||
Anirudha Srikkanth|BAT|0|0|56|R||
Steve Smith|BAT|1|1|86|R|lb|A
Stuart Binny|AR|0|1|68|R|rm|
S Badrinath|BAT|0|0|70|R||A
Subhranshu Senapati|BAT|0|0|56|R||
Sudeep Tyagi|BOWL|0|1|56|R|rmf|
Sumit Narwal|WK|0|0|52|R||
Sushant Marathe|BAT|0|0|50|L||
Syed Mehdi Hasan|AR|0|0|52|R|sla||?
Tajinder Dhillon|AR|0|0|52|R|rm||?
Tanmay Agarwal|BAT|0|0|54|L||
Tanmay Mishra|BAT|1|1|54|R||
Tejas Baroka|BOWL|1|1|50|R|lb||?
Thisara Perera|AR|1|1|72|L|rmf|P
Tim Southee|BOWL|1|1|76|R|rfm|X
T Suman|BAT|0|0|58|R|ob|
Tymal Mills|BOWL|1|1|76|R|lf|X
Umang Sharma|BAT|0|0|52|R||
Unmukt Chand|BAT|0|0|64|R||R
Utkarsh Singh|AR|0|0|52|L|ob|
Vaibhav Rawal|BAT|0|0|52|R||
Varun Aaron|BOWL|0|1|70|R|rf|X
Veer Pratap Singh|BOWL|0|0|54|R|rmf|
Venugopal Rao|BAT|0|1|64|R|ob|
Vijay Zol|BAT|0|0|56|L||
Vikas Tokas|BOWL|0|0|52|R|rmf|
Vikramjeet Malik|BOWL|0|0|56|R|rmf|
Virat Singh|BAT|0|0|56|L||
Virender Sehwag|BAT|0|1|88|R|ob|PM
Wayne Parnell|BOWL|1|1|70|R|lfm|
Writtick Chatterjee|AR|0|0|50|R|ob|
Yogesh Gowalkar|BOWL|0|0|50|R|rmf||?
Yogesh Takawale|WK|0|0|54|R||
Yusuf Pathan|AR|0|1|86|R|ob|PFM
Yuvraj Singh|AR|0|1|88|L|sla|PM
Zaheer Khan|BOWL|0|1|86|R|lfm|XM
Zahir Khan|BOWL|1|0|56|L|lws|
"""
BOWL = {'rf': 'right-arm fast', 'rfm': 'right-arm fast-medium', 'rmf': 'right-arm medium-fast', 'rm': 'right-arm medium',
        'lf': 'left-arm fast', 'lfm': 'left-arm fast-medium', 'lmf': 'left-arm medium-fast', 'lm': 'left-arm medium',
        'ob': 'right-arm offbreak', 'lb': 'legbreak', 'lbg': 'legbreak googly', 'sla': 'slow left-arm orthodox', 'lws': 'left-arm wrist-spin'}
TAG = {'P': '🔥 Power Hitter', 'F': '🚀 Finisher', 'A': '🧱 Anchor', 'D': '🎯 Death Bowler', 'X': '⚡ Pace Ace', 'S': '🌀 Spin Wizard',
       'M': '🏅 Match Winner', 'G': '🏃 Gun Fielder', 'V': '🔄 Versatile', 'K': '🧤 Safe Hands', 'R': '🌱 Rising Star'}
TABLE = {}
for line in PAST.strip().splitlines():
    f = (line.split('|') + [''] * 9)[:9]
    TABLE[nk(f[0])] = f

nb = json.load(open(NB, encoding='utf-8'))
names = None
for c in nb['cells']:
    for o in c.get('outputs', []):
        t = ''.join(o.get('data', {}).get('text/plain', ''))
        if t.startswith('array([') and 'Aaron Finch' in t:
            names = ast.literal_eval(t[t.index('['):t.rindex(']') + 1])
assert names, 'player list not found in the notebook'
old = {}
for p in json.loads(pat.search(open(OLD_HTML, encoding='utf-8').read()).group(1))['players']:
    old.setdefault(nk(p['n']), p); old.setdefault(nk(p['sn']), p)
html = open(OUT_HTML, encoding='utf-8').read()
m = pat.search(html)
I = json.loads(m.group(1))
cur = [p for p in I['players'] if p.get('s26')]          # IPL 2026 players stay, earlier additions are rebuilt
have = {nk(p['n']) for p in cur}
bp = lambda r: 200 if r >= 86 else 150 if r >= 80 else 100 if r >= 74 else 75 if r >= 68 else 50 if r >= 62 else 25   # base prices in ₹0.25 Cr steps
out, seen, skipped, matched, guessed, missing = [], set(), [], 0, [], []
for raw in names:
    name = SAME.get(raw, raw)
    k = nk(name)
    if k in have: skipped.append(raw); continue
    if k in seen: continue
    seen.add(k)
    p = old.get(k)
    if p and nk(p['n']) != k:            # matched through a short name (R. Ashwin) -> dedupe on the full one
        if nk(p['n']) in have: skipped.append(raw); continue
        if nk(p['n']) in seen: continue
        seen.add(nk(p['n']))
    if p:
        matched += 1
        e = {key: (v[:] if isinstance(v, list) else v) for key, v in p.items()}
        e['cat'] = 'Capped' if e['cat'] == 'Marquee' else e['cat']
    else:
        f = TABLE.get(k)
        if not f: missing.append(raw); continue
        n, r, os_, cap, rt, bat, bw, tg, unsure = f
        e = {'n': n, 'sn': n, 'cid': 0, 'r': r, 'rt': int(rt), 'bp': bp(int(rt)), 'bat': bat, 'bowl': BOWL.get(bw, ''),
             'bk': ('spin' if bw in ('ob', 'lb', 'lbg', 'sla', 'lws') else 'pace') if bw else '', 'os': int(os_),
             'cat': 'Capped' if cap == '1' else 'Uncapped', 'tg': [TAG[c] for c in tg], 'img': '', 'dob': '', 'st': None}
        if unsure: e['tg'].append('❓ Check role'); guessed.append(n)
    e['pa'] = 1          # sold at an IPL auction between 2013 and 2022
    e['s26'] = None
    out.append(e)
assert not missing, 'add these to PAST: ' + ', '.join(missing)
out.sort(key=lambda x: (-x['rt'], x['n']))
I['players'] = cur + out
html = html[:m.start()] + 'const IPL = ' + json.dumps(I, ensure_ascii=False, separators=(',', ':')) + ';' + html[m.end():]
open(OUT_HTML, 'w', encoding='utf-8').write(html)
print('notebook names', len(names), '| already in the pool', len(skipped), '| added', len(out),
      f'({matched} with IPL stats, {len(out) - matched} from the table, {len(guessed)} to check)')
print('pool now', len(I['players']))
print('skipped:', ', '.join(skipped))
print('check:', ', '.join(guessed))

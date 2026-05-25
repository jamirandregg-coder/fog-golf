from fpdf import FPDF

class FOGGuide(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, 'FOG Golf League - User Guide', align='C')
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 90, 50)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 90, 50)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.cell(8, 5.5, '-')
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def check_page_space(self, needed=40):
        if self.get_y() > self.h - self.b_margin - needed:
            self.add_page()

pdf = FOGGuide()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=25)
pdf.add_page()

# -- COVER PAGE --
pdf.ln(50)
pdf.set_font('Helvetica', 'B', 32)
pdf.set_text_color(30, 90, 50)
pdf.cell(0, 14, 'FOG Golf League', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_font('Helvetica', '', 16)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 10, 'User Guide', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_draw_color(30, 90, 50)
pdf.line(70, pdf.get_y(), 140, pdf.get_y())
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 7, 'thefog.golf', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, '2025 Season', align='C', new_x="LMARGIN", new_y="NEXT")

# -- PAGE 2: WHAT IS FOG? --
pdf.add_page()

pdf.section_title('What is FOG Golf League?')
pdf.body_text(
    "FOG Golf League is a web app for managing a weekly 9-hole golf league. "
    "It handles everything from RSVPs and tee time pairings to live hole-by-hole "
    "scoring, skins, payouts, and season-long standings. The app works on any "
    "device with a browser and can be installed on your phone for quick access."
)

pdf.section_title('Getting Started')
pdf.body_text(
    "Visit thefog.golf in your phone or computer browser. No account or login "
    "needed. Every player in the league can RSVP, enter scores, and view "
    "results immediately."
)

pdf.sub_title('Add to Your Home Screen (Recommended)')
pdf.body_text(
    "For the best experience, add the app to your phone so it opens like a native app:"
)
pdf.bullet("iPhone: Open thefog.golf in Safari, tap the Share icon, then 'Add to Home Screen.'")
pdf.bullet("Android: Open thefog.golf in Chrome, tap the menu, then 'Add to Home Screen' or 'Install App.'")

pdf.sub_title('Turn On Notifications')
pdf.body_text(
    "When you first open the app, you may see a banner asking to enable notifications. "
    "Tap 'Enable' to receive alerts when scoring opens, rounds close, or the admin "
    "sends announcements. On iPhone, notifications only work if the app has been added "
    "to your home screen first."
)

# -- NAVIGATION --
pdf.add_page()
pdf.section_title('Navigating the App')
pdf.body_text('The app has seven main tabs along the top of the screen:')

tabs = [
    ('This Week', "Your home base. Shows the current week's course, date, tee times, RSVP list, pairings, and the reigning champion."),
    ('Live Scoring', 'Enter your hole-by-hole scores during a round and watch the live scorecard update in real time.'),
    ('Pairings', 'View tee time groupings for each week.'),
    ('Standings', "Season-long leaderboard showing each player's rank, average, best score, and rounds played."),
    ('Scores', 'Week-by-week history of past rounds and results.'),
    ('Schedule', 'The full season schedule with courses, dates, and RSVP status for each week.'),
    ('Past Seasons', 'Historical standings and champions from previous seasons.'),
]
for name, desc in tabs:
    pdf.sub_title(name)
    pdf.body_text(desc)

# -- THIS WEEK --
pdf.add_page()
pdf.section_title('This Week (Home Tab)')

pdf.sub_title('Course & Round Info')
pdf.body_text(
    "At the top you will see the course name, date, par, and tee times for the "
    "upcoming or current round."
)

pdf.sub_title('RSVP')
pdf.body_text(
    "Below the course info is the RSVP list showing every player in the league. "
    "Tap your name to toggle your status:"
)
pdf.bullet("'I'm In' (green) - You are confirmed to play.")
pdf.bullet("'Out' (red) - You cannot make it this week.")
pdf.bullet("'Pending' (gray) - You have not responded yet.")
pdf.body_text(
    "Your payment status is also shown. Once the admin marks you as paid, "
    "a green 'PAID' badge appears next to your name."
)

pdf.sub_title('Adding a Guest')
pdf.body_text(
    "Want to bring a friend? Type their name in the 'Guest name...' box and "
    "tap '+ Add Guest.' The guest will appear in the RSVP list with a gold "
    "'GUEST' badge and will automatically be marked as 'In.' Guests participate "
    "in pairings, live scoring, and payouts for that week only. They do not "
    "appear in season standings."
)

pdf.sub_title('Pairings Preview')
pdf.body_text(
    "Once tee time pairings have been generated, they appear on the This Week "
    "tab so you can quickly see your group and tee time."
)

pdf.sub_title('Winner Banner')
pdf.body_text(
    "After a round is scored and closed, a champion banner appears showing "
    "the low scorer with their score and course."
)

pdf.sub_title('Announcements')
pdf.body_text(
    "If the admin posts an announcement, a gold banner appears at the top of "
    "the page with the message. You can dismiss it by tapping the X."
)

# -- LIVE SCORING --
pdf.add_page()
pdf.section_title('Live Scoring')

pdf.sub_title('How It Works')
pdf.body_text(
    "When a round is live, the Live Scoring tab lets you enter your scores "
    "hole by hole. Select your name from the dropdown, then type your score "
    "for each hole. Tap 'Save Scores' to sync so everyone sees your scores "
    "in real time."
)

pdf.sub_title('Score Colors')
pdf.body_text('Scores are color-coded on the scorecard:')
pdf.bullet('Birdie or better: highlighted in pink/magenta')
pdf.bullet('Par: standard white')
pdf.bullet('Bogey: muted color')
pdf.bullet('Double bogey or worse: red')

pdf.sub_title('Group Scoring')
pdf.body_text(
    "When group scoring is enabled, the designated scorer for each group "
    "sees a full group scorecard and can enter scores for everyone in "
    "the group. But you can always still scroll down and enter your own "
    "score individually. Both methods work at the same time."
)

pdf.sub_title('Live Scorecard')
pdf.body_text(
    "Below the score entry, a full scorecard grid shows all players' "
    "scores updating in real time. It includes each hole, totals, and "
    "score vs. par."
)

# -- PAYOUTS --
pdf.check_page_space(60)
pdf.section_title('Payouts & Prizes')
pdf.body_text(
    "When a round is closed, the Payouts section appears on the Live Scoring tab, "
    "breaking down the prize money:"
)
pdf.sub_title('Skins')
pdf.body_text(
    "The lowest score on each hole wins that hole's skin. If two or more players "
    "tie, the hole is a 'push' and no one wins. The skins pot is split among "
    "all hole winners."
)
pdf.sub_title('Closest to Pin')
pdf.body_text(
    'On designated par-3 holes, the player closest to the pin wins the CTP prize.'
)
pdf.sub_title('Long Drive')
pdf.body_text(
    'On the designated long drive hole, the longest drive wins the prize.'
)
pdf.sub_title('Low Gross')
pdf.body_text(
    "The player with the lowest total score for the round wins the low gross pot. "
    "If there is a tie, the pot is split."
)
pdf.sub_title('Total Earnings')
pdf.body_text(
    "A summary at the bottom shows each player's total earnings for the round "
    "and their net (earnings minus the entry fee)."
)

# -- PAIRINGS --
pdf.add_page()
pdf.section_title('Pairings')
pdf.body_text(
    "The Pairings tab shows tee time groupings for each week. Each group lists "
    "the tee time and the players assigned to it. Guest players are marked with "
    "a 'G' badge. Pairings are generated based on who has RSVP'd 'In.'"
)

# -- STANDINGS --
pdf.check_page_space(50)
pdf.section_title('Standings')
pdf.body_text(
    'The Standings tab is the season leaderboard. It shows every player ranked by '
    'their scoring average and includes:'
)
pdf.bullet('Rank')
pdf.bullet('Player name')
pdf.bullet('Rounds played')
pdf.bullet('Total score across all rounds')
pdf.bullet('Scoring average')
pdf.bullet('Best single-round score')
pdf.bullet('Score vs. par')
pdf.body_text(
    'Guest players are not included in standings since they only play individual weeks.'
)

# -- SCHEDULE --
pdf.check_page_space(50)
pdf.section_title('Schedule')
pdf.body_text(
    "The Schedule tab shows every week of the season with the course, date, and status "
    "(Upcoming, This Week, or Completed). Tap on any week to expand it and see the "
    "RSVP status for that week. You can RSVP for future weeks directly from the schedule."
)

# -- SCORES HISTORY --
pdf.check_page_space(50)
pdf.section_title('Scores (History)')
pdf.body_text(
    "The Scores tab shows results from all past rounds. Each week lists the course, "
    "par, and every player's score. It is your record book for the season."
)

# -- PAST SEASONS --
pdf.check_page_space(50)
pdf.section_title('Past Seasons')
pdf.body_text(
    'View standings and champions from previous seasons. Use the season selector '
    'at the top to switch between years.'
)

# -- PAYING DUES --
pdf.check_page_space(50)
pdf.section_title('Paying League Dues')
pdf.body_text(
    "The This Week tab includes a Venmo link for paying your weekly entry fee. "
    "Tap 'Pay League Dues via Venmo' to open Venmo directly. Once the admin "
    "confirms your payment, a green 'PAID' badge will appear next to your name "
    "in the RSVP list."
)

# -- TIPS & FAQ --
pdf.add_page()
pdf.section_title('Tips & FAQ')

pdf.sub_title("My scores are not showing on another device?")
pdf.body_text(
    "Make sure you have an internet connection and refresh the page. Scores sync "
    "through Firebase in real time, so they should appear within seconds."
)

pdf.sub_title('How do I know when scoring is open?')
pdf.body_text(
    "If you have enabled notifications, you will get a push alert when scoring opens. "
    "You can also check the Live Scoring tab for the round status badge (Setup, "
    "Live, or Closed)."
)

pdf.sub_title('Can I edit my score after saving?')
pdf.body_text(
    "Yes, as long as the round is still live (not closed). Just go back to Live "
    "Scoring, select your name, update your scores, and save again."
)

pdf.sub_title('What if I am bringing a guest?')
pdf.body_text(
    "Go to the This Week tab, type the guest's name in the input box, and "
    "tap '+ Add Guest.' They will be included in everything for that week."
)

pdf.sub_title('How do I get notifications on iPhone?')
pdf.body_text(
    "You must add the app to your home screen first (Safari > Share > Add to Home "
    "Screen). Then open the app from the home screen icon and enable notifications "
    "when prompted. Regular Safari does not support push notifications on iOS."
)

# -- OUTPUT --
output_path = r'C:\Users\jamia\OneDrive\Desktop\FOG Golf League - User Guide.pdf'
pdf.output(output_path)
print(f'PDF saved to: {output_path}')

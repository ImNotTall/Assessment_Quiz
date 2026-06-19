# imports from outside main python
import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

def get_capitals():
    # retrieves capital data from csv file

    file = open("00_Country_Capital_List.csv", "r")
    all_capitals = list(csv.reader(file, delimiter=","))
    file.close()

    all_capitals.pop(0)

    return all_capitals

def get_round_capitals():

    all_capital_list = get_capitals()

    round_capitals = []

    while len(round_capitals) < 4:
        potential_capital = random.choice(all_capital_list)

        if potential_capital not in round_capitals:
            round_capitals.append(potential_capital)

    # shuffles the round capitals

    random.shuffle(round_capitals)

    capital_length = [len(item[1]) for item in round_capitals]

    # finds median for later use in stats
    capital_length.sort()
    median = (capital_length[1] + capital_length[2]) / 2
    median = round_ans(median)

    return round_capitals, median

def round_ans(val):

    # Rounds numbers to nearest integer

    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)

class StartGame:

    def __init__(self):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # introduction to how to play the game

        intro_string = ("Enter the number of round you would like to play. If you would like to try for a high "
                        "score, press the infinite mode. Each round you will be given a random country then " 
                        "you select from one of the four buttons what capital responds to said country.\n\n"

                        "Your goal is to get as many countries correct and get the highest score possible.\n\n"
                        "Use the 'Hints' and 'Stats' located under the question choices."
                        )

        choose_string = "How many rounds do you want to play?"

        start_labels_list = [
            ["Capital Quiz", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#009900"]
        ]

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=590, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # code buttons and "number enterer"

        self.choose_label = start_label_ref[2]

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=5, pady=10)

        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=12,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=5)

        self.infinite_mode_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#E33C38", text="Infinite Mode! 🔥", width=25,
                                  command=self.infinite_mode)
        self.infinite_mode_button.grid(row=1, column=0, pady=2, columnspan=2)

    def check_rounds(self):

        # Asks the user to see how many rounds they want to play. Tells them
        # to enter a number larger than 0 if it's below.

        rounds_wanted = self.num_rounds_entry.get()

        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:

                Play(rounds_wanted, infinite=0)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 10, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

    def infinite_mode(self):

        # sets number of rounds to a large number to make it
        # seem like its infinite

        number_of_rounds = 999999999999999

        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        try:
            number_of_rounds = int(number_of_rounds)
            if number_of_rounds > 0:

                Play(number_of_rounds, "yes")
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 10, "bold"))
            self.infinite_mode_button.config(bg="#F4CCCC")

class Play:

    def __init__(self, how_many, infinite):

        # Lists to store everything for later use

        self.quiz_score = IntVar()

        self.streak = IntVar()
        self.best_streak = IntVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        self.round_capital_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.infinite_mode_yn = infinite

        body_font = ("Arial", 12)

        # Top of GUI labels and information

        play_labels_list = [
            ["Round # of #", ("Arial", 16, "bold"), None, 0],
            ["What is the Country Capital of: ", body_font, "#24bf2a", 1],
            ["'Country'", ("Arial", 18, "bold"), "#6599EC", 2],
            ["Capital", body_font, "#ABABAB", 3]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0] , font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        self.heading_label = play_labels_ref[0]
        self.question_label = play_labels_ref[1]
        self.country_name_label = play_labels_ref[2]
        self.results_label = play_labels_ref[3]

        self.capital_frame = Frame(self.game_frame)
        self.capital_frame.grid(row=4)

        self.capital_button_ref = []
        self.button_capitals_list = []

        # Area for capital names and lengths

        for item in range(0, 4):
            self.capital_button = Button(self.capital_frame, font=("Arial", 12),
                                         text=f"Capital Name", width=15,
                                         command=partial(self.round_results, item))
            self.capital_button.grid(row=item // 2,
                                     column=item % 2,
                                     padx=5, pady=5)

            self.capital_button_ref.append(self.capital_button)

        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=7)

        # buttons of main play screen

        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 10, 0, 1],
            [self.game_frame, "End Game", "#990000", self.close_play, 21, 7, None]
        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5]+1, column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.new_round()

        self.score_label = Label(self.game_frame, text="Score: 0",
                                 font=("Arial", 12, "bold"))
        self.score_label.grid(row=5, pady=5)

    def new_round(self):

        # creates new question when next round starts

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        self.round_capital_list, self.median = get_round_capitals()

        # changes the amount of rounds at top of screen depending on what mode

        if self.infinite_mode_yn != "yes":

            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")

        else:
            self.heading_label.config(text=f"Round {rounds_played} of Infinite!")

        self.question_label.config(text=f"Choose the Correct Capital of:",
                                 font=("Arial", 10, "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # checks for correct capital selected

        self.correct_answer = random.choice(self.round_capital_list)

        self.country_name_label.config(text=self.correct_answer[0])

        # Capital buttons after each round change back to original state
        for count, item in enumerate(self.capital_button_ref):
            item.config(
                text=f"{self.round_capital_list[count][1]} [{self.round_capital_list[count][4]}]",
                state=NORMAL,
                bg="#FFFFFF")

            print(self.round_capital_list[count][1])

            self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):

        # displays information after round

        selected = self.round_capital_list[user_choice]

        rounds_won = self.rounds_won.get()

        for button in self.capital_button_ref:
            button.config(state=DISABLED)

        # if user answer is correct changes selected answer green

        if selected == self.correct_answer:
            self.results_label.config(text="Correct! ✅", bg="#C6EFCE")
            self.quiz_score.set(self.quiz_score.get() + 1)

            self.streak.set(self.streak.get() + 1)

            if self.streak.get() > self.best_streak.get():
                self.best_streak.set(self.streak.get())

            self.capital_button_ref[user_choice].config(bg="#35DB46")

            rounds_won += 1
            self.rounds_won.set(rounds_won)

        # if user answer is wrong changes selected answer red and correct
        # answer green

        else:
            self.results_label.config(
                text=f"Wrong ❌\nCorrect: {self.correct_answer[1]}",
                bg="#FFC7CE"
            )

            self.capital_button_ref[user_choice].config(bg="#E73C2F")

            self.streak.set(0)

            # Find and highlight correct answer in green
            for index, item in enumerate(self.round_capital_list):
                if item == self.correct_answer:
                    self.capital_button_ref[index].config(bg="#35DB46")

        # Disable buttons after answering
        self.next_button.config(state=NORMAL)

        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        # ends game if number of rounds is equal to number of rounds selected

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.capital_button_ref:
            item.config(state=DISABLED)

        # updates score for each round

        self.score_label.config(text=f"Score: {self.quiz_score.get()}")

    def close_play(self):

        root.deiconify()
        self.play_box.destroy()

    # gets variables ready to be transferred into next class

    def to_hints(self):

        print("correct answer:", self.correct_answer)
        print("round capital list: ", self.round_capital_list)

        Hints(self, self.correct_answer, self.median)

    def to_stats(self):

        rounds_won = self.rounds_won.get()
        rounds_played = self.rounds_played.get()
        streak_amount = self.best_streak.get()

        stats_bundle = [rounds_won, rounds_played, streak_amount]

        Stats(self, stats_bundle)

class Stats:
    def __init__(self, partner, all_stats_info):

        # calculates stats from users choices

        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        streak_amount = all_stats_info[2]

        self.stats_box = Toplevel()

        partner.stats_button.config(state=DISABLED)

        # if users press cross at top closes stats and
        # 'releases' stats button

        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        rounds_played = user_scores

        # calculates success rate between rounds

        success_rate = rounds_won / rounds_played * 100
        total_score = rounds_won

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")

        # calculates total score of rounds won and best streak

        total_score_string = f"Total Score: {total_score}"

        streak_amount_string = f"Best Streak: {streak_amount}"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")

        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [streak_amount_string, normal_font, "W"],
            ["\nRound Stats", heading_font, ""],
        ]

        # code for displaying all stats

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1], wraplength=300,
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_stats(self, partner):
        # Put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

class Hints:

    def __init__(self, partner, first_letter_hint, median):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # displays median number of letters each capital has per round for hint

        # disable help button
        partner.hints_button.config(state=DISABLED)

        self.correct_answer = first_letter_hint
        self.median = median

        # if users press cross at top closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid(padx=0, pady=0)

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Hint",
                                        font=("Arial", 14, "bold"),
                                        padx=30, pady=30)
        self.help_heading_label.grid(row=0)

        capital_length = len(self.correct_answer[1])

        # compares the correct answer length to overall median length and displays something different
        #depending on much smaller or larger it is

        if capital_length >= self.median:
            help_text = f"The capital is at LEAST / MORE than {median} letters long!"

        elif capital_length <= self.median:
            help_text = f"The Capital is at LEAST / LESS than {median} letters long!"

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left",
                                     font=("Arial", 20))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=30, pady=30)

        # closes help dialogue (used by button and x at top of dialogue)

    def close_hints(self, partner):
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()

# displays the whole quiz as a separate window

if __name__ == "__main__":
    root = Tk()
    root.title("Capital Quiz")
    StartGame()
    root.mainloop()


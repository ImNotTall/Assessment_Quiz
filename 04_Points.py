import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

def get_capitals():

    capitals = ["Wellington", "Canberra", "Washington D.C", "London", "Paris", "Beijing", "Tokyo", "Bangkok"]

    random_capital = random.choice(capitals)
    print(random_capital)

    return capitals

def round_capitals():

    capitals_list = get_capitals()

    round_capitals = []

    while len(round_capitals) < 4:
        potential_capital = random.choice(capitals_list)

        if potential_capital not in round_capitals:
            round_capitals.append(potential_capital)

    # Trial this. It shuffles the round capitals.

    random.shuffle(round_capitals)

    return round_capitals

class StartGame:

    def __init__(self):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        intro_string = (" Smaller Game to Check Points "
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

                Play(rounds_wanted)
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

class Play:

    def __init__(self, how_many):

        # A lot of lists

        self.quiz_score = IntVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.round_capital_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        body_font = ("Arial", 12)

        # Top of GUI labels and information

        play_labels_list = [
            ["Round # of #", ("Arial", 16, "bold"), None, 0],
            ["What is the Country Capital of: ", body_font, "#24bf2a", 1],
            ["'Country'", body_font, "#6599EC", 2],
            ["Capital", body_font, "#ABABAB", 3]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
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

        for item in range(0, 4):
            self.capital_button = Button(self.capital_frame, font=("Arial", 12),
                                         text="Capital Name", width=15,
                                         command=partial(self.round_results, item))
            self.capital_button.grid(row=item // 2,
                                     column=item % 2,
                                     padx=5, pady=5)

            self.capital_button_ref.append(self.capital_button)

        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=7)

        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None]
        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5]+1, column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.new_round()

        self.score_label = Label(self.game_frame, text="Score: 0",
                                 font=("Arial", 12, "bold"))
        self.score_label.grid(row=5, pady=5)

    def new_round(self):

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        self.round_capital_list = round_capitals()

        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")

        self.question_label.config(text=f"Chose the correct Capital",
                                 font=("Arial", 14, "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        self.correct_answer = random.choice(self.round_capital_list)

        self.country_name_label.config(text=self.correct_answer)

        for count, item in enumerate(self.capital_button_ref):
            item.config(text=self.round_capital_list[count],
                        state=NORMAL)

            print(self.round_capital_list[count][1])

            self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):

        selected = self.round_capital_list[user_choice]

        if selected == self.correct_answer:
            self.results_label.config(text="Correct! ✅", bg="#C6EFCE")
            self.quiz_score.set(self.quiz_score.get() + 1)
        else:
            self.results_label.config(
                text=f"Wrong ❌\nCorrect: {self.correct_answer}",
                bg="#FFC7CE"
            )

        # Disable buttons after answering
        for button in self.capital_button_ref:
            button.config(state=DISABLED)

        self.next_button.config(state=NORMAL)

        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.capital_button_ref:
            item.config(state=DISABLED)

        self.score_label.config(text=f"Score: {self.quiz_score.get()}")

    def close_play(self):

        root.deiconify()
        self.play_box.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Capital Quiz")
    StartGame()
    root.mainloop()
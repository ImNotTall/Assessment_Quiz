from tkinter import *

class StartGame:

    def __init__(self):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        intro_string = ("Enter the number of round you would like to play. If you would like to try for a high "
                        "score, press the infinite mode. Each round you will be given a random country then " 
                        "you select from one of the four buttons what capital responds to said country.\n\n"

                        "Your goal is to get as many countries correct and get the highest score possible. "
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

        self.infinite_mode_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#E33C38", text="Infinite Mode! 🔥", width=25,
                                  command=self.check_rounds)
        self.infinite_mode_button.grid(row=1, column=0, pady=2, columnspan=2,
                                       command=self.infinite_mode)

    def check_rounds(self):

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
            self.choose_label.config(text=error, fg="990000",
                                     font=("Arial", 10, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                        font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):

        root.deiconify()
        self.play_box.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Capital Quiz")
    StartGame()
    root.mainloop()
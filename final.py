import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist

# incase you run it for the first time
# nltk.download('punkt')
# nltk.download('stopwords')

# Customization options
style_settings = {
    "background_color": "#000",
    "label_font_size2":16,
    "text_color": "#fff",
    "button_color": "#86BAA1",
    "label_font_size": 16,
    "text_input_font_size": 12,
    "width": 50,
    "height": 10,
    "text_size": 12,
    "font": "verdana",  # Change the font to your preferred font
    "slider_bg": "#A0E8AF",  # Background color for the slider
    "button_copy_color": "#000",
}


def text_summarizer(text, num_sentences=5):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    # Calculate word frequency
    freq = FreqDist(words)

    # Assign a score to each sentence based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in freq.keys():
            if word in sentence.lower():
                if sentence in sentence_scores:
                    sentence_scores[sentence] += freq[word]
                else:
                    sentence_scores[sentence] = freq[word]

    # Get the top N sentences with the highest scores
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    # Join the summary sentences to create the final summary
    summary = ' '.join(summary_sentences)
    return summary


class TextSummarizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarizer")
        self.num_sentences_label = None  # Initialize the attribute
        self.create_widgets()

    def create_widgets(self):
        # Left Column
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.text_input_label = tk.Label(left_frame, text="Enter Text:", fg=style_settings["text_color"],
                                         font=(style_settings["font"], style_settings["label_font_size"]))
        self.text_input_label.grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.text_input = tk.Text(left_frame, wrap=tk.WORD, width=style_settings["width"],
                                  height=style_settings["height"],
                                  font=(style_settings["font"], style_settings["text_input_font_size"]))
        self.text_input.grid(row=1, column=0, pady=5, sticky="nsew")

        # Right Column
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.slider_label = tk.Label(right_frame, text="Number of Sentences:", fg=style_settings["text_color"],
                                     font=(style_settings["font"], style_settings["label_font_size"]))
        self.slider_label.grid(row=0, column=0, pady=(10, 5), sticky="w", padx=(0, 0))

        self.slider_var = tk.IntVar()
        self.slider = ttk.Scale(right_frame, from_=1, to=99, variable=self.slider_var, orient=tk.HORIZONTAL,
                                length=200, command=self.update_slider_bg)
        self.slider.set(5)  # Default value
        self.slider.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        self.num_sentences_label = tk.Label(right_frame, text=int(self.slider_var.get()),
                                            fg=style_settings["text_color"],
                                            font=(style_settings["font"], style_settings["label_font_size2"]))
        self.num_sentences_label.grid(row=0, column=0, pady=(10, 5), padx=(190, 0), sticky="w")

        # Summarize Button
        self.summarize_button = tk.Button(right_frame, text=" Summarize ", command=self.summarize_text,
                                          bg=style_settings["button_color"], fg=style_settings["button_copy_color"])
        self.summarize_button.grid(row=2, column=0, pady=(0, 5), sticky="nsew")

        # Copy Summary Button
        self.copy_button = tk.Button(right_frame, text=" Copy ", command=self.copy_summary,
                                     bg=style_settings["button_color"], fg=style_settings["button_copy_color"])
        self.copy_button.grid(row=3, column=0, pady=(0, 5), sticky="nsew")
        
        # ahmed sleem Button
        self.copy_button = tk.Button(right_frame, text=" made by Ahmed Sleem ",
                                     bg=style_settings["button_color"], fg=style_settings["button_copy_color"])
        self.copy_button.grid(row=4, column=0, pady=(33, 5), sticky="nsew")



        # Result Display
        result_frame = tk.Frame(self.root)
        result_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self.result_label = tk.Label(result_frame, text="Summary:", fg=style_settings["text_color"],
                                     font=(style_settings["font"], style_settings["label_font_size"]))
        self.result_label.grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, width=style_settings["width"],
                                   height=style_settings["height"],
                                   font=(style_settings["font"], style_settings["text_size"]))
        self.result_text.grid(row=1, column=0, pady=5, sticky="nsew")

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def update_slider_bg(self, event):
        # Update the label text to display the integer value of the slider
        self.num_sentences_label["text"] = int(self.slider_var.get())

    def summarize_text(self):
        input_text = self.text_input.get("1.0", tk.END)
        num_sentences = self.slider_var.get()
        summary = text_summarizer(input_text, num_sentences)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, summary)

    def copy_summary(self):
        summary = self.result_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(summary)
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizerGUI(root)
    root.geometry("1200x300")
    root.mainloop()
    
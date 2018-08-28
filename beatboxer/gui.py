from inspect import getsourcefile
from os import path, remove, listdir
from tempfile import mkdtemp
import winsound

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askdirectory

from beatboxer import BeatBoxer


CUR_DIR = path.dirname(path.abspath(getsourcefile(lambda: 0)))
ROOT = CUR_DIR[:CUR_DIR.rfind(path.sep)]
ONESHOT_PATH = path.join(ROOT, 'beatboxer', 'samples')
ONESHOTS = [''] + list(map(lambda x: x.split('.')[0], listdir(ONESHOT_PATH)))
ICON_PATH = path.join(ROOT, 'beatboxer', 'icon', 'icon.ico')


class Window(tk.Frame):

    def __init__(self, parent):
        """
        Main window of the GUI.
        """
        super().__init__(parent)
        self.parent = parent
        self.parent.title('BeatBoxer')
        self.parent.iconbitmap(ICON_PATH)

        self.initialize()
        self.make_menu()

    def initialize(self):
        ## TOP HALF ##
        # Initialize with 3 tracks and 8 beats
        self.top_frame = TrackListing(self.parent, 3, 8)
        self.top_frame.grid(row=1, columnspan=3)

        ## BOTTOM HALF ##
        # TO BE USED LATER
        self.bot_frame = tk.Frame(self.parent)
        self.bot_frame.grid(row=2)
        self.bot_frame.config(background='green')

        ## HEADER ##
        # BPM
        self.bpm_text = tk.Label(self.parent, text='BPM:')
        self.bpm_text.grid(row=0, sticky=tk.E)
        self.bpm = tk.Entry(self.parent, width=4)
        self.bpm.grid(row=0, column=1, sticky=tk.W)
        self.bpm.insert(0, 240)
        # Preview what the measure sounds like
        self.preview = tk.Button(self.parent, text='Preview',
            command=lambda: self.top_frame.preview_measure(int(self.bpm.get())))
        self.preview.grid(row=0, column=2)
        self.parent.bind('<Control-p>',
            lambda event: self.top_frame.preview_measure(int(self.bpm.get())))

    def make_menu(self):
        # Menu comes last to reference self.top_frame
        menu = tk.Menu(self.parent)

        # FILE MENU
        filemenu = tk.Menu(menu, tearoff=0)
        filemenu.add_command(label='Save', accelerator='Ctrl-S',
            command=lambda event: self.top_frame.save_measure)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', accelerator='Ctrl-Q',
            command=lambda event: self.parent.destroy())
        self.parent.bind('<Control-s>',
            lambda event: self.top_frame.save_measure(int(self.bpm.get())))
        self.parent.bind('<Control-q>', lambda event: self.parent.destroy())

        # EDIT MENU
        self.editmenu = tk.Menu(menu, tearoff=0)
        self.editmenu.add_command(label='Add track', accelerator='Ctrl-T',
            command=self.top_frame.add_track)
        self.editmenu.add_command(label='Change number of beats', accelerator='Ctrl-B',
            command=self.change_num_beats)
        self.parent.bind('<Control-t>', self.top_frame.add_track)
        self.parent.bind('<Control-b>', self.change_num_beats)

        # Put it all together
        menu.add_cascade(label='File', menu=filemenu)
        menu.add_cascade(label='Edit', menu=self.editmenu)
        self.parent.config(menu=menu)

    def change_num_beats(self, event=None):
        """
        Command to change the number of beats per the measure
        """
        # Popup window to enter the number of beats
        beats_popup = BeatsPopup(self.parent)
        self.parent.wait_window(beats_popup.top)

        # Create the new frame and add it, if window isn't exited out of
        if beats_popup.num_beats is not None:
            # Remove the old frame
            self.top_frame.destroy()

            # Set the new frame and place in the spot of the old one
            self.top_frame = TrackListing(self.parent, self.top_frame.height,
                beats_popup.num_beats)
            self.top_frame.grid(row=1, columnspan=3)

            # Reset the command for adding tracks, without the command will point
            # to the destroyed widget
            self.editmenu.entryconfig(0, command=self.top_frame.add_track)
            self.parent.bind('<Control-t>', self.top_frame.add_track)


class TrackListing(tk.Frame):

    def __init__(self, parent, height, width):
        """
        The upper-half of the GUI with the tracks and their beats
        """
        super().__init__(parent)
        self.parent = parent
        self.height = height
        self.width = width

        self.initialize()

    def initialize(self):
        # Build each row
        for row in range(self.height):
            Track(self, self.parent, row + 1, self.width)

    @property
    def tracks(self):
        """
        A list of every Track object
        """
        return list(filter(lambda x: type(x) == Track, self.winfo_children()))

    @property
    def measure(self):
        """
        A list of the measure as the syntax of Beatbox.make_a_beat. Each element
        of the list is a list of every oneshot on that beat.
        """
        # Make the measure
        measure = [[] for _ in range(self.width)]

        # Get the tracks
        for track in self.tracks:
            # Get the beats
            for ind, beat in enumerate(track.beats):
                beat = beat.get()
                # If the beat isn't blank, add it to the list
                if beat:
                    measure[ind].append(beat)

        return measure

    def add_track(self, event=None):
        # Make sure to increase the height by one
        self.height += 1
        Track(self, self.parent, self.height, self.width)

    def remove_track(self, track_frame, parent):
        # Row number changes for tracks below track currently being deleted
        for track in self.tracks[parent.row:]:
            # Unbind the hotkey since the number changes and then rebind
            track.unset_binding()
            track.row -= 1
            track.set_binding()
        # Make sure to decrease the height by one
        self.height -= 1

        # Destroy all the children (The button and every beat)
        for child in track_frame.winfo_children():
            child.destroy()

        # And destroy space holding the children it (otherwise space stays used)
        # And it's parent (the Track object)
        track_frame.destroy()
        parent.destroy()

    def preview_measure(self, bpm):
        # Play it in the popup
        preview_popup = PreviewPopup(self.parent, self.measure, bpm, self.width)

    def save_measure(self, bpm):
        bb = BeatBoxer(bpm=bpm)
        bb.make_a_beat(self.measure)
        # Get the directory path and name to save audio file as
        save_path, name = path.normpath(asksaveasfilename(
            defaultextension='.wav', filetypes=[('WAV', '.wav')])
            ).rsplit(path.sep, 1)
        # Then save it
        bb.save_beat(name=name.split('.')[0], save_path=save_path)


class Track(tk.Frame):

    def __init__(self, parent, gparent, row, num_cols):
        """
        Each row of the track listing
        """
        super().__init__(parent)
        self.parent = parent
        self.gparent = gparent
        self.row = row
        self.num_cols  = num_cols

        self.initialize()

    def initialize(self):
        # Create a 'sub'-parent Frame so that there is a parent to destroy
        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        # Remove track button
        remove = tk.Button(self.frame, text='Remove track')
        remove.config(command=lambda parent=self, track=self.frame:
            self.parent.remove_track(track, parent))
        remove.grid(row=0, column=0)
        self.set_binding()

        # Each beat of the track
        self.beats = []
        for col in range(self.num_cols):
            var = tk.StringVar()
            var.set('')
            self.beats.append(var)
            beat = tk.OptionMenu(self.frame, var, *ONESHOTS)
            beat.config(font=('calibri', 12), bg='grey', width=6)
            beat.grid(row=0, column=col + 1)

    def set_binding(self):
        """
        Set the hotkey for deleting the Track based on its current row
        """
        self.hotkey = '<Control-Key-{}>'.format(self.row)
        self.binding = self.gparent.bind(self.hotkey,
            lambda event, parent=self, track=self.frame:
            self.parent.remove_track(track, parent))

    def unset_binding(self):
        """
        Unset hotkey set by self.set_binding when Track's row changes
        """
        self.hotkey = '<Control-Key-{}>'.format(self.row)
        self.gparent.unbind(self.hotkey, self.binding)


class BeatsPopup:

    def __init__(self, parent):
        """
        Popup window for changing the number of beats.
        """
        self.top = tk.Toplevel(parent)
        self.top.iconbitmap(ICON_PATH)
        self.top.title('')
        self.top.protocol('WM_DELETE_WINDOW', self.close)
        self.top.bind('<Escape>', self.close)

        self.initialize()

    def initialize(self):
        self.beats_label = tk.Label(self.top, text='Number of beats per measure:')
        self.beats_label.pack(padx=3)

        self.beats = tk.Entry(self.top)
        self.beats.focus_set()
        self.beats.pack(pady=5)

        # Press enter to accept the number of beats
        self.top.bind('<Return>', self.send)
        self.beats_button = tk.Button(self.top, text='Submit', command=self.send)
        self.beats_button.pack(pady=5)

    def send(self, event=None):
        # Do nothing if not a number or if is 0
        if not self.beats.get().isdigit() or not int(self.beats.get()):
            return

        self.num_beats = int(self.beats.get())
        self.top.destroy()

    def close(self, event=None):
        self.num_beats = None
        self.top.destroy()


class PreviewPopup:

    def __init__(self, parent, measure, bpm, width, size=200):
        """
        Popup window for the playback of the measure where `measure` is the list
        that BeatBox.make_a_beat takes, `bpm` is self-explanatory, `width` is
        the number of beats per the measure, `size` is the size of the window.
        """
        self.measure = measure
        self.bpm = bpm
        self.spb = 60 / self.bpm
        self.width = width
        self.size = size

        self.top = tk.Toplevel(parent)
        # Keep the size fixed
        self.top.resizable(height=False, width=False)
        self.top.geometry('{size}x{size}'.format(size=self.size))
        self.top.iconbitmap(ICON_PATH)
        self.top.title('')
        # Run self.close when exited out
        self.top.protocol('WM_DELETE_WINDOW', self.close)
        # Can exit out with Esc key
        self.top.bind('<Escape>', self.close)
        self.top.focus_set()

        self.initialize()

    def initialize(self):
        # Length as a fraction of the size of the window
        csize = 0.85
        self.canvas = tk.Canvas(self.top)
        # The divisor line, scales with self.size
        self.canvas.create_line(csize * self.size, (1 - csize) * self.size,
            (1 - csize) * self.size, csize * self.size, width=10)
        # The current beat, get the ID for the text in the canvas object
        self.cur_beat_id = self.canvas.create_text(70, 70, text='1', font=('Courier', 30))
        # The value of the current beat
        self.cur_beat = 1
        # The total number of beats a.k.a self.width
        self.canvas.create_text(130, 130, text=self.width, font=('Courier', 30))
        self.canvas.pack()

        # Make BeatBoxer object to create audio file and save to temp dir
        self.bb = BeatBoxer(bpm=self.bpm, save_path=mkdtemp())
        self.bb.make_a_beat(self.measure, num_measures=1)
        self.bb.save_beat('tmp')
        tmp_file = path.join(self.bb.save_path, 'tmp.wav')
        winsound.PlaySound(tmp_file, winsound.SND_ASYNC|winsound.SND_LOOP)

        # Increment the value of the current beat with this
        self.top.after(int(1000 * self.spb), self.increment_beat)

    def increment_beat(self):
        # Increment the current beat and change canvas item
        self.cur_beat = self.cur_beat % self.width + 1
        self.canvas.itemconfig(self.cur_beat_id, text=self.cur_beat)
        self.top.after(int(1000 * self.spb), self.increment_beat)

    def close(self, event=None):
        winsound.PlaySound(None, winsound.SND_FILENAME)
        self.num_beats = None
        self.top.destroy()


def gui():
    root = tk.Tk()
    window = Window(root)
    root.mainloop()


if __name__ == "__main__":
    gui()

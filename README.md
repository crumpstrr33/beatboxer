# Beatboxer
I don't have the money (or talent) to use FL Studios or the patience to learn anything else. Luckily I already know Python so here's my solution.

Make beats just by indicating on what beat what sound should be played. It's pretty simple, trust me.

What uses does this have you ask me? Lots! Quickly supply dope beats for rap battles, bangers for that quick crunk sesh, backtracks for your SoundCloud rapper aspirations with that classic syncopated subbass rhythym, use it as a glorified and versatile metronome and so on!

## Installing Package
Just do it the classic way:
```
pip install beatboxer
```

## Example
Here's an example ripped straight from the `main` function:

First, create the object.
``` python
from inspect import getsourcefile
from os import path
    
from beatboxer import BeatBoxer

# Create directory to save audio into
save = path.join(path.dirname(path.abspath(getsourcefile(lambda: 0))), 'outputs')

# Create object with 120 beats per minute and quarter note as one beat
b = BeatBoxer(bpm=120, base_note=4, save_path=save)
```

Now let's make some beats. This first one has 16 beats and one measure in 16/4 time and
1) Every beat plays a hihat
2) Every 3rd beat starting on the 2nd beat plays a kick
3) Every 4th beat starting on the 2nd beat plays a snare
4) Every 8th beat starting on the 1st beat plays a crash
``` python
b.make_a_beat(b.empty(), num_measures=1, every_beat=['hihat'],
    every_4th=[('snare', 1)], every_3rd=[('kick', 1)], every_8th=[('crash', 0)])
# Store it with the name 'dope1'
b.store_beat('dope1')
```

Let's make a second beat! We'll only change the time signature to 16/8 and play it for 4 measures. This beat will play twice as fast as the first beat. And let us throw a clap on the 7th and 11th beat.
``` python
b.change_base_note(8)
b.make_a_beat(b.empty(), num_measures=4, single={'clap': [7, 11]}, every_beat=['hihat'],
    every_4th=[('snare', 1)], every_3rd=[('kick', 1)], every_8th=[('crash', 0)])
# Store it with the name 'dope2'
b.store_beat('dope2')
```

One last beat. We'll change the BPM to 100 and the time signature to 3/8 for 12 measures.
``` python
b.change_bpm(100)
b.make_a_beat(b.empty(3), num_measures=12, every_beat=['hihat'], every_3rd=[('snare', 2), ('kick', 1)])
# Store it with the name 'lastly dope'
b.store_beat('lastly dope')
```

And we'll save our favorite, the second one as `dopest.wav`.
``` python
b.save_beat('dopest', b.stored_beats['dope2'])
```

If you print the object, it'll show the stored and current beats.
``` python
print(b)
```
This outputs:
```
---------Current Beat--------
BPM: 100 --- Time Signature: 3/8 --- Number of Measures: 12 --- Length: 10.981 s

---------Stored Beats--------
Name: dope1       --- BPM: 120 --- Time Signature: 16/4 --- Number of Measures:  1 --- Length:  8.106 s
Name: dope2       --- BPM: 120 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 16.106 s
Name: lastly dope --- BPM: 100 --- Time Signature:  3/8 --- Number of Measures: 12 --- Length: 10.981 s
```

Ahhh wait... even though the second one is like Kanye-level quality, the first needs work... So let's edit it.
``` python
# First switch it to the current beat
b.switch_current_beat('dope1', force=True)

# Remove every snare and every 2nd hihat. Then add a bass on every kick and
# re-add the snare on every 4th note but with a 2 beat offset.
b.edit_current_beat(bpm=140, base_note=8, num_measures=4, remove={
    'every_beat': ['snare'], 'every_2nd': [('hihat', 1)]
    }, add={
        'every_3rd': [('bass', 1)], 'every_4th': [('snare', 2)]
    })
# Now, there is still the original 'dope1' beat in b.stored_beats. We can
# either overwrite it with this or store as a new one like so:
b.store_beat('way better than dope1')
# And lets save that bad boy
b.save_beat('dopestest')

print('\n\nDid some editting...')
print(b)
```

And the final output will be:
```
Did some editting...
---------Current Beat--------
BPM: 140 --- Time Signature: 16/8 --- Number of Measures: 4 --- Length: 13.696 s

---------Stored Beats--------
Name: dope1                 --- BPM: 120 --- Time Signature: 16/4 --- Number of Measures:  1 --- Length:  8.106 s
Name: dope2                 --- BPM: 120 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 16.106 s
Name: lastly dope           --- BPM: 100 --- Time Signature:  3/8 --- Number of Measures: 12 --- Length: 10.981 s
Name: way better than dope1 --- BPM: 140 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 13.696 s
```

## Using the GUI
I'm not going to use picture here for the present since the GUI will most likely change drastically soon. But it is used like so:
- The grid shows the number of beats per measure and you can choose what plays on each beat of the measure.
- If you want more sounds played on a specific beat that are available, go to `Edit` and `Add Track` or `Ctrl-T` to add another track to use.
- If you want to have more or less beats per measure, go to `Edit` and `Change Number of Beats` or `Ctrl-B` to change the number of beats.
- You can remove a track with the `Remove Track` button or with the hotkey `Ctrl-<row>` where `<row>` is the row of the track.
- You can preview what the measure sounds like with the `Preview` button where it will play the measure on loop while showing the current beat.
- And you can save your measure as a WAV file with `File` then `Save` or `Ctrl-S`.

That's what I got so far, fellas. Stay tuned.

## Future Aspirations
Find the meaning to life.


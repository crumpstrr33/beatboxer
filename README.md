# Beatboxer
I don't have the money (or talent) to use FL Studios or the patience to learn anything else. Luckily I already know Python so here's my solution.

Make beats just by indicating on what beat what sound should be played. It's pretty simple, trust me.

What uses does this have you ask me? Lots! Quickly supply dope beats for rap battles, bangers for that quick crunk sesh, backtracks for your SoundCloud rapper aspirations with that classic syncopated subbass rhythym, use it as a glorified and versatile metronome and so on!

## Example
Here's an example ripped straight from the `main` function:
``` python
    from inspect import getsourcefile
    from os import path
    
    from beatboxer import BeatBoxer

    # Create directory to save audio into
    save = path.join(path.dirname(path.abspath(getsourcefile(lambda: 0))), 'outputs')

    # Create object with 120 beats per minute and quarter note as one beat
    b = BeatBoxer(bpm=120, base_note=4, save_path=save)

    # Create audio with 16 beats off an empty template for one measure:
    #     1) Every beat play a hihat
    #     2) Every 4th beat starting on the 2nd beat plays a snare
    #     3) Every 3rd beat starting on the 2nd beat plays a snare
    #     4) Every 8th beat starting on the 1st beat plays a crash
    # Time signature will be 16/4
    b.make_a_beat(b.empty(), num_measures=1, every_beat=['hihat'],
        every_4th=[('snare', 1)], every_3rd=[('kick', 1)], every_8th=[('crash', 0)])
    b.store_beat('dope1')

    # Change to having an eight note as one beat
    b.change_base_note(8)
    # Create same thing as before but it will now be twice as fast with a 
    # time signature of 16/8 and played for 4 measures
    b.make_a_beat(b.empty(), num_measures=4, every_beat=['hihat'],
        every_4th=[('snare', 1)], every_3rd=[('kick', 1)], every_8th=[('crash', 0)])
    b.store_beat('dope2')

    # Change to 100 beats per minute
    b.change_bpm(100)
    # Now have a time signature of 3/8 for 12 measures
    b.make_a_beat(b.empty(3), num_measures=12, every_beat=['hihat'],
        every_3rd=[('snare', 2), ('kick', 1)])
    b.store_beat('lastly dope')

    # Save one of the beats
    b.save_beat('dopest', b.stored_beats['dope2'])

    # Printing the object will display the stored and current beat(s)
    print(b)

    # Second one is great but I don't like the first one, let's edit it...
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
The output will be:
```
---------Current Beat--------
BPM: 100 --- Time Signature: 3/8 --- Number of Measures: 12 --- Length: 10.981 s

---------Stored Beats--------
Name: dope1       --- BPM: 120 --- Time Signature: 16/4 --- Number of Measures:  1 --- Length:  8.106 s
Name: dope2       --- BPM: 120 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 16.106 s
Name: lastly dope --- BPM: 100 --- Time Signature:  3/8 --- Number of Measures: 12 --- Length: 10.981 s



Did some editting...
---------Current Beat--------
BPM: 140 --- Time Signature: 16/8 --- Number of Measures: 4 --- Length: 13.696 s

---------Stored Beats--------
Name: dope1                 --- BPM: 120 --- Time Signature: 16/4 --- Number of Measures:  1 --- Length:  8.106 s
Name: dope2                 --- BPM: 120 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 16.106 s
Name: lastly dope           --- BPM: 100 --- Time Signature:  3/8 --- Number of Measures: 12 --- Length: 10.981 s
Name: way better than dope1 --- BPM: 140 --- Time Signature: 16/8 --- Number of Measures:  4 --- Length: 13.696 s


```

## Future Aspirations
Lol, suggestions welcomed.


from nose.tools import assert_equals, assert_in, assert_true
import itertools

NOTES = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]

def distance(note1, note2):
  """Returns the number of semitones between note1 and note2."""
  a = NOTES.index(note1)
  b = NOTES.index(note2)
  if b < a:
    b += len(NOTES)
  return b - a

def note_up(note, dist):
  """Return the note $dist semitones above $note."""
  return NOTES[(NOTES.index(note) + dist) % len(NOTES)]

def fingers_for_note(target):
  """Given a note, output (mandolin string, fret number) pairs that produce it when strummed."""
  bases = ["G", "D", "A", "E"]
  output = set()
  for i in range(16):
    for note in bases:
      if (NOTES.index(note) + i) % len(NOTES) == NOTES.index(target):
        output.add((note, i))
  return output

def notes_in_chord(chord):
  """Given a chord like 'A' or 'Gbm', return the three notes in it."""
  targets = []
  if chord[-1] == "m":
    targets.append(chord[:-1])
    targets.append(note_up(targets[0], 3))
    targets.append(note_up(targets[0], 7))
  else:
    targets.append(chord)
    targets.append(note_up(targets[0], 4))
    targets.append(note_up(targets[0], 7))
  return targets

def fingers_for_chord(chord, n):
  """$chord: the chord to find fingering for. $n: how many fingerings to return."""
  targets = set(notes_in_chord(chord))
  options = []

  # Each (g, d, a, e) tuple is a possible fingering of the fretboard.
  # A fingering is the fret being held down for each string of the mandolin.
  for g, d, a, e in itertools.product(range(16), range(16), range(16), range(16)):
    positions = {"G": g, "D": d, "A": a, "E": e}

    # Check if holding down frets g, d, a and e will produce the notes in the chord
    notes = [note_up(note, i) for note, i in positions.items()]
    if targets == set(notes):
      options.append((g, d, a, e))

  # Sort ways to play that chord, return the top n
  options.sort(key=lambda option: max(option) - min(option))
  for option in options[:n]:
    ma, mi = max(option), min(option)
    yield (option, [note_up(n,i) for n,i in zip(["G", "D", "A", "E"], option)])

def test_notes_in_chord():
  assert_equals(["F", "A", "C"], notes_in_chord("F"))
  assert_equals(["F", "Ab", "C"], notes_in_chord("Fm"))

def test_distance():
  assert_equals(1, distance("A", "Bb"))
  assert_equals(2, distance("A", "B"))
  assert_equals(10, distance("B", "A"))
  assert_equals(11, distance("A", "Ab"))
  assert_equals(9, distance("A", "Gb"))
  assert_equals(1, distance("B", "C"))
  assert_equals(11, distance("C", "B"))

def test_fingers_for_note():
  assert_in(("G", 7), fingers_for_note("D"))
  assert_in(("D", 7), fingers_for_note("A"))
  assert_equals(set([
    ("A", 1),
    ("E", 6),
    ("A", 13),
    ("G", 3),
    ("G", 15),
    ("D", 8),
    ]), fingers_for_note("Bb"))
  assert_equals(set([
    ("D", 6),
    ("G", 1),
    ("E", 4),
    ("A", 11),
    ("G", 13),
    ]), fingers_for_note("Ab"))
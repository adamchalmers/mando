import music
import click

@click.group()
def cli():
  """Mando is a tool for finding mandolin chords."""
  pass

@cli.command()
@click.argument("note1")
@click.argument("note2")
def dist(note1, note2):
  """Outputs the number of semitones between note1 and note2."""
  click.echo(music.distance(note1, note2))

@cli.command()
@click.argument("note")
def note(note):
  """Outputs (string, fret) pairs which produce the given note."""
  positions = music.fingers_for_note(note)
  out = "\n".join([note + str(pos) for note, pos in positions])
  click.echo(out)

@cli.command()
@click.option("--verbose", is_flag=True, help="Prints extra information.")
@click.argument("chord")
@click.argument("n", default=5)
def chord(verbose, chord, n):
  """Outputs (G, D, A, E) fingerings for the given chord."""
  if verbose:
    click.echo("The chord %s has notes %s" % (chord, ", ".join(music.notes_in_chord(chord))))
  for fingering, notes in music.fingers_for_chord(chord, n):
    if verbose:
      click.echo ("%s plays %s" % (fingering, ", ".join(notes)))
    else:
      click.echo(" ".join([str(x) for x in fingering]))

if __name__ == "__main__":
  cli()
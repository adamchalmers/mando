import music
import click

@click.group()
def cli():
  pass

@cli.command()
@click.argument("note1")
@click.argument("note2")
def dist(note1, note2):
  click.echo(music.distance(note1, note2))

@cli.command()
@click.argument("note")
def note(note):
  positions = music.fingers_for_note(note)
  out = ", ".join([note + str(pos) for note, pos in positions])
  click.echo(out)

@cli.command()
@click.argument("chord")
@click.argument("n", default=5)
def chord(chord, n):
  click.echo("The chord %s has notes %s" % (chord, ", ".join(music.notes_in_chord(chord))))
  for fingering, notes in music.fingers_for_chord(chord, n):
    click.echo ("%s plays %s" % (fingering, ", ".join(notes)))

if __name__ == "__main__":
  cli()
<h1>Mando</h1>
Mando is a little command line tool for learning mandolin. It can help you find nice ways to play chords, figure out the fretting for a certain note, or find easy chord progressions. Eventually it'll do more. I hope.

<h2>Usage</h2>

```
$ python cli.py progressions "G C D"
G: 0,0,2,3	C: 0,2,3,0	D: 2,0,0,2
G: 0,0,2,3	C: 0,2,3,0	D: 7,0,0,2
G: 0,0,2,3	C: 0,2,3,0	D: 11,0,0,2
G: 0,0,2,3	C: 0,2,3,0	D: 11,0,0,5
G: 0,0,2,3	C: 0,5,3,0	D: 2,0,0,2

$ python cli.py chord Abm
The chord Abm has notes Ab, B, Eb
(4, 6, 6, 4) plays B, Ab, Eb, Ab
(8, 6, 6, 7) plays Eb, Ab, Eb, B
(1, 1, 2, 4) plays Ab, Eb, B, Ab
(4, 1, 2, 4) plays B, Eb, B, Ab
(4, 6, 6, 7) plays B, Ab, Eb, B

$ python cli.py note C#
A4
G6
E9
D11
```

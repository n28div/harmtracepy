# Running the docker
Create the docker with

`docker build -t harmtracepy .`

Run the docker with

`docker run -d --name harmtracepy harmtracepy`

Test the docker with

`docker exec harmtracepy stack exec harmtrace parse -- --grammar=jazz --chords="C:maj D:min;1 G:7;2 C:maj;1"`

the result should contain something in the line of

```
parsed 3 chords into 1 analysis tree(s)
[Piece[PD[D_1_1[S_1par_1[IIm_1[D:min]]][D_2_1[V7_2[G:7]]]]][PT[T_1_1[I_1[C:maj]]]]]
```


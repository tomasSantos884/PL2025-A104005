program Tabuada;
var
  i, n: integer;
begin
  writeln('Introduza um número inteiro:');
  readln(n);
  for i := 1 to 10 do
    writeln(n, ' x ', i, ' = ', n * i);
end.
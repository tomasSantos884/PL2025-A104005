program ParOuImpar;
var
  n: integer;
begin
  writeln('Introduza um número inteiro:');
  readln(n);
  if n mod 2 = 0 then
    writeln(n, ' é par')
  else
    writeln(n, ' é ímpar');
end.
program Teste;
var 
a: array[0..2] of integer;
begin
  a[0] := 5;
  a[1] := a[0] + 2;
  writeln(a[1]);
end.
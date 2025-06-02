program grades;
var
  marks : integer;
  grade : char;
begin
  write('Enter marks: ');
  readln(marks);

  if marks >= 75 then
    grade := 'A'
  else if marks >= 65 then
    grade := 'B'
  else if marks >= 55 then
    grade := 'C'
  else if marks >= 40 then
    grade := 'S'
  else
    grade := 'W';

  writeln('Your grade: ', grade);
end.
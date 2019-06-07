.sub Println
.param pmc str
$P1 = str
say $P1
.end

.sub len
  .param pmc array
  elements $I0, array
  .return($I0)
.end
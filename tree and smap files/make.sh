# treefixDTL simulations -- unused
cp -p ~/work/treefixDTL/config/strees/S1.stree ./
cp -p ~/work/treefixDTL/config/S.smap ./

cp -p ~/work/treefixDTL/data/sim/Seqlength333/lowDTL/height1/G1/G1.pep.raxml.boot.rangerDTL.tree ./
cp -p ~/work/treefixDTL/data/sim/Seqlength333/lowDTL/height1/G1/G1.pep.raxml.boot.rangerDTL.recon ./

cp -p  ~/work/treefixDTL/data/sim/Seqlength333/lowDTL/height1/G1/G1.pep.raxml.mowgli.tree ./
cp -p  ~/work/treefixDTL/data/sim/Seqlength333/lowDTL/height1/G1/G1.pep.raxml.mowgli.brecon ./


vistrans -s S1.stree -S S.smap -t G1.pep.raxml.mowgli.tree -b G1.pep.raxml.mowgli.brecon
vistrans -s S1.stree -S S.smap -t G1.pep.raxml.boot.rangerDTL.tree -r G1.pep.raxml.boot.rangerDTL.recon    # does not work



# simple case -- works
echo '((A:1,B:1):2,C:3)' > test.stree
echo '(a_1,(b_1,c_1))' > test.tree
echo -e 'a_*\tA\nb_*\tB\nc_*\tC' > test.smap

cp ~/work/treefixDTL/bin/run-mowgli ./
cp ~/work/treefixDTL/bin/run-mowgli-with-map ./
./run-mowgli-with-map -s test.stree -S test.smap \
    -U .tree -T .mowgli.tree -O .mowgli.output \
    --extra "-d 2 -t 3 -l 1 -C" test.tree
vistrans -s test.stree -S test.smap -t test.mowgli.tree -b test.mowgli.brecon

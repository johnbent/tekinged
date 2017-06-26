infile=$1
inname=`convert -ping "$infile" -format "%t" info:`
suffix=`convert -ping "$infile" -format "%e" info:`
convert "$infile" -auto-level -morphology smooth diamond:1 \
-background white -deskew 40% +repage \
-fuzz 10% -trim +repage tmp.png
OIFS=$IFS
IFS=$'\n'
white_arr=(`convert tmp.png -auto-level -scale x1! txt: |\
tail -n +2 | tr -cs "0-9\n" " " | grep -e '.* .* 255'`)
echo "${white_arr[*]}"
num=${#white_arr[*]}
IFS=$OIFS
middle=`convert xc: -format "%[fx:round($num/2)]" info:`
echo "middle=$middle"
xcrop=`echo "${white_arr[$middle]}" | cut -d\  -f1`
echo "xcrop=$xcrop"
ww=`convert -ping tmp.png -format "%w" info:`
hh=`convert -ping tmp.png -format "%h" info:`
ww1=$((xcrop+1))
dim1="${ww1}x${hh}+0+0"
ww2=`convert xc: -format "%[fx:$ww-$xcrop-1]" info:`
xoff2=$ww1
dim2="${ww2}x${hh}+${xoff2}+0"
echo "dim1=$dim1; dim2=$dim2;"
convert tmp.png \
\( -clone 0 -crop $dim1 +repage -write ${inname}_left.$suffix \) \
\( -clone 0 -crop $dim2 +repage -write ${inname}_right.$suffix \) \
null:
rm -f tmp.png


dim1=`convert ${inname}_left.$suffix -scale 1x! -scale 2x! -negate -fuzz 18% -format "%@" info:`
echo $dim1
dim1=`echo "$dim1" | sed -n 's/^2x\(.*\)$/\1/p'`
echo $dim1
ht=`echo "$dim1" | cut -d+ -f1`
yoff=`echo "$dim1" | cut -d+ -f3`
echo "ht=$ht; yoff=$yoff;"
y1=`convert xc: -format "%[fx:($yoff-50)<0?0:($yoff-50)]" info:`
y2=`convert xc: -format "%[fx:($ht+$yoff+50)>$hh?$hh:($ht+$yoff+50)]" info:`
echo "y2=$y2; y1=$y1;"
ht=$((y2-y1))
dim1="${ww1}x${ht}+0+$y1"
echo $dim1
convert ${inname}_left.$suffix -crop $dim1 +repage -trim +repage -bordercolor white -border 20 ${inname}_left.$suffix

dim2=`convert ${inname}_right.$suffix -scale 1x! -scale 2x! -negate -fuzz 18% -format "%@" info:`
echo $dim2
dim2=`echo "$dim2" | sed -n 's/^2x\(.*\)$/\1/p'`
echo $dim2
ht=`echo "$dim2" | cut -d+ -f1`
yoff=`echo "$dim2" | cut -d+ -f3`
echo "ht=$ht; yoff=$yoff;"
y1=`convert xc: -format "%[fx:($yoff-50)<0?0:($yoff-50)]" info:`
y2=`convert xc: -format "%[fx:($ht+$yoff+50)>$hh?$hh:($ht+$yoff+50)]" info:`
echo "y2=$y2; y1=$y1;"
ht=$((y2-y1))
dim2="${ww2}x${ht}+0+$y1"
echo $dim2
convert ${inname}_right.$suffix -crop $dim2 +repage -trim +repage -bordercolor white -border 20 ${inname}_right.$suffix

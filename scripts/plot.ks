GNUPlot_Update_Func() {
#------ Client Disk Allocation and Utilization vs. Time ------
  $MYSQL --column-names=0 -u$DBUSER -p$DBPASS $DBNAME &lt;&lt; EOF | while read HOSTNAME
  SELECT DISTINCT host_name FROM sandisk_clients ORDER BY host_name;
  EOF
  do
    $MYSQL --column-names=0 -u$DBUSER -p$DBPASS $DBNAME &lt; "${TMPDIR}/${HOSTNAME}_gnuplot_client.dat"
    SELECT host_name, line_datetime, SUM(alloc_kb), SUM(used_kb) 
    FROM sandisk_clients 
    WHERE host_name LIKE '$HOSTNAME'
    GROUP BY YEAR(line_datetime), MONTH(line_datetime), DAYOFMONTH(line_datetime);
    EOF
    echo "set title '$HOSTNAME'"           &gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set xdata time"           &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set key box"            &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set key bottom right"         &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set size 1.5,1.5"           &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set xlabel 'Date'"          &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set ylabel 'Size, Kb' font 'Arial,12'"      &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set autoscale"            &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo 'set timefmt "%Y-%m-%d %H-%M-%S"'        &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set term png color"         &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "set output '${CHARDIR}/${HOSTNAME}_client_001.png'" &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    echo "plot '${TMPDIR}/${HOSTNAME}_gnuplot_client.dat' using 2:4 title 'Allocated, Kb' smooth bezier with
    linespoints, '${TMPDIR}/${HOSTNAME}_gnuplot_client.dat' using 2:5 title 'Used, Kb' smooth bezier with linespoints" &gt;&gt;  "${TMPDIR}/${HOSTNAME}_gnuplot_client.gnu"
    $GNUPLOT  /dev/null 2&gt;&amp;1
    done
}

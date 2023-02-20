# python option_trade_data.py -l 'custom' -n '30m'

# python option_trade_data.py -l 'custom' -n '15m'

# python option_trade_data.py -l 'dow' -n '30m'

# python option_trade_data.py -l 'dow' -n '15m'

# python option_trade_data.py -l 'sp500' -n '30m'

# python option_trade_data.py -l 'sp500' -n '15m'

#define the list of index
list_index="sp500 dow custom"
list_intervals="15m 30m"
# Iterate the string variable using for loop
for l in $list_index; do
    for i in $list_intervals; do
        echo "export " $l $i $1
        python /home/steven/dev/yosemite_jupyter/option_trade_data.py -l $l -n $i -dt $1
    done
done
echo "after"

var no_valid_entries = 1160
var from = "2017-04-25"
var to   = "2019-05-09"
var jp_search_number = 53
var jp_offer_number  = 14
var sw_search_number = 14
var sw_offer_number  = 1
var doy_data_jp_search  = [{t: '2016-05-01 00:00:00', y: 1},{t: '2016-05-16 00:00:00', y: 1},{t: '2016-06-05 00:00:00', y: 1},{t: '2016-06-05 00:00:00', y: 1},{t: '2016-07-08 00:00:00', y: 1},{t: '2016-09-14 00:00:00', y: 1},{t: '2016-09-17 00:00:00', y: 1},{t: '2016-09-18 00:00:00', y: 1},{t: '2016-09-26 00:00:00', y: 1},{t: '2016-10-17 00:00:00', y: 1},{t: '2016-10-23 00:00:00', y: 1},{t: '2016-10-24 00:00:00', y: 1},{t: '2016-10-25 00:00:00', y: 1},{t: '2016-10-28 00:00:00', y: 1},{t: '2016-10-31 00:00:00', y: 1},{t: '2016-11-06 00:00:00', y: 1},{t: '2016-12-04 00:00:00', y: 1},{t: '2016-12-05 00:00:00', y: 1},{t: '2016-12-12 00:00:00', y: 1},{t: '2016-12-20 00:00:00', y: 1},{t: '2016-01-22 00:00:00', y: 1},{t: '2016-01-24 00:00:00', y: 1},{t: '2016-02-24 00:00:00', y: 1},{t: '2016-02-26 00:00:00', y: 1},{t: '2016-03-12 00:00:00', y: 1},{t: '2016-04-21 00:00:00', y: 1},{t: '2016-04-26 00:00:00', y: 1},{t: '2016-05-02 00:00:00', y: 1},{t: '2016-05-07 00:00:00', y: 1},{t: '2016-05-16 00:00:00', y: 1},{t: '2016-05-23 00:00:00', y: 1},{t: '2016-06-20 00:00:00', y: 1},{t: '2016-07-10 00:00:00', y: 1},{t: '2016-08-26 00:00:00', y: 1},{t: '2016-09-18 00:00:00', y: 1},{t: '2016-09-18 00:00:00', y: 1},{t: '2016-09-25 00:00:00', y: 1},{t: '2016-09-28 00:00:00', y: 1},{t: '2016-10-05 00:00:00', y: 1},{t: '2016-10-09 00:00:00', y: 1},{t: '2016-10-12 00:00:00', y: 1},{t: '2016-11-14 00:00:00', y: 1},{t: '2016-11-20 00:00:00', y: 1},{t: '2016-11-29 00:00:00', y: 1},{t: '2016-01-06 00:00:00', y: 1},{t: '2016-01-16 00:00:00', y: 1},{t: '2016-02-06 00:00:00', y: 1},{t: '2016-02-11 00:00:00', y: 1},{t: '2016-02-20 00:00:00', y: 1},{t: '2016-03-18 00:00:00', y: 1},{t: '2016-04-02 00:00:00', y: 1},{t: '2016-04-29 00:00:00', y: 1},{t: '2016-05-07 00:00:00', y: 1}]
var doy_data_jp_offer   = [{t: '2016-05-02 00:00:00', y: 2},{t: '2016-05-03 00:00:00', y: 2},{t: '2016-07-26 00:00:00', y: 2},{t: '2016-08-12 00:00:00', y: 2},{t: '2016-10-28 00:00:00', y: 2},{t: '2016-10-29 00:00:00', y: 2},{t: '2016-03-07 00:00:00', y: 2},{t: '2016-03-26 00:00:00', y: 2},{t: '2016-05-02 00:00:00', y: 2},{t: '2016-07-01 00:00:00', y: 2},{t: '2016-07-15 00:00:00', y: 2},{t: '2016-11-08 00:00:00', y: 2},{t: '2016-11-22 00:00:00', y: 2},{t: '2016-04-13 00:00:00', y: 2}]
var doy_data_sw_search  = [{t: '2016-08-26 00:00:00', y: 4},{t: '2016-09-24 00:00:00', y: 4},{t: '2016-09-26 00:00:00', y: 4},{t: '2016-10-30 00:00:00', y: 4},{t: '2016-01-03 00:00:00', y: 4},{t: '2016-02-18 00:00:00', y: 4},{t: '2016-05-23 00:00:00', y: 4},{t: '2016-07-31 00:00:00', y: 4},{t: '2016-09-02 00:00:00', y: 4},{t: '2016-09-04 00:00:00', y: 4},{t: '2016-11-02 00:00:00', y: 4},{t: '2016-12-13 00:00:00', y: 4},{t: '2016-02-06 00:00:00', y: 4},{t: '2016-03-08 00:00:00', y: 4}]
var doy_data_sw_offer   = [{t: '2016-11-01 00:00:00', y: 5}]
var doy_labels= ['2016-01-01', '2016-02-01', '2016-03-01', '2016-04-01', '2016-05-01', '2016-06-01', '2016-07-01', '2016-08-01', '2016-09-01', '2016-10-01', '2016-11-01', '2016-12-01']
var search_labels_jp = ['German', 'English', 'Norwegian', 'French']
var search_values_jp = [12, 2, 1, 1]
var search_low_count_table_jp = ''

var search_labels_sw = ['Russian', 'French']
var search_values_sw = [1, 1]
var search_low_count_table_sw = ''


var clndr_icon = '<span class="glyphicon glyphicon-calendar"></span>'// document ready$( document ).ready(function() {  // we don't want any cache  $.ajaxSetup({ cache: false });  // setup the clndr control  clndr_init();  //hide the clndr control  hide_cal();  //ensure the clndr control displays ok on resize  $(window).on('resize', function(){    if($('#cal-container:visible').length != 0) {      gen_cal_css();    }  });});// clndr initfunction clndr_init() {  var date_string = moment.unix(get_current_unix_time()).format('YYYY-MM-DD');    $('#btn-calendar').html(date_string + " " + clndr_icon);  display_date_time(moment(date_string).unix());    // clndr_datetime is a hidden input to track the unix date time  // need to set a unix time from 12:00 AM for this to work on the initial load  $('#clndr_datetime').val(moment(date_string).unix());    var clndr = $('.devcal').clndr({        template: $('#template-calendar').html(),    startWithMonth: moment().add('month', 0),    clickEvents: {      click: function(target) {        var target_date = target.date._i;        var unix_time = moment(target_date).unix();        $('#btn-calendar').html(moment.unix(unix_time).format('YYYY-MM-DD') + " " + clndr_icon);        display_date_time(unix_time);        hide_cal();      }    }  });    // btn-calendar click  $("#btn-calendar").click(function() {    if($('#cal-container:visible').length == 0) {      show_cal();    }    else {      hide_cal();    }  });}// generate cal cssfunction gen_cal_css() {  var _pos = $("#btn-calendar").position();  var _width = $("#btn-calendar").width();  var _left = _pos.left;  $("#cal-container").css({    position: 'absolute',    top: (_pos.top + 20) + "px",    left: _left + "px",    width: _width + "px",    display: "block"  });}// show calendarfunction show_cal() {  gen_cal_css();  $('#cal-container').fadeIn( "slow", function() {    // Animation complete  });}// hide calendarfunction hide_cal() {  $('#cal-container').fadeOut( "fast", function() {    // Animation complete  });}// get_current_unix_timefunction get_current_unix_time() {  var m = moment();  var unix_time = m.unix();  return unix_time;}// display_date_timefunction display_date_time(d) {  if ($('#clndr_datetime').length) {    $('#clndr_datetime').val(d).trigger('change');    }  $('#day_name').html(moment.unix(d).format('dddd'));  $('#day_number').html(moment.unix(d).format('DD'));  $('#month_name').html(moment.unix(d).format('MMMM'));}// set locale timestampsfunction set_locale_timestamps(html_id, format) {  $.each($('span[id^=' + html_id + ']'), function( index, value ) {    var ts = $(value).html();    var m = moment.utc(ts);    if(format == "calendar") {        $(value).html(m.calendar());    }    else if(format == "fromNow") {        $(value).html(m.fromNow());    }    else {        $(value).html(m.format(format));    }  });}// set unix locale timestampsfunction set_unix_locale_timestamps(html_id, format) {  $.each($('span[id^=' + html_id + ']'), function( index, value ) {    var ts = $(value).html();    var m = moment.unix(ts);    if(format == "calendar") {        $(value).html(m.calendar());    }    else if(format == "fromNow") {        $(value).html(m.fromNow());    }    else {        $(value).html(m.format(format));    }  });}
// document ready$( document ).ready(function() {    // initial load    var unix_time = $('#clndr_datetime').val();    get_ajax_posts_latest(unix_time);});// get postsfunction get_ajax_posts_latest(unix_time) {  // latest posts  posts_url = '/ajax/p/latest';  $.ajax({      type: 'GET',      dataType: "html",      url: posts_url,      data: {date_time: unix_time },      success: function(data) {         $('#posts_latest').html(data);        set_locale_timestamps("p_l_ts_", "fromNow");        set_unix_locale_timestamps("p_l_unix_ts_", "YYYY-MM-DD");      },      contentType: "application/html",      dataType: 'html'  });}
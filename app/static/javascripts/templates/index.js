// document ready
$( document ).ready(function() {
  $('#clndr_datetime').on('change', function() {
    // get selected days posts
    // templates/partial/posts.js
    get_ajax_posts($('#clndr_datetime').val());
     
    // get latest posts
    // templates/partial/posts_latest.js
    get_ajax_posts_latest($('#clndr_datetime').val());
  });
});

(function($){
"use strict";

function setViewport() {
  if (wwidth > 631 && wwidth < 899){
    return $("html,body").animate({
      scrollLeft: rwidth
    }, 700), !1;
  }
}

$(window).load(function () {
  setViewport();
});

var rwidth = $("#river").width();
var wwidth = $(window).width();

}(jQuery));
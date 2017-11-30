var c = document.getElementById("canv");
var $ = c.getContext("2d");
c.width = window.innerWidth;
c.height = window.innerHeight / 5;

var num = 300;
var rad = 105 * Math.PI / num;
var o = [];
var _o;

var draw = function() {

  for (var i = 0; i < num; i++) {
    if (o.length < num) o[i] = i / num;
    _o = o[0];
    if (o[i] + 1 / num > 1) o[i] = 0;
    o[i] = o[i] + 1 / num;
    $.fillStyle = 'hsla(' + i + 2 + ', 90%, 50%,' + o[i] + ')';
    $.beginPath();
    $.setTransform(Math.cos(num * i),
      Math.sin(num * rad),
      Math.sin(num * i),
      Math.cos(num * rad),
      c.width / 2, c.height);
    if (i != 0)
      $.fillRect(num * 6 * o[i - 1], 0, c.width, c.height);
    else
      $.fillRect(num * 6 * _o, 0, c.width, c.height);
    $.fill();
  }

};
//animate && resize
window.addEventListener('resize', function() {
  c.width = window.innerWidth;
  c.height = window.innerHeight / 2;
}, false);

window.requestAnimFrame = (function() {
  return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function(callback) {
      window.setTimeout(callback, 1000 / 60);
    };
})();

var run = function() {
  window.requestAnimFrame(run);
  window.requestAnimationFrame(draw);

}
run();
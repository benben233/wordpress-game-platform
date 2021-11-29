let l = document.createElement("li")

l.innerHTML = '<input type="checkbox" id="checkboxOne" value="Rainbow Dash"><label for="checkboxOne">Rainbow Dash</label>'

// Click Handler Function
function clickHandler() {
  var transition = 'fade';
  var speed = 250
  var data = this.dataset;

  // Call Ajax Load More `filter` method
  ajaxloadmore.filter(transition, speed, data);
}
// Get All Filter Buttons
var buttons = document.querySelectorAll('ul.filters button');
if (buttons) {
  // Loop each button and add click event
  [].forEach.call(buttons, function (button) {
    button.addEventListener('click', clickHandler);
  });
}
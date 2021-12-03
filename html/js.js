let l = document.createElement("li")

l.innerHTML = '<input type="checkbox" id="checkboxOne" value="Rainbow Dash"><label for="checkboxOne">Rainbow Dash</label>'

// Click Handler Function
function clickHandler() {
  var data = this.dataset;
  var inputs = document.querySelectorAll('ul.ks-cboxtags li input[type="checkbox"]:checked');
  tag = ''
  inputs.forEach(x => tag += ',' + x.id)
  data.tag = tag
  data.meta_key = 'reviews'
  data.orderby = ''
  // Call Ajax Load More `filter` method
  ajaxloadmore.filter('fade', 250, data);
}
var button = document.querySelector("#sec-1626 div.u-layout-cell-2 > div > a")
button.addEventListener('click', clickHandler);
// Get All Filter Buttons
var buttons = document.querySelectorAll('ul.filters button');
if (buttons) {
  // Loop each button and add click event
  [].forEach.call(buttons, function (button) {
    button.addEventListener('click', clickHandler);
  });
}
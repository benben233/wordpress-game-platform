function clickHandler() {
  var data = this.dataset;
  var inputs = document.querySelectorAll('ul.ks-cboxtags li input.tag[type="checkbox"]:checked');
  var category_in = document.querySelectorAll('ul.ks-cboxtags li input.pub[type="checkbox"]:checked');
  var order = document.querySelector('select')
  var search = document.querySelector('#searchInput')
  tag = ''
  inputs.forEach(x => tag += x.id + ',')
  category = ''
  category_in.forEach(x => category += x.id + ',')
  data.tag = tag
  data.category = category
  data.meta_key = order.value
  data.orderby = order.value
  data.s = search.value
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
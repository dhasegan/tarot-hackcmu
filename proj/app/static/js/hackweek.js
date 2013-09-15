var timer = setInterval(function() {
	/* Code that goes here:
	 * Get the counter numbers from the html
	 * Decrease that number by 1
	 * Set the counter on the html to this new number
	 * *Note* for now, keep the time in terms of seconds ONLY
	 */
}, 1000);

setTimeout(function() {
	clearInterval(timer); //Stops the ticking of the timer
	/* Code that goes here:
	 * Removes the question or disables voting somehow
	 */
}, 60000); //Replace 60000 with how long the question lasts in milliseconds


// UI SLIDER
$('.ui-slider-handle').draggable({ axis: 'x', containment: "parent", stop: function() {
	var qcur = $(this).parents('.qvalue');
	var val = parseInt($(this).css('left'));

	var minv = parseFloat(qcur.siblings('.minvalue').text());
	var maxv = parseFloat(qcur.siblings('.maxvalue').text());

	var value = (val / 134) * (maxv - minv) + minv;

	qcur.siblings('.curvalue').text(Math.round(value.toString(),2))
}});

// LOGOUT LINK
$('.logout').click(function() {
    window.location.href = "/logout/";
});

// Timepicker
$('#timepicker1').timepicker();

// Ajax request for sending Question update
$('.submitquestion').click(function() {

	var errors = []
	var question = $('.dropdown-input').val();
	var date = $('.dropdown-dateinput').val();
	var time = $('.dropdown-timeinput').val();
	var minval = $('.dropdown-minvalue').val();
	var maxval = $('.dropdown-maxvalue').val();
	var csrf = $(this).parent().siblings('input[name=csrfmiddlewaretoken]').attr('value');
	var min, max;

	if (question.length <= 0 || question.length >= 140){
		alert('Please input a question!');
		return;
	}
	if (date.length <= 0 || date.length >= 10) {
		alert('Please input a date!')
		return ;
	}
	if (time.length <= 0 || time.length >= 10) {
		alert('Please input a time!')
		return ;
	}
	if (minval.length <= 0 || minval.length >= 6) {
		alert('Please input a minval!')
		return ;
	}
	if (maxval.length <= 0 || maxval.length >= 6) {
		alert('Please input a maxval!')
		return ;
	}
	min = parseInt(minval)
	max = parseInt(maxval)
	if (min == NaN || max == NaN || min >= max) {
		alert('Min and max values are not valid!')
		return ;
	}

	var dataString = 'text='+ question + '&date=' + date + '&time=' + time + '&minval=' + minval + '&maxval=' + maxval + '&csrfmiddlewaretoken=' + csrf;
	$.ajax({
	  type: "POST",
	  url: "/add_question",
	  data: dataString,
	  success: function(data) {
	  	var tl = $('#timeline');
	  	var emp = $('.emptyspacefornewquestion')
	  	var emphtml = '<div class="emptyspacefornewquestion"> </div>'
	  	$(emp).replaceWith(emphtml + data)
	  }
	});
	return false


	// xmlhttp.open("GET","demo_get2.asp?fname=Henry&lname=Ford",true);
	// xmlhttp.send();
});

// JAVASCRIPT FOR DATE
var nowTemp = new Date();
var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
	if (top.location != location) {
    top.location.href = document.location.href ;
  }
		$(function(){
			window.prettyPrint && prettyPrint();
			var startDate = new Date(2012,1,20);
			var endDate = new Date(2012,1,25);
			$('#dp1').datepicker()
				.on('changeDate', function(ev){
					if (ev.date.valueOf() > endDate.valueOf()){
						$('#alert').show().find('strong').text('The start date can not be greater then the end date');
					} else {
						$('#alert').hide();
						startDate = new Date(ev.date);
						$('#startDate').text($('#dp4').data('date'));
					}
					$('#dp4').datepicker('hide');
				});
			$('#dp2').datepicker()
				.on('changeDate', function(ev){
					if (ev.date.valueOf() < startDate.valueOf()){
						$('#alert').show().find('strong').text('The end date can not be less then the start date');
					} else {
						$('#alert').hide();
						endDate = new Date(ev.date);
						$('#endDate').text($('#dp5').data('date'));
					}
					$('#dp5').datepicker('hide');
				});

        // disabling dates
        var nowTemp = new Date();
        var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);

        var checkin = $('#dpd1').datepicker({
          onRender: function(date) {
            return date.valueOf() < now.valueOf() ? 'disabled' : '';
          }
        }).on('changeDate', function(ev) {
          if (ev.date.valueOf() > checkout.date.valueOf()) {
            var newDate = new Date(ev.date)
            newDate.setDate(newDate.getDate() + 1);
            checkout.setValue(newDate);
          }
          checkin.hide();
          $('#dpd2')[0].focus();
        }).data('datepicker');
        var checkout = $('#dpd2').datepicker({
          onRender: function(date) {
            return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
          }
        }).on('changeDate', function(ev) {
          checkout.hide();
        }).data('datepicker');
		});
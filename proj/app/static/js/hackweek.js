setInterval(function() {
	 var hs = $('.hidden-seconds')
	 $.each(hs, function(i, l) {
	 	make_string = function(secs) {
	 		if (secs < 1.0)
	 			return "";
	 		var sec = parseInt(secs) % 60;
	 		var min = Math.floor(parseInt(secs) / 60) % 60 ;
	 		var hour = Math.floor(parseInt(secs) / 3600) % 24;
	 		var days = Math.floor(parseInt(secs) / (3600*24) );
	 		var ss = sec.toString();
	 		var sm = min.toString();
	 		var sh = hour.toString();
	 		var sd = days.toString();

	 		if (sec < 10) {
	 			ss = "0" + ss;
	 		}
	 		if (min < 10) {
	 			sm = "0" + sm;
	 		}
	 		if (hour < 10) {
	 			sh = "0" + sh;
	 		}

	 		if (days == 0) {
	 			if (hour == 0) {
	 				if (min == 0) {
	 					if (sec == 0) {
	 						return ""
	 					}
	 					return ss;
	 				}
	 				return sm + ":" + ss;
	 			}
	 			return sh + ":" + sm + ":" + ss;
	 		}
	 		return sd + " days " + sh + ":" + sm + ":" + ss;
	 	}
	 	var counter = $(l).siblings('.counter');
	 	var secs = parseFloat($(l).text()) - 1;
	 	$(l).text(secs)
	 	var res = make_string(Math.floor(secs));
	 	if (res == "") {
	 		q = $(l).parents('.question')
	 		$($(l).parent()).html("<div class='endcountdown'> \
	 			<a class='questiontimeout'> Question timeout </a> \
	 			</div>")
	 	}
	 	counter.text(res);
	 }.bind(this));
}.bind(this), 1000);

// UI SLIDER on resize
$(window).resize(function() {
	var realValue = parseInt($(this).css("left")) / ($(this).parents(".ui-slider").width()-16)

	var width = $('.ui-slider').parents('.qvalue')[0].offsetWidth;
	$('.ui-slider').css('width', width);

	var sliders = $('.ui-slider-handle')
	$.each(sliders, function(i, slider) {
		var qcur = $(slider).parents('.qvalue');
		var sliderObj = $(slider);

		var minv = parseFloat(qcur.siblings('.minvalue').text());
		var maxv = parseFloat(qcur.siblings('.maxvalue').text());

		var realValue = (maxv - minv)/2 + minv;
		var nominalValue = ((sliderObj.parents('.ui-slider').width() - 16)/2) / (sliderObj.parents('.ui-slider').width())

   		$(this).css("left", parseInt(nominalValue * 100).toString() +"%");
		qcur.siblings('.curvalue').text((Math.round(realValue*10)/10).toString(),2)
	});
});

// UI SLIDER setup 
$('.ui-slider-handle').draggable({ axis: 'x', containment: "parent", stop: function() {
	var realValue = parseInt($(this).css("left")) / ($(this).parents(".ui-slider").width()-16)
   	$(this).css("left", parseInt($(this).css("left")) / ($(this).parents(".ui-slider").width() / 100)+"%");
	var qcur = $(this).parents('.qvalue');
	var val = parseInt($(this).css('left'));

	var minv = parseFloat(qcur.siblings('.minvalue').text());
	var maxv = parseFloat(qcur.siblings('.maxvalue').text());

	var value = realValue * (maxv - minv) + minv;

	qcur.siblings('.curvalue').text((Math.round(value*10)/10).toString(),2)
}});

// Ajax request for sending Answer update
$('.submitanswer').click(function() {

	var errors = []
	var form = $($(this).parents('.answerform'));
	var ans = parseFloat(form.children('.curvalue').text());
	var qid = form.children('.questionid').val();
	var csrf = form.children('input[name=csrfmiddlewaretoken]').attr('value');
	var q = form.parents('.question');

	var dataString = 'id='+ qid + '&ans=' + ans + '&csrfmiddlewaretoken=' + csrf;
	$.ajax({
	  type: "POST",
	  url: "/add_answer",
	  data: dataString,
	  success: function(data) {
	  	$(q).fadeOut('slow')
	  }
	});
	return false
});

// LOGOUT LINK
$('.logout').click(function() {
    window.location.href = "/logout/";
});
$('.discover-link').click(function() {
    window.location.href = "/discover/";
});
$('.dashboard-link').click(function() {
    window.location.href = "/dashboard/";
});
$('.questiontimeout').click(function() {
    window.location.href = "/dashboard/";
});

// Timepicker
var currenttime = new Date( new Date().getTime() + 30*60*1000 );
var currenttimestring = '';
if (currenttime.getHours() > 12)
	currenttimestring = currenttime.getHours() + ':' + currenttime.getMinutes() + ' PM';
else 
	currenttimestring = currenttime.getHours() + ':' + currenttime.getMinutes() + ' AM';
$('#timepicker1').timepicker('setTime', currenttimestring);

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
	  	if (emp == undefined)
	  		return ;
	  	var emphtml = '<div class="emptyspacefornewquestion"> </div>'
	  	var parent = $(emp).parent()
	  	$(emp).replaceWith(emphtml + data)

		// UI SLIDER setup
		$('.ui-slider-handle',$('.question')[0]).draggable({ axis: 'x', containment: "parent", stop: function() {
			var realValue = parseInt($(this).css("left")) / ($(this).parents(".ui-slider").width()-16)
		   	$(this).css("left", parseInt($(this).css("left")) / ($(this).parents(".ui-slider").width() / 100)+"%");
			var qcur = $(this).parents('.qvalue');
			var val = parseInt($(this).css('left'));

			var minv = parseFloat(qcur.siblings('.minvalue').text());
			var maxv = parseFloat(qcur.siblings('.maxvalue').text());

			var value = realValue * (maxv - minv) + minv;

			qcur.siblings('.curvalue').text((Math.round(value*10)/10).toString(),2)
		}});

		// Ajax request for sending Answer update
		$('.submitanswer', $('.question')[0]).click(function() {

			var errors = []
			var form = $($(this).parents('.answerform'));
			var ans = parseFloat(form.children('.curvalue').text());
			var qid = form.children('.questionid').val();
			var csrf = form.children('input[name=csrfmiddlewaretoken]').attr('value');
			var q = form.parents('.question');

			var dataString = 'id='+ qid + '&ans=' + ans + '&csrfmiddlewaretoken=' + csrf;
			$.ajax({
			  type: "POST",
			  url: "/add_answer",
			  data: dataString,
			  success: function(data) {
			  	$(q).fadeOut('slow')
			  }
			});
			return false
		});


	  }
	});
	$('.dropdown').toggleClass('open')
	return false
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

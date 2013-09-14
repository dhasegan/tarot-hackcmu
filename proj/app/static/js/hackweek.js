

$('.ui-slider-handle').draggable({ axis: 'x', containment: "parent", stop: function() {
	var qcur = $(this).parents('.qvalue');
	var val = parseInt($(this).css('left'));

	var minv = parseFloat(qcur.siblings('.minvalue').text());
	var maxv = parseFloat(qcur.siblings('.maxvalue').text());

	var value = (val / 134) * (maxv - minv) + minv;

	qcur.siblings('.curvalue').text(Math.round(value.toString(),2))
}});
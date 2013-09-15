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
	 * Runs the python script that takes the votes and user scores
	 * and updates the database with the new user private/public scores
	 */
}, 60000); //Replace 60000 with how long the question lasts in milliseconds

$('.ui-slider-handle').draggable({ axis: 'x', containment: "parent", stop: function() {
	var qcur = $(this).parents('.qvalue');
	var val = parseInt($(this).css('left'));

	var minv = parseFloat(qcur.siblings('.minvalue').text());
	var maxv = parseFloat(qcur.siblings('.maxvalue').text());

	var value = (val / 134) * (maxv - minv) + minv;

	qcur.siblings('.curvalue').text(Math.round(value.toString(),2))
}});

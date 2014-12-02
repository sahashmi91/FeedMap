var map;

function initialize(lat, long) {
	var mapOptions = {
		center: { lat: lat, lng: long},
		zoom: 10,
		styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#193341"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#2c5a71"}]},{"featureType":"road","elementType":"geometry","stylers":[{"color":"#29768a"},{"lightness":-37}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#406d80"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#406d80"}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#3e606f"},{"weight":2},{"gamma":0.84}]},{"elementType":"labels.text.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"administrative","elementType":"geometry","stylers":[{"weight":0.6},{"color":"#1a3541"}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#2c5a71"}]}],
		mapTypeId: google.maps.MapTypeId.SATELLITE
	};
	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);
}
google.maps.event.addDomListener(window, 'load', function() {
	initialize(20, 30);
});
overlay = $('.overlay-contentscale');
function jsonError() {
	expandButton = $('#expand');
	overlay.css('background', 'red');
	expandButton.html(' Failed internet connection.').fadeIn();
	expandButton.addClass('fa fa-exclamation-triangle uk-button-danger');
}
function closeOverlay() {
	overlay.removeClass('open').addClass('close');
}

tweetCount = 0;
function getContent(searchQuery) {
	tweetCount += 1;
	$.when(
		$.ajax({
			url: 'getfeed.json',
			crossDomain: true,
			dataType: 'json',
			success: function(data) {
				var topic = $('#topic');
				var expandButton = $('#expand');
				topic.html('#' + data.handle);
				expandButton.removeClass('fa-exclamation-triangle uk-button-danger');
				var tweet = '<div class="tweet">' + data.tweet + '</div>';
				var expand_msg = '<span class="ladda-label"></span><i class="fa fa-long-arrow-left"></i> Expand ' + tweetCount + ' <img src="button-logo.png" width="150" alt=""/>'
				if (data.twitterId == '') {
					$.UIkit.notify("<i class='fa fa-twitter'></i> New tweet by Anonymous", {pos:'top-left'});
				} else {
					$.UIkit.notify('<i class="fa fa-twitter"></i> New tweet by <a href="https://twitter.com/' + data.twitterId + "'>" + data.twitterId + '</a>', {pos:'top-left'});
				}

				expandButton.hide().html(expand_msg).fadeIn();
				$('.uk-offcanvas-bar').append(tweet);
			},
			error: function(){
				jsonError();
			}
		}),
		$.ajax({
			url: 'city-tweets.json',
			crossDomain: true,
			dataType: 'json',
			data: {city: searchQuery},
			success: function(cityData) {
				closeOverlay();
				city = $('city');
				city.html(cityData.city);
			},
			error: function(data) {
				jsonError();
			}
		})
	);
}

var interval = null;

function onSubmit(searchQuery) {
	if(interval) clearInterval(interval);

	getContent(searchQuery);

	interval = setInterval(function(){
		getContent(searchQuery);
	}, 5000);
}
$(function(){
	$('form').on('submit', function(e){
		e.preventDefault();
		var selectedTag = $(e.target).find('input').val();
		onSubmit(selectedTag);
	})
});
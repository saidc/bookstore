document.addEventListener('DOMContentLoaded', () => {
	var days = 3;
	var dias_en_segundos = 267840;

	fetch("/count_down", {
		method: "GET",
		headers: {"Content-Type": "application/json"},
		body: JSON.stringify({}) 
	}).then(function(response) {
		if (response.ok) {return response.json();} else {
			msg = "Ocurrio un error al obtener el countdown";
			console.log(msg);
			throw new Error(msg);
		}
	}).then(function(data){
		console.log("data de respuesta: ", data );
		console.log("count_down: ", data["count_down"] );
	}).catch(function(error) {
		msg = "Ocurrio un error al obtener el countdown";
		console.log(msg, error);
	});

	// Unix timestamp (in seconds) to count down to
	
	var twoDaysFromNow = (new Date().getTime() / 1000) + dias_en_segundos + 1;

	// Set up FlipDown
	var flipdown = new FlipDown(twoDaysFromNow)

		// Start the countdown
		.start()

		// Do something when the countdown ends
		.ifEnded(() => {
		console.log('The countdown has ended!');
		});
});

$("#cart").click(function(){
	window.location.href = "/cart";
});
  
;(function () {
	
	'use strict';
	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};


	var testimonialCarousel = function(){
		
		var owl = $('.owl-carousel-fullwidth');
		owl.owlCarousel({
			items: 1,
			loop: true,
			margin: 0,
			responsiveClass: true,
			nav: false,
			dots: true,
			autoHeight: true,
			smartSpeed: 800,
			autoHeight: true
		});

	};

	var contentWayPoint = function() {
		var i = 0;
		$('.animate-box').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('animated-fast') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .animate-box.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn animated-fast');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft animated-fast');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight animated-fast');
							} else {
								el.addClass('fadeInUp animated-fast');
							}

							el.removeClass('item-animate');
						},  k * 200, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '85%' } );
	};



	
	$(function(){
		testimonialCarousel();
		contentWayPoint();
	});


}());
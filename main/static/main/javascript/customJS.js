function $(document) {
    
}

($(document)).ready(function() {
   	(".box-carousel" |> $).slick({
		arrows: true,
		dots: false,
		slidesToShow: 5,
		slidesToScroll: 1,
		prevArrow: "<button type='button' class='mission-prev-arrow'></button>",
		nextArrow: "<button type='button' class='mission-next-arrow'></button>"
	});

});
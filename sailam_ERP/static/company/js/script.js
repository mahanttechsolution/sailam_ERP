// header
$(function() {
    var header = $(".add_class");
    $(window).scroll(function() {    
        var scroll = $(window).scrollTop();
    
        if (scroll >= 200) {
            header.removeClass('container').addClass("container-fluid");
            $(".container-fluid").css("transition" , "2s");
        } else {
            header.removeClass("container-fluid").addClass('container');
            $(".container").css("transition" , "2s");
        }
    });
});
// header  


// customer slider script 
var $slider = $('.slider');
  
if ($slider.length) {
  var currentSlide;
  var slidesCount;
  var sliderCounter = document.createElement('div');
  sliderCounter.classList.add('slider__counter');
  
  var updateSliderCounter = function(slick, currentIndex) {
    currentSlide = slick.slickCurrentSlide() + 1;
    slidesCount = slick.slideCount;
    $(sliderCounter).text(currentSlide + '/' +slidesCount)
  };

  $slider.on('init', function(event, slick) {
    $slider.append(sliderCounter);
    updateSliderCounter(slick);
  });

  $slider.on('afterChange', function(event, slick, currentSlide) {
    updateSliderCounter(slick, currentSlide);
  });

  $slider.slick();
}
// customer slider script 
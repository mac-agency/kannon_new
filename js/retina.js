// JavaScript Document

 $(function(){
        var retinaCheck = window.devicePixelRatio;
        if(retinaCheck >= 2) { // Retinaディスプレイと判定された場合
            $('img.retina').each( function() {
                var retinaimg = $(this).attr('src').replace(/\.(?=(?:png|jpg|jpeg)$)/i, '@2x.');
                $(this).attr('srcset', retinaimg + " 2x");
            });
            $('.blockWrap').children().each( function() {
                var retinaimg = $(this).attr('href').replace(/\.(?=(?:png|jpg|jpeg)$)/i, '@2x.');
                $(this).attr('href', retinaimg);
            });
            $('.tp-bgimg').each( function() {
                var retinaimg = $(this).attr('src').replace(/\.(?=(?:png|jpg|jpeg)$)/i, '@2x.');
                $(this).attr('src', retinaimg);
            });
        }
    });